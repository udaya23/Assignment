import requests
import certifi
import json
import xlrd
import sys
import base64
import collections
import logging
import ast
from time import strftime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ConfigParser import SafeConfigParser
from ast import literal_eval


class Device_d42:

    def __init__(self):
            self.read_config()

    def log_file(self):
        """
        Create file handler which logs even debug messages
        """
        logger = logging.getLogger('Debugging logs')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(strftime("mylogfile_%m_%d_%Y.log"))
        logging.debug('This message should go to the log file')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def read_config(self):
        """
        Read all crederntails from a config file
        """
        self.logger = self.log_file()
        self.logger.info("Reading all the credentials to connect to the database.....")
        filepath = sys.argv[1] 
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
        except IOError,e:
            self.logger.error(e, exc_info=True)           

    def post_data(self, theurl, data):
        method = "POST"
        method = method.upper()
        try:
            resp = requests.request(method, theurl, auth = self.auth, data = data, verify = False)
            return resp.text
        except requests.error as err:
            self.logger.error(err)

    def get_data(self, url, api_key):
        """
        GET function to return the building/devices/room/rack data from Device42 API
        """       
        theurl = url + api_key
        method = "GET"
        try:
            resp = requests.request(method, theurl, auth = self.auth, verify = False)
            return resp.text
            self.logger.info('Getting data from %s' %theurl)
        except requests.error as err:
            self.logger.error(err)
 
    def get_names_list(self, url, api_key):
        """
        Getting the list of building/room/rack names from Device42 API
        """
        result = self.get_data(url,api_key)
        res = ast.literal_eval(result)
        api_key = api_key[:-1]
        result = res[api_key]
        names = [i['name'] for i in result if 'name' in i]
        return names

    def post_building(self, url, building_params):
        """
        For POST req to execute Building name parameter is mandatory
        """
        building_params = eval(building_params)
        if building_params.has_key('name') != True:
            self.logger.info('Building info not available for device')
        else:            
            theurl = url + "buildings/"
            result = self.post_data(theurl, building_params)
            self.logger.info(result)
            return result
           
    def post_room(self, url, room_params):
        """
        For POST req to execute Building name,room name parameters are required
        """
        buildingnames = self.get_names_list(url, "buildings/")
        for building in buildingnames:
            if building in room_params:
                self.logger.info('Room info exists for device')
            else:
                pass
        room_params = eval(room_params)
        try:
            if room_params.has_key('building') != True:
                self.logger.info('Building info not available for device')
            if room_params.has_key('name') != True:
                self.logger.info('Room info not available for device')
            else:
                theurl = url + "rooms/"
                result = self.post_data(theurl, room_params)
                self.logger.info(result)
        except exceptions.RequestException as err:
            self.logger.error(err)

    def post_racks(self, url, rack_params):
        """
        For POST req to execute rack name, size (u size), room name parameters are required
        check if room doesnt exist re-direct to add room function
        """
        roomnames = self.get_names_list(url, "rooms/")
        for room in roomnames:
            if room in rack_params:
                self.logger.info('Room info exists for device')
            else:
                pass
        rack_params = eval(rack_params)
        try: 
            if rack_params.has_key('name') != True:
                self.logger.info('Rack name not provided')
            if rack_params.has_key('size') != True:
                rack_params["size"] = 42
                url = D42_URL + "racks/"
                result = self.post_data(url,rack_params)
                self.logger.info(result)
                return result
        except exceptions.RequestException as err:
            self.logger.error(err)
                
    def post_hwmodel(self, url, hw_params):
        """
        For POST req to execute hardware model name parameter is required.
        """
        hw_params = eval(hw_params)
        try:
            if hw_params.has_key('name') != True:
                self.logger.info('Hardware model name not available')
            else:
                theurl = url + "hardwares/"
                result = self.post_data_func(theurl, hw_params)
                self.logger.info(result)
                return result
        except exceptions.RequestException as err:
            self.logger.error(err)

    def post_device(self, url, params):
        """
        Post Devices without giving any hardware model
        """
        params = eval(params)
        theurl = url + "devices/"
        result = self.post_data(theurl, params)
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
            result = self.post_data(theurl, device_to_rack)
            self.logger.info("Device is posted to Device42",json.dumps(result))
 
    def update_device(self, url, update_params):
        """
        Update an existing devices by name, serial, ID or asset number.
        """
        update_params = eval(update_params)
        theurl = url + "devices/"
        try:
            resp = requests.put(theurl, auth = self.auth, data=update_params, verify=False)
            self.logger.info(resp.raise_for_status())
            self.logger.info('Device info has been updated',json.loads(resp.content))
        except requests.HTTPError:
            self.logger.warning('Device id not found')
            
    def check_column_exists(self,lkeys):
        """
        Check if column names are correct"
        """
        columns_list = ['id','name','asset_no','type','network_device','in_service','building','rack','room','orientation','virtual_host','serial_no','hw_model','start_at','live_id','first_added','last_updated','storage_room','discovery_spec','device_host','customer','uuid','service_level','blade_chassis','blade_slot_no','device_host_chassis','fiber_switch','discovery_spec']
        for i in range(0,len(lkeys)):
            if lkeys[i] in columns_list:
                pass
            else:
                self.logger.info("columns names are wrong.Please provide correct column names")
                sys.exit(1)
        return True

    def read_column_names(self,keys):
        """
        Read column headers and check if there is any empty headers
        """
        for i in range(0,len(keys)): 
            if '' in keys:
                result = self.send_message()
                sys.exit(1)
            else:
                lkeys = map(str.lower,keys)
                if self.check_column_exists(lkeys) is True:                   
                    return lkeys
        return True
      
    def build_message(self):
        """
        Build E-mail message and subject
        """
        msg = """File has empty headers
        """
        msgd = MIMEText(msg)
        return msgd
 
    def send_message(self, sender, receivers):
        """
        Send E-mail to Developers incase of error
        """
        try:
            msg = self.build_message()
            sender = 'udaya.python23@gmail.com'
            receivers = ['udaya.ackula@gmail.com']
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.ehlo()
            s.starttls()
            s.login('udaya.python23@gmail.com','doyoulikewhatyousee')
            result = s.sendmail(sender, receivers, msg)
            return result
            self.logger.info("Successfully sent email")
            s.quit()
        except smtplib.SMTPException as error:
            self.logger.warning("Error: unable to send email")
            self.logger.warning(str(error))

    def read_from_xlsx(self):
        """
        Read data from Excel sheet
        """
        xl_workbook = xlrd.open_workbook("csv_devices.xlsx")
        sheet = xl_workbook.sheet_by_index(0)
        keys = [str(sheet.cell(0, col_index).value) for col_index in xrange(sheet.ncols)]
        lkeys = self.read_column_names(keys)
        dict_list = []
#        num_rows = sheet.nrows-1
        for row_index in xrange(1, sheet.nrows):
            d = {lkeys[col_index]: str(sheet.cell(row_index, col_index).value) 
                for col_index in xrange(sheet.ncols)}
            dict_list.append(d)
        return dict_list
    

    def post_multipledata(self, url):
        """
        Post Request for multiple data excel sheet
        """
        theurl = url + "device/"
        headers = {'Content-type': 'application/x-www-form-urlencoded',\
    			'Authorization' : 'Basic '+ base64.b64encode(self.username + ':' + self.password)}
        data_s = []
        data_s = self.read_from_xlsx()
        data_len = len(data_s)-1
        try:
            for i in range(0,data_len):
                data = dict(data_s[i])
                resp = requests.post(theurl, verify = False, data = data, headers = headers)
                self.logger.info(resp)
        except exceptions.RequestException as err:
            self.logger.error(err)

    def delete_device(self):
        """
        Delete request for device
        """
        theurl = url +"devices/" + str(self.device_id)
        try:
            result = self.delete_data("delete", theurl)
            self.logger.info(result)
        except exceptions.RequestException as err:
            self.logger.error(err)

    def delete_building(self):
        """
        Delete request for building
        """
        theurl = url +"buildings/" + str(self.building_id)
        try:
            result = self.delete_data("delete", theurl)
            self.logger.info(result)
        except exceptions.RequestException as err:
            self.logger.error(err)

    def delete_data(self, method, theurl):
        """
        Delete Data Requests library
        """
        method = str(method.upper())
        try:
            resp = requests.request(method, theurl, auth = self.auth, verify = False)
            return resp
        except exceptions.RequestException as err:
            self.logger.error(err)

c = Device_d42()
#c.check_if_exists(c.url,c.api_key)
#c.post_racks(c.url, c.rack_params)
#c.get_data(c.url, c.get_api)
#c.post_device(c.url, c.params)
#c.delete_data(c.url, c.device_id)
#c.update_device(c.url, c.auth, c.update_params)
#c.post_building(c.url, c.building_params)
#c.post_room(c.url, c.room_params)
#c.post_hwmodel(c.url, c.hw_params)
#c.post_multipledata(c.url)
#c.post_device_2_rack(c.url, c.device_to_rack)       

