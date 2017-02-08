import certifi
import json
import xlrd
import sys
import base64
import collections
import logging
import os
import ast
from time import strftime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
#from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser
from ast import literal_eval

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
    logger.info("Import Error has Occured.Please Install Request module before proceeding by pip install module_name. Further follow Instructions on how to install a package")
    sys.exit(1)

#Opening config parameters file to read
#filepath = sys.argv[1]
filepath = "../Device42_project/config_param.cfg"
config = SafeConfigParser()
if not os.path.isfile(filepath):
    logger.info("Cannot find the file.Please make sure config file is present and is readaable")
    sys.exit(1)
else:
    pass
 
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
            #self.read_cache = config.get('cache_header','cache_flag')
            self.read_cache = False
            if self.read_cache:
                self.create_cache()
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
                theurl =  self.url + fname
                if os.path.isfile(os.path.join('./',fname + '.txt')) == True:
                    #check if cache is up-to-date
                    data_from_api = self.get_list_of_entity_names(theurl = thrurl, fname = fname)
                    data_in_cache = self.read_file(fname = fname)
                    if set(data_from_api) == set(data_in_cache):
                        logger.info("Cache is up-to-date")
                    else:
                        logger.info("Re-write the cache as file is not being uodated")
                        self.write_to_file(fname = fname, data_from_api = data_from_api)
                else:
                    #get data from get request and parse it inot a list of entity names to write to cache
                    data_from_api = self.get_list_of_entity_names(theurl = thrurl, fname = fname)
                    #create a cache with all the data
                    self.write_to_file(fname = fname, data_from_api = data_from_api)                   
        except IOError,e:
            logger.error(e, exc_info=True)

    def write_to_file(self, fname, data_from_api):
        """
        write to file from the api get request response
        """
        try:
            f = open('{i}.txt'.format(fname), 'w')
            f.write(','.join(data_from_api))
            f.close()
        except:
            logger.info("File write is incomplete")
        return True

    def get_list_of_entity_names(self, theurl, fname):
        """
        request get data and parse it for usable data to write to cache
        """
        names = [ ]
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
        return names
        

    def read_file(self, fname):
        """
        Read the cache file created and return data of names
        """
        fname = fname + '.txt'
        try:
            with open(fname, 'r') as f:
                data = f.read().split(',')
                f.close()
            return data
        except IOError:
            logger.info("File read is not successfull.") 
            
    def if_name_exists_in_cache(self,name,fname):
        """
        check from the cache data if the entity that has to be created, already exists in Device42 API
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
        try:
            with open(fname, 'a+') as f:
                f.write(',{0}'.format(data))
                f.close()
            return True
        except IOError:
            logger.info("Update cache after post data failed.Please check if cache file exists") 

    def get_names_list(self, url, api_key):
        """
        Getting the list of building/room/rack names from Device42 API
        """
        data = None
        result = self.data_req(url, api_key, data, method="GET")
        res = ast.literal_eval(result.text)
        api_key = api_key[:-1]
        result = res[api_key]
        names = [i['name'] for i in result if 'name' in i]
        return names

    def data_req(self, url, api_key, data, method):
        """
        GET, POST, PUT requests are implemented
        """
        theurl = url + api_key
        try:
            resp = requests.request(method, theurl, auth = self.auth, data = data, verify = False)
            return resp
        except requests.error as err:
            logger.error(err)

    def check_mandatory_fields(self, data, field_list):
        """
        check for mandatory parameters in the data
        """
        #data = eval(data)
        if all(param in data for param in field_list):
            logger.info("All parameters available...Proceeding to Post Data..")
            field_check = True
        else:
            msg = "Mandatory parameters required to post data are missing"
            logger.error(msg.upper())
            self.send_message(msg, sender, receivers)
            sys.exit(1)
        return field_check


    def get_idnumber(self, api_key, name):
        """
        get id number of device/building/rack
        """
        id_key = api_key[:-2] + str('_id')
        theurl = self.url + api_key
        try:
            resp = requests.get(theurl, auth = self.auth, verify = False)
            json_data = json.loads(resp.text)
            id_num = next(d[id_key] for d in json_data[api_key.strip('/')] if d['name'] == name)
        except Error,err:
            logging.info("Getting ID number request was not successfull")
        return id_num

    def delete_request(self, api_key, building_id):
        """
        Delete request for building
        """
        theurl = self.url + api_key + str(building_id)
        try:
            resp = requests.delete(theurl, auth = self.auth, verify = False)
            logger.info("Delete request has been successfull" +str(resp.text))
        except requests.exceptions.RequestException as err:
            logger.error(err)
        return True
           
    def post_building(self, url, building_params):
        """
        For POST req to execute Building name parameter is mandatory
        """
        if type(building_params) == str:
            building_params = eval(building_params)
            #building_name = building_params['name']
        else:
            pass
        if self.read_cache == True:
             exists = self.if_name_exists_in_cache(self, name = eval(building_params['name']), fname = "buildings.txt")
             if exists == True:
                logger.info('This Building already exists')
             else:            
                result = self.data_req(url=url, api_key="buildings/", data = building_params, method="POST")                
                logger.info(result)
                #update cache with new building name only if it is success
                if result.status_code == 200:
                    self.update_cache_after_post(fname="buildings.txt", data = building_params['name'])
                    return result.status_code
        else:
            buildingnames = self.get_names_list(url = url, api_key = "buildings/")
            building_name_match = next((name for name in buildingnames if name in building_params),None)
            if not building_name_match:
                logger.info("Building is not available.Proceeding towards POST building....")
                result = self.data_req(url=url, api_key="buildings/", data = building_params, method="POST")
                logger.info("POST BUILDING IMPLEMENTED and the response is {}".format(result))
            else:
                logger.info("Building exists.")
        return True
               
    def post_room(self, url, room_params):
        """
        For POST req to execute Building name,room name parameters are required
        """
        if type(room_params) == str:
            room_params = eval(room_params)
        else:
            pass
        building_dict = {'name' : room_params['building']}
        #check if all mandotory fields are present or not
        field_check = self.check_mandatory_fields(data = room_params, field_list = ['building','name'])
        if field_check == True:
            # check if room name to be posted is already existing in the device42 api
            #if read_cache = True read from cache otherwise from get request response
            if self.read_cache == True:
                exists = self.if_name_exists_in_cache(self, name = room_params['name'], fname = "rooms.txt")
                if exists == True:
                    logger.info('This Room name already exists')
                    sys.exit(1)
            else:
                roomnames = self.get_names_list(url = url, api_key = "rooms/")
                room_name_match = next((name for name in roomnames if name in room_params),None)
                if room_name_match:
                    logger.info('This Room name already exists')
                    sys.exit(1)            
            #check if building already exists in Device42, If not create a building first
            if self.read_cache == True:
                 b_exists = self.if_name_exists_in_cache(self, name = room_params['building'], fname = "buildings.txt")
                 if b_exists == False:
                    logger.info('Building does not exist..Proceeding to creating building first....')
                    result.status_code = self.post_building(url = url, building_params = building_dict)
                    if result.status_code == 200:
                        logger.info('Post Building Successfull..Proceeding to creating room....')
                 else:                     
                    logger.info('Building exists..Proceeding to post room....')
                    result = self.data_req(url = url, api_key = "rooms/", data = room_params, method = "POST")
                    logger.info(result)
                #update in cache after succesful post of room
                 if result.status_code == 200:
                    self.update_cache_after_post(fname = "buildings.txt", data = room_params['building'])
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
                    logger.info("Proceeding towards post room")
                else:
                    logger.info("Building exists.Proceed to POST room...")
                    
                result = self.data_req(url = url, api_key = "rooms/", data = room_params, method = "POST")
                if result.status_code == 200:
                    logger.info("Room Posted successfully" +str(result))
                else:
                    #Implement rollback if the request is not succesfull
                    logger.info("POST ROOM was not successfull.so implemeting rollback and deleting the data created before")
                    #get building id and pass it to delete request function 
                    id_num = self.get_idnumber(api_key = "buildings/", name = building_dict['name'])
                    self.delete_request(api_key = "buildings/", id_num = id_num)                    
        return True

 
    def post_racks(self, url, rack_params):
        """
        For POST req to execute rack name, size (u size), room name parameters are required
        check if room doesnt exist re-direct to add room function
        """       
        if type(rack_params) == str:
            rack_params = eval(rack_params)
        else:
            pass
        room_dict = {'name' : rack_params['room'], 'building' : rack_params['building']}
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
                    self.update_cache_after_post(fname = "rooms.txt", data = rack_params['room'])
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
                if result.status_code == 200:
                     logger.info("succesfull POST RACK" + str(result.text))
                else:
                    #Implement rollback if the request is not succesfull
                    logger.info("POST RACK was not successfull.So implemeting rollback and deleting the data created before")
                    #get room id and pass it to delete request function 
                    id_num = self.get_idnumber(api_key = "rooms/", name = room_dict['name'])
                    self.delete_request(api_key = "rooms/", id_num = id_num)                    
                    #if rack_params.has_key('size') != True:
                    #rack_params["size"] = 42
        return True
        
                
    def post_hwmodel(self, url, hw_params):
        """
        For POST req to execute hardware model name parameter is required.
        """
        if type(hw_params) == str:
            hw_params = eval(hw_params)
        else:
            pass
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
        if type(params) == str:
            params = eval(params)
        else:
            pass
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
        if type(device_to_rack) == str:
            device_to_rack = eval(device_to_rack)
        else:
            pass
        field_check = self.check_mandatory_fields(data = device_to_rack, field_list = ['hw_model'])
        if field_check == True:
            #check if hwmodel exists
            hwmodel_names = self.get_names_list(url = url, api_key = "hardwares/")
            hwmodel_name_match = next((name for name in hwmodel_names if name in device_to_rack),None)
            if not hwmodel_name_match:
                logger.info('Hardware model doesnot exist.Proceeding to create...')
                hwmodel_dict = {'name' : device_to_rack['hw_model']}
                result = self.data_req(url = url, api_key = "hardwares/", data = hwmodel_dict, method = "POST")
                logger.info("HW model" + str(result))
            else:
                logger.info('This Hardware model exists')

            rack_names = self.get_names_list(url = url, api_key = "racks/")
            rack_name_match = next((name for name in rack_names if name in device_to_rack),None)
            if not rack_name_match:
                logger.info('Rack doesnot exist.Proceeding to create...')
                rack_dict = {'name': device_to_rack['rack'], 'room': device_to_rack['room'],'building': device_to_rack['building']}
                result = self.data_req(url = url, api_key = "racks/", data = rack_dict, method = "POST")
                logger.info("Creating a Rack model" + str(result))
            else:
                logger.info('This Hardware model exists')

            if device_to_rack.has_key('start_at') != True:
                device_to_rack['start_at'] = 'auto'
                #all checks finished 
                #add device to rack
                try:
                    result = self.data_req(url=url, api_key="device/rack/", data = device_to_rack, method="POST")
                    logger.info("Device is added to the rack" + str(result))
                except requests.exceptions.RequestException as err:
                    logger.error(err)
        return True
 
    def update_device(self, url, update_params):
        """
        Update an existing devices by name, serial, ID or asset number.
        """
        if type(update_params) == str:
            update_params = eval(update_params)
        else:
            pass
        try:
            resp = self.data_req(url = url, api_key = "devices/", data = update_params,  method = "PUT")
            logger.info(resp.raise_for_status())
            logger.info('Device info has been updated'+str(resp))
        except requests.HTTPError:
            logger.warning('Device id not found')


    def check_column_exists(self,keys):
         """
         Check if columns have valid headers or not
         """
         columns_list = ['id','name','type','asset_no','uuid','customer','blade_slot_no','device_host_chassis','network_device','building','rack','room','orientation','virtual_host','serial_no','hw_model','hardware','start_at','live_id','first_added','last_updated','storage_room','discovery_spec','device_host','customer','uuid','service_level','in_service','blade_chassis','fiber_switch','discovery_spec','asset_no']
         all_columns_valid =  all((False for x in keys if x not in columns_list))
         if all_columns_valid == False:
             logger.info("columns names are wrong.Cannot proceed further.Please provide correct column names")
             result = self.send_message("File has has invalid headers", self.sender, self.receivers)
             sys.exit(1)
         else:
             return all_columns_valid
 
 
    def read_column_names(self,keys):
         """
         Read column headers and check if there is any empty headers
         """
         column_has_none = any(True for x in keys if (x == " " or x == 'None'))
         if column_has_none == True:
             result = self.send_message("File has has empty headers or None.",self.sender,self.receivers)
             sys.exit(1)
         else:
             all_columns_valid = self.check_column_exists(keys)
             if all_columns_valid == True:
                 logger.info("All checks passed.Proceeding towards POST DATA")
         return True
          
    def send_message(self, msg, sender, receivers):
        """
        Send E-mail to Developers incase of any Error which will stop the flow of 
        """
        try:
            #msg = MIMEMultipart()
            #msg.attach(MIMEText(msg, 'plain'))
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(self.sender, self.password)
            #text = msg.as_string()
            result = s.sendmail(self.sender, self.receivers, msg)
            return result
            logger.info("Successfully sent email")
            s.quit()
        except smtplib.SMTPException as error:
            logger.warning("Error: unable to send email")
            logger.warning(str(error))
          

    def read_from_xlsx(self, filename):
        """
        Read data from Excel sheet
        """       
        xl_workbook = xlrd.open_workbook(filename)
        sheet = xl_workbook.sheet_by_index(0)
        keys = [str(sheet.cell(0, col_index).value) for col_index in xrange(sheet.ncols)]
        lkeys = map(str.lower,keys)
        status_to_proceed = self.read_column_names(lkeys)
        if status_to_proceed:
            dict_list = []
            #num_rows = sheet.nrows-1
            for row_index in xrange(1, sheet.nrows):
                d = {lkeys[col_index]: str(sheet.cell(row_index, col_index).value) 
                    for col_index in xrange(sheet.ncols)}
                dict_list.append(d)
            return dict_list
   
    def post_multipledata(self, filename):
        #filename = "csv_dev.xlsx"
        theurl = self.url + "device/"
        headers = {'Content-type': 'application/x-www-form-urlencoded',\
    			'Authorization' : 'Basic '+ base64.b64encode(self.username + ':' + self.password)}
        data_s = []
        data_s = self.read_from_xlsx(filename)
#        buildingnames = self.get_names_list(self.url, "buildings/")
        for i in range(0,len(data_s)):
            data = dict(data_s[i])
            resp = requests.post(theurl, data = data, auth = self.auth ,headers = headers, verify = False)
            if resp.status_code != 200:
                logger.info("error in post data"+str(resp.text))
            else:
                logger.info("POST DATA SUCCESS"+str(resp.text))
        return True

            # If building is not created already it will be created
        """
            if data["building"] not in buildingnames:
                keys = ['name']
                values = [data["building"]]
                buil_dict = str(dict(zip(keys,values)))
                resp = self.post_building(url = self.url, building_params = buil_dict)
                """


c = Device_d42()
#c.get_list_of_entity_names()
c.read_file('test_file.txt')
#c.send_message(c.sender, c.receivers)
#c.get_idnumber()
#c.read_from_xlsx('testexcel.xlsx')
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
#c.post_racks(c.url,c.rack_params)
#c.post_hwmodel(c.url, c.hw_params)
#c.post_multipledata()
#c.post_device_2_rack(c.url, c.device_to_rack)       

