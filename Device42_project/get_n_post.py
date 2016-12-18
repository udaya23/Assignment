import requests
import certifi
import json
import ast
import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ConfigParser import SafeConfigParser
import collections
from ast import literal_eval
from collections import MutableMapping
import warnings


class device_42_app:

    D42_URL = "https://192.168.0.23/api/1.0/"
    get_api = "rooms/"
    device_id = 2
    params = {"name" : "db-181-eastport", "type" : "cluster", "virtual_host" : "yui","Location" : " Los Gatos"}
    update_params = {"name" : "TXARL1-MPC2", "serial_no":"NXQQ50905WQ","asset_no":"34000803B11B3040000002SW","virtual_subtype":"1"}
    building_params = {"name" : "Elcamino-Drive-CA","address" : "84 Rac st","contact_name" : "Andrew", "contact_phone": "669546768", "notes": "Second site"}
    room_params = {"building" : "New-Haven-DC","name": "DC room2","notes" : "Second room"}
    rack_params = {"name": "rack-102" , "size": "42","room":"DC room1","manufacturer":"Dell Inc."}
    hw_params = {"name": "L200" , "manufacturer":"Dell Inc","type": "physical","size": "12","depth":"Full Depth"}



#    D42_USERNAME = 'admin'
#    D42_PASSWORD = 'adm!nd42'

    try:
        parser = SafeConfigParser()
        parser.read('config_p.cfg')
        section = parser.sections()[0]
        options = collections.OrderedDict(parser.items(section))
        dict_a = options.values()
        D42_USERNAME = dict_a[0]
        D42_PASSWORD = dict_a[1]
        auth = (D42_USERNAME,D42_PASSWORD)
    except IOError, error:
        sys.exit(error)

#function that can be used to pass GET,DELETE as method and connection to api is made here
    def connec_func_get(self,method,theurl):
         method = method.upper()
         if method not in ('GET','DELETE'):
            print  "UserWarning(Unsupported HTTP request.)"
         try:
            resp = requests.request(method,theurl,auth = self.auth,verify = False)
         except requests.RequestException as e:
            self.last_request = False
         else:
            return resp.text


    def connec_post(self,theurl,data):
         method = "post"
         method = method.upper()
         if method not in ('GET','POST'):
            print  "UserWarning(Unsupported HTTP request.)"
         try:
            resp = requests.request(method,theurl,auth = self.auth,data = data,verify = False)
         except requests.RequestException as e:
            self.last_request = False
         else:
            return resp.text


    def get_data(self,D42_URL,get_api):       
        url = D42_URL + get_api
        method = "get"
        result = self.connec_func_get(method,url)
        print result.encode('utf8')
 
    def post_building(self,D42_URL,building_params):
#building name is required
        if building_params.has_key('name') != True:
            print "Please enter a Building name for your room"
        else:            
            url = D42_URL + "buildings/"
            result = self.connec_post(url,building_params)
            print result

        
    def post_room(self,D42_URL,room_params):
#building name and room name is required
        if room_params.has_key('building') != True:
            print "Please enter a Building name for your room"
        else:
            theurl = D42_URL + "rooms/"
            result = self.connec_post(url,room_params)
            print result

    def post_racks(self,D42_URL,rack_params):
#rack name, size (u size), and room name are all required
#check if room doesnt exist re-direct to add room function
        url = D42_URL + "rooms/"
        result = self.connec_func_get("get",url)
        res = ast.literal_eval(result)
        s = [i for i in res.values() if type(i) == list]
        s2 = ", ".join(repr(e) for e in s)
        s = s2[1:-1]
        words = re.split(': |,',s2)
        wi = str(rack_params['room'])
        for w in words:
            if w[1:-1] == wi:
                print "Room is found"
            else:
                pass
        url = D42_URL + "racks/"
        result = self.connec_post(url,rack_params)
        print result
                
#        res = result.encode('utf8')            

    def post_hwmodel(self,D42_URL,hw_params):
#Name = hardware model name is required.
        url = D42_URL + "hardwares/"
        result = self.connec_post(url,hw_params)
        print result

    def post_device(self,D42_URL,params):
        url = D42_URL + "devices/"
        result = self.connec_post(url,params)
        print result
 
    def delete_data(self,D42_URL,device_id):       
        url = D42_URL +"devices/" + str(self.device_id)
        try:
            result = self.connec_func_get("delete",url)
            print result
        except requests.HTTPError:
            print ("Device id not found")

#Update an existing devices by name, serial, ID or asset number.
    def update_device(self,D42_URL,update_params):
        theurl = D42_URL + "devices/"
        try:
            resp = requests.put(theurl,auth = self.auth,data=update_params,verify=False)
            print resp.raise_for_status()
            print json.loads(resp.content)
            print "Updated device from device name: "
        except requests.HTTPError:
            print ("Device id not found")


c = device_42_app()
#c.post_racks(c.D42_URL,c.rack_params)
#c.get_data(c.D42_URL,c.get_api)
#c.connec_fun(self,verb,theurl)
#c.post_device(c.D42_URL,c.params)
#c.delete_data(c.D42_URL,c.device_id)
#c.update_device(c.D42_URL,c.auth,c.update_params)
#c.post_building(c.D42_URL,c.building_params)
#c.post_room(c.D42_URL,c.room_params)
#c.post_hwmodel(c.D42_URL,c.hw_params)
       

