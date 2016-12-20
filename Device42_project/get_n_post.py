import requests
import certifi
import time
import json
import xlrd
import sys
import os
import collections
import logging
from datetime import datetime
from time import strftime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ConfigParser import SafeConfigParser
from ast import literal_eval
import warnings
import pdb


class Device_d42:

    def __init__(self):
            self.read_config()

    def log_file(self):
        logger = logging.getLogger('Debugging logs')
        logger.setLevel(logging.INFO)
        """
        create file handler which logs even debug messages
        """
        fh = logging.FileHandler(strftime("mylogfile_%m_%d_%Y.log"))
        logging.debug('This message should go to the log file')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def read_config(self):
        self.logger = self.log_file()
        self.logger.info("Reading all the credentials to connect to the database.....")
        filepath = sys.argv[1] 
        if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
            self.logger.info('File exists and is readable')
            print "yes"
        else:
            self.logger.warning('Either file is missing or is not readable')
            print "no"
        try:
            config = SafeConfigParser()
            config.read(filepath)
            self.username = config.get('config_param', 'D42_USERNAME')
            self.password = config.get('config_param', 'D42_PASSWORD')
            self.url = config.get('config_param', 'D42_URL')
            self.update_params = config.get('config_values', 'update_params')
            self.building_params = config.get('config_values', 'building_params')
            self.device_to_rack = config.get('config_values', 'device_to_rack')
            self.room_params = config.get('config_values', 'room_params')
            self.rack_params = config.get('config_values', 'rack_params')
            self.hw_params = config.get('config_values', 'hw_params')
            self.params = config.get('config_values', 'params')
            self.device_id = config.get('config_values', 'device_id')
            self.auth = (self.username, self.password)
            self.get_api = "rooms/"
            print type(self.hw_params)
        except IOError, error:
            sys.exit(error)
            print "error"

 
    def get_and_delete(self, method, theurl):
        """
        pass GET,DELETE as method and connection to api is made
        """
        method = method.upper()
        if method not in ('GET','DELETE'):
            self.logger.info('UserWarning Unsupported HTTP request.')
        try:
            resp = requests.request(method, theurl, auth = self.auth, verify = False)
        except requests.RequestException:
            self.logger.error('Exception has occured')
        else:
            return resp.text

    def post_data_func(self, theurl, data):
        method = "post"
        method = method.upper()
        if method not in ('GET','POST'):
            self.logger.info('UserWarning Unsupported HTTP request.')
        try:
            resp = requests.request(method, theurl, auth = self.auth, data = data, verify = False)
        except requests.RequestException:
            self.logger.error('Exception has occured')
        else:
            return resp.text

    def get_data(self, url, get_api):       
        theurl = url + get_api
        method = "get"
        result = self.get_and_delete(method, theurl)
        self.logger.info('Getting data from %s' %theurl)
        print result.encode('utf8')
 
        
    def post_room(self, url, room_params):
        """
        building name and room name is required
        """
        room_params = eval(room_params)
        if room_params.has_key('building') != True:
            self.logger.info('Building info not available for device')
        if room_params.has_key('name') != True:
            self.logger.info('Room info not available for device')
        else:
            theurl = url + "rooms/"
            result = self.post_data_func(theurl, room_params)
            print result

    def check_if_exists(self, theurl, api_key):
        result = self.get_and_delete("get", theurl)
        res = ast.literal_eval(result)
        result = res[api_key]
        roomnames = [i['name'] for i in result if 'name' in i]
        return roomnames

    def post_building(self, url, building_params):
        """
        building name is mandatory
        """
        building_params = eval(building_params)
        if building_params.has_key('name') != True:
            self.logger.info('Building info not available for device')
        else:            
            theurl = url + "buildings/"
            result = self.post_data_func(theurl, building_params)
            print result

    def post_racks(self, url, rack_params):
        """
        rack name, size (u size), and room name are all required
        check if room doesnt exist re-direct to add room function
        """
        rack_params = eval(rack_params)
        api_key = "rooms/"
        theurl = url + api_key
        roomnames = self.check_if_exists(theurl, api_key)
        for room in roomnames:
            if room in rack_params:
                self.logger.info('Room info exists for device')
            else:
                pass
        url = D42_URL + "racks/"
        result = self.connec_post(url,rack_params)
        print result
                
#        res = result.encode('utf8')            


    def post_hwmodel(self, url, hw_params):
        """
        Name = hardware model name is required.
        """
        hw_params = eval(hw_params)
        if hw_params.has_key('name') != True:
            self.logger.info('Hardware model name not available')
        else:
            theurl = url + "hardwares/"
            result = self.post_data_func(theurl, hw_params)
            self.logger.info("Hardware model is added to Device42",result)

    def post_device(self, url, params):
        """
        devices can be added without giving any hardware model
        """
        params = eval(params)
        theurl = url + "devices/"
        result = self.post_data_func(theurl, params)
        self.logger.info("Device is posted to Device42",json.dumps(result))
 
    def post_device_2_rack(self, url, device_to_rack):
        """
        Rack id or building/room/rack names and starting location (or auto) are required
        """
        device_to_rack = eval(device_to_rack)
        if device_to_rack.has_key('building') != True:
            self.logger.info('Building info not available for device')
        if device_to_rack.has_key('room') != True:
            self.logger.info('Room info not available for device')
        if device_to_rack.has_key('rack') != True:
            self.logger.info('Rack info not available for device')           
        else:            
            theurl = url + "device/rack/"
            result = self.post_data_func(theurl, device_to_rack)
        self.logger.info("Device is posted to Device42",json.dumps(result))
        print result
 
    def delete_data(self, url, device_id):       
        theurl = url +"devices/" + str(self.device_id)
        try:
            result = self.get_and_delete("delete", theurl)
            print result
        except requests.HTTPError:
            print ("Device id not found")

    def update_device(self, url, update_params):
        """
        Update an existing devices by name, serial, ID or asset number.
        """
        update_params = eval(update_params)
        theurl = url + "devices/"
        try:
            resp = requests.put(theurl, auth = self.auth, data=update_params, verify=False)
            print resp.raise_for_status()
            print json.loads(resp.content)
            self.logger.info('Device info has been updated')
        except requests.HTTPError:
            self.logger.warning('Device id not found')
            print ("Device id not found")

    def read_from_xlsx(self):
        xl_workbook = xlrd.open_workbook("deviceHard.xlsx")
        xl_sheet = xl_workbook.sheet_by_index(0)
        if xl_sheet is None:
            self.logger.warning("xl_sheet is None")           
        first_row = []
        for col in range(xl_sheet.ncols):
            first_row.append( xl_sheet.cell_value(0,col) )
        data_s =[]
        for row in range(1, xl_sheet.nrows):
            elm = collections.OrderedDict()
            for col in range(xl_sheet.ncols):
                elm[first_row[col]]=xl_sheet.cell_value(row,col)
            data_s.append(elm)       
        return data_s

    def post_multipledata(self, url):
        theurl = url + "devices/"
        data_s = self.read_from_xlsx()
        for i in range(2,13):
            data = dict(data_s[i])
            print data
            resp = requests.post(theurl, auth= self.auth, verify = False, data = data)
        print resp.text
        print resp.raise_for_status()

c = Device_d42()
#c.post_racks(c.url, c.rack_params)
#c.get_data(c.url, c.get_api)
#c.post_device(c.url, c.params)
#c.delete_data(c.url, c.device_id)
#c.update_device(c.url, c.auth, c.update_params)
#c.post_building(c.url, c.building_params)
#c.post_room(c.url, c.room_params)
#c.post_hwmodel(c.url, c.hw_params)
#c.post_multipledata(c.url)
c.post_device_2_rack(c.url, c.device_to_rack)       

