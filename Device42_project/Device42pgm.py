import certifi
import json
import xlrd
import sys
import base64
import collections
import logging
import ast
import os
from time import strftime
from ConfigParser import SafeConfigParser
from ast import literal_eval
import pickle

logger = logging.getLogger('Debugging logs')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(strftime("mylogfile_%m_%d_%Y.log"))
logging.debug('This message should go to the log file')
logger = logging.getLogger('Debugging logs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(strftime("mylogfile_%m_%d_%Y.log"))
#logging.debug('This message should go to the log file')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


#while importing third party libraries if any error occurs User will be notified
try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except ImportError:
    logging.info("Import Error has Occured.Please Install Request module before proceeding by pip install module_name. Further follow Instructions on how to install a package")
    sys.exit(1)

#Opening config parameters file to read
#filepath = sys.argv[1]
filepath = "../Device42_project/config_param.cfg"
config = SafeConfigParser()
if not os.path.isfile(filepath):
    logger.info("Cannot find the file.Please make sure config file is present and is readaable")
    sys.exit(1)

 
class Device_d42:

    def __init__(self):
            self.read_config()
 
    def read_config(self):
        """
        Read all crederntails from a config file
        """
        logger.info("Reading all the credentials to connect to the database.....")
        try:
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
            self.sender = config.get('config_emailid', 'sender')
            self.receivers = config.get('config_emailid', 'receivers')
            self.password = config.get('config_emailid', 'password')
            #read from config file if user wants to use cache or get data directly from api
            self.read_cache = config.get('cache_header','cache_flag')
        except IOError,e:
            logger.error(e, exc_info=True)

    def create_cache(self):
        """
        This func creates cache of text files
        """
        get_api = ["racks","devices","hardwares","rooms","buildings"]
        try:
            for i in range(0,len(get_api)):
                names = [ ]
                fname = get_api[i]
                f = open('{0}.txt'.format(fname), 'w+')
                theurl =  self.url + fname
                resp = requests.get(theurl, auth = self.auth, verify = False)
                data =  json.loads(resp.text)
                if fname == "devices":
                    fname = fname.title()
                elif fname == "hardwares":
                    fname = "models"
                else:
                    fname = fname
                for d in data[fname]:
                    names.append(d['name'])
                print f.write(','.join(names))
                return f.write(','.join(names))
            f.close()
        except IOError,e:
            logger.error(e, exc_info=True)

    def read_file(self,fname):
        """
        Read the cache file created and return data of names
        """
        with open(fname, 'r') as f:
            data = f.read().split(',')
            f.close()
        return data

    def if_name_exists_in_cache(self,name,fname):
        """
        check from the cache data if it already exists in Device42 API
        """
        data = self.read_file(fname)
        exists = False
        for i in data:
            if name == i:
                exists = True
        return exists

    def update_cache_after_post(self,fname,data):
        """
        Update cache after every post
        """
        with open(fname, 'a+') as f:
            f.write(',{0}'.format(data))
        return True

    def data_req(self, url, api_key, data, method):
        """
        GET, POST, PUT requests are implemented
        """
        theurl = url + api_key
        try:
            resp = requests.request(method, theurl, auth = self.auth, data = data, verify = False)
            logger.info(resp)
            return resp.text
        except requests.error as err:
            logger.error(err)

    def get_names_list(self, url, api_key):
        """
        Getting the list of building/room/rack names from Device42 API
        """
        data = None
        result = self.data_req(url, api_key, data, method="GET")
        res = ast.literal_eval(result)
        api_key = api_key[:-1]
        result = res[api_key]
        names = [i['name'] for i in result if 'name' in i]
        return names

    def check_mandatory_fields(self, data, field_list):
        """
        check for mandatory parameters in the data
        """
        data = eval(data)
        if all(param in data for param in field_list):
            logger.info("All parameters available...Proceeding to Post Data..")
            field_check = True
        else:
            msg = "Mandatory parameters required to post data are missing"
            logger.error(msg.upper())
            self.send_message(msg, sender, receivers)
            sys.exit(1)
        return field_check
    
    def post_building(self, url, building_params):
        """
        For POST req to execute Building name parameter is mandatory
        """
        building_params = eval(building_params)
        building_name = building_params['name']
        if self.read_cache == True:
             exists = self.if_name_exists_in_cache(self, name = building_name, fname = "buildings.txt")
             if exists == True:
                logger.info('This Building already exists')
             else:            
                result = self.data_req(url=url, api_key="buildings/", data = building_params, method="POST")                
                logger.info(result)
                self.update_cache_after_post(fname="buildings.txt", data = building_params['name'])
                return result
        else:
            buildingnames = self.get_names_list(url = url, api_key = "buildings/")
            building_name_match = next((name for name in buildingnames if name in building_params),None)
            if not building_name_match:
                logger.info("Building is not available.Proceeding towards POST building....")
                result = self.data_req(url=url, api_key="buildings/", data = building_params, method="POST")
            else:
                logger.info("Building exists.")
        return True

                

    def post_room(self, url, room_params):
        """
        For POST req to execute Building name,room name parameters are required
        """
        room_params = eval(room_params)
        building_dict = {'name' : room_params['building']}
        #check if all mandotory fields are present or not
        field_check = self.check_mandatory_fields(data = room_params, field_list = ['building','name'])
        if field_check == True:
            # check if room name to be posted is already existing in the device42 api
            #if read_cache = True read from cache otherwise from get request response
            if self.read_cache == True:
                exists = self.if_name_exists_in_cache(self, name = room_params['name'], fname = "rooms.txt")
                if exists == True:
                    logger.info('This Room already exists')
                    sys.exit(1)
            else:
                roomnames = self.get_names_list(url = url, api_key = "rooms/")
                room_name_match = next((name for name in roomnames if name in room_params),None)
                if room_name_match:
                    logger.info('This Room already exists')
                    sys.exit(1)            
            #check if building already exists in Device42, If not create a building first
            if self.read_cache == True:
                 b_exists = self.if_name_exists_in_cache(self, name = room_params['building'], fname = "buildings.txt")
                 if b_exists == False:
                    logger.info('Building does not exist..Proceeding to creating building first....')
                    result = self.post_building(url = url, building_params = building_dict)
                    if result.status_code == 200:
                        logger.info('Post Building Successfull..Proceeding to creating room....')
                 else:                     
                    logger.info('Building exists..Proceeding to post room....')
                    result = self.data_req(url = url, api_key = "rooms/", data = room_params, method = "POST")
                    logger.info(result)
                #update in cache after succesful post of room
                 if result.status_code == 200:
                    self.update_cache_after_post(fname="rooms.txt",data = room_params['name'])
                    logger.info("Succesfull updating of CACHE")
                 else:
                    logger.error("POST ROOM IS NOT SUCCESSFULL")                   
            #if not using cache
            else:
                buildingnames = self.get_names_list(url = url, api_key = "buildings/")
                building_name_match = next((name for name in buildingnames if name in room_params),None)
                if not building_name_match:
                    logger.info("Building is not available.Proceeding towards POST building first....")
                    result = self.post_building(url = url, building_params = building_dict)
                else:
                    logger.info("Building exists.Proceed to POST room...")
                    
                result = self.data_req(url = url, api_key = "rooms/", data = room_params, method = "POST")
                logger.info(result)
        return True

 
    def post_racks(self, url, rack_params):
        """
        For POST req to execute rack name, size (u size), room name parameters are required
        check if room doesnt exist re-direct to add room function
        """       
        rack_params = eval(rack_params)
        room_dict = {'name' : room_params['room'], 'building' : room_params['building']}
        #check if all mandotory fields are present or not
        field_check = self.check_mandatory_fields(data = rack_params, field_list = ['size', 'room', 'name'])
        if field_check == True:
        # check if rack name to be posted is already existing in the device42 api
        #if read_cache = True read from cache otherwise from get request response
            if self.read_cache == True:
                 exists = self.if_name_exists_in_cache(self, name = rack_params['name'], fname = "racks.txt")
                 if exists == True:
                    logger.info('This Rack already exists')
                    sys.exit(1)
            else:
                 racknames = self.get_names_list(url = url, api_key = "racks/")
                 rack_name_match = next((name for name in racknames if name in rack_params),None)
                 if rack_name_match:
                    logger.info('This Rack already exists')
                    sys.exit(1)
        #check if Room already exists in Device42, If not create a Room first
            if self.read_cache == True:
                room_exists = self.if_name_exists_in_cache(self, name = rack_params['room'], fname = "rooms.txt")
                if room_exists == False:
                    logger.info('Room does not exist..Proceeding to creating room first....')
                    result = self.post_room(url = url, room_params = room_dict)
                    if result.status_code == 200:
                        logger.info('Post Room Successfull..Proceeding to creating rack....')
                else:                     
                    self.logger.info('Room exists..Proceeding to post Rack....')
                    result = self.data_req(url = url, api_key = "racks/", data = rack_params, method = "POST")
                    logger.info(result)
                #update cache after succesful post of room
                if result.status_code == 200:
                    self.update_cache_after_post(fname="racks.txt", data = rack_params['name'])
                    logger.info("Succesfull updating of CACHE")
                else:
                    logger.error("POST RACK IS NOT SUCCESSFULL")
                    
            #if not using cache
            else:
                roomnames = self.get_names_list(url = url, api_key = "rooms/")
                room_name_match = next((name for name in roomnames if name in rack_params),None)
                if not room_name_match:
                    logger.info("Room is not available.Proceeding towards POST room first....")
                    result = self.post_room(url = url, room_params = room_dict)
                else:
                    logger.info("Room exists.Proceed to POST rack...")
                    
                result = self.data_req(url = url, api_key = "racks/", data = rack_params, method = "POST")
                logger.info(result)
                #if rack_params.has_key('size') != True:
                #rack_params["size"] = 42
        return True
        
                
    def post_hwmodel(self, url, hw_params):
        """
        For POST req to execute hardware model name parameter is required.
        """
        hw_params = eval(hw_params)
        field_check = self.check_mandatory_fields(data = hw_params, field_list = ['name'])
        if field_check == True:
            #check if Hardware model name already exists in Device42
            if self.read_cache == True:
                 exists = self.if_name_exists_in_cache(self, name = hw_params['name'], fname = "hardwares.txt")
                 if exists == True:
                    logger.info('This Hardware model already exists')
                 else:
                    logger.info('HW model doesnot exist.Proceeding to creating a HWmodel...')
                    result = self.data_req(url = url, api_key = "hardwares/", data = hw_params, method = "POST")
                    logger.info(result)
                    if result.status_code == 200:
                        #update cache after succesful post of room
                        self.update_cache_after_post(fname="hardwares.txt", data = hw_params['name'])
                        logger.info("Succesfull updating of CACHE")
            #if not using cache
            else:
                 hwnames = self.get_names_list(url = url, api_key = "hardwares/")
                 hw_name_match = next((name for name in hwnames if name in hw_params),None)
                 if not hw_name_match:
                    self.logger.info('HW model doesnot exist.Proceeding to creating a HWmodel...')
                    result = self.data_req(url = url, api_key = "hardwares/", data = hw_params, method = "POST")
                    logger.info(result)
                 else:
                    logger.info('This Hardware model already exists')
        return True

    def post_device(self, url, params):
        """
        Post Devices without giving any hardware model
        """
        params = eval(params)
        field_check = self.check_mandatory_fields(data = params, field_list = ['name'])
        if field_check == True:
            if self.read_cache == True:
                 exists = self.if_name_exists_in_cache(self, name = params['name'], fname = "devices.txt")
                 if exists == True:
                    logger.info('This Device name already exists')
                 else:
                    result = self.data_req(url = url, api_key = "devices/", data = params, method = "POST")
                    logger.info(result)
                    if result.status_code == 200:
                        self.update_cache_after_post(fname="devices.txt", data = params['name'])
                        logger.info("Succesfull updating of CACHE")
            else:
                 devicenames = self.get_names_list(url = url, api_key = "devices/")
                 device_name_match = next((name for name in devicenames if name in params),None)
                 if not device_name_match:
                    logger.info('Device name doesnot exist.Proceeding to create...')
                    result = self.data_req(url = url, api_key = "devices/", data = params, method = "POST")
                    logger.info(result)
                 else:
                    logger.info('This Device name already exists')
        return True
 
    def post_device_2_rack(self, url, device_to_rack):
        """
        Rack id or building/room/rack names and starting location (or auto) are required
        """
        device_to_rack = eval(device_to_rack)
        field_check = self.check_mandatory_fields(data = device_to_rack, field_list = ['hw_model', 'start_at'])
        if field_check == True:
            if device_to_rack.has_key('start_at') != True:
                device_to_rack['start_at'] = 'auto'           
                result = self.data_req(url=url, api_key="device/rack/", data = device_to_rack, method="POST")
                logger.info("Device is added to the rack",json.dumps(result))
        return True
 
    def update_device(self, url, update_params):
        """
        Update an existing devices by name, serial, ID or asset number.
        """
        update_params = eval(update_params)
        try:
            resp = self.data_req(url = url, api_key = "devices/", data = update_params,  method = "PUT")
            logger.info(resp.raise_for_status())
            logger.info('Device info has been updated',json.loads(resp.content))
        except requests.HTTPError:
            logger.warning('Device id not found')

    """           
    def check_column_exists(self,lkeys):
        columns_list = ['id','name','asset_no','type','network_device','in_service','building','rack','room','orientation','virtual_host','serial_no','hw_model','start_at','live_id','first_added','last_updated','storage_room','discovery_spec','device_host','customer','uuid','service_level','blade_chassis','blade_slot_no','device_host_chassis','fiber_switch','discovery_spec']
        keys_a = []
        for i in range(0,len(lkeys)):
            if lkeys[i] in columns_list:
                keys_a.append(lkeys[i])
                return keys_a
            else:
                return False
                logger.info("columns names are wrong.Please provide correct column names")
        return True
        """
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
                #keys_a = self.check_column_exists(lkeys)
                return lkeys
        #return True
         
        
    def send_message(self, msg, sender, receivers):
        """
        Send E-mail to Developers incase of any Error which will stop the flow of 
        """
        try:
            msg = MIMEText(msg)
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.ehlo()
            s.starttls()
            s.login(self.sender, self.password)
            result = s.sendmail(self.sender, self.receivers, msg)
            return result
            logger.info("Successfully sent email")
            s.quit()
        except smtplib.SMTPException as error:
            logger.warning("Error: unable to send email")
            logger.warning(str(error))

    def read_from_xlsx(self,filename):
        """
        Read data from Excel sheet
        """
       
        xl_workbook = xlrd.open_workbook(filename)
        sheet = xl_workbook.sheet_by_index(0)
        keys = [str(sheet.cell(0, col_index).value) for col_index in xrange(sheet.ncols)]
        lkeys = self.read_column_names(keys)
        dict_list = []
        #num_rows = sheet.nrows-1
        for row_index in xrange(1, sheet.nrows):
            d = {lkeys[col_index]: str(sheet.cell(row_index, col_index).value) 
                for col_index in xrange(sheet.ncols)}
            dict_list.append(d)
        return dict_list
        
    def post_multipledata(self, filename):
        theurl = self.url + "device/"
        headers = {'Content-type': 'application/x-www-form-urlencoded',\
    			'Authorization' : 'Basic '+ base64.b64encode(self.username + ':' + self.password)}
        data_s = []
        data_s = self.read_from_xlsx(filename)
        buildingnames = self.get_names_list(self.url, "buildings/")
        for i in range(0,len(data_s)):
            data = dict(data_s[i])
            # If building is not created already it will be created
            if data["building"] not in buildingnames:
                keys = ['name']
                values = [data["building"]]
                buil_dict = str(dict(zip(keys,values)))
                self.post_building(url = self.url, building_params = buil_dict)
            resp = requests.post(theurl, verify = False, data = data, headers = headers)
            logger.info(resp)
                      
    def delete_req(self, method, theurl):
        """
        Delete Data Requests library
        """
        method = str(method.upper())
        try:
            resp = requests.request(method, theurl, auth = self.auth, verify = False)
            return resp
        except exceptions.RequestException as err:
            logger.error(err)

    def delete_device(self):
        """
        Delete request for device
        """
        theurl = url +"devices/" + str(self.device_id)
        try:
            result = self.delete_req("delete", theurl)
            logger.info(result)
        except exceptions.RequestException as err:
            logger.error(err)

    def delete_building(self):
        """
        Delete request for building
        """
        theurl = url +"buildings/" + str(self.building_id)
        try:
            result = self.delete_req("delete", theurl)
            logger.info(result)
        except exceptions.RequestException as err:
            logger.error(err)

c = Device_d42()
#c.read_from_xlsx()
#c.read_all_info()
#c.get_names_list(c.url)
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

