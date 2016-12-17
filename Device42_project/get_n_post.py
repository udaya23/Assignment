import requests
import certifi
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ConfigParser import SafeConfigParser
import collections


class device_42_app:

    D42_URL = "https://192.168.0.23/api/1.0/"
    get_api = "rooms/"
    params = {"name" : "db-181-eastport", "type" : "cluster", "virtual_host" : "yui","Location" : " Los Gatos"}
    update_params = {"name" : "TXARL1-MPC2", "serial_no":"NXQQ50905WQ","asset_no":"34000803B11B3040000002SW","virtual_subtype":"1"}
    building_params = {"name" : "Elcamino-Drive-CA","address" : "84 Rac st","contact_name" : "Andrew", "contact_phone": "669546768", "notes": "Second site"}
    room_params = {"building" : "New-Haven-DC","name": "DC room2","notes" : "Second room"}
    rack_params = {"name": "rack-101" , "size": "12"}
    hw_params = {"name": "L200" , "manufacturer":"Dell Inc","type": "physical","size": "12","depth":"Full Depth"}



#    D42_USERNAME = 'admin'
#    D42_PASSWORD = 'adm!nd42'

    def __init__(self):
        try:
            parser = SafeConfigParser()
            parser.read('config_param.cfg')
            section = parser.sections()[0]
            options = collections.OrderedDict(parser.items(section))
            self.dict = options.values()
            D42_USERNAME = self.dict[0]
            D42_PASSWORD = self.dict[1]
            auth= (D42_USERNAME,D42_PASSWORD)
        except IOError, error:
            sys.exit(error)


   def post_building(self,D42_URL,building_params):
        print D42_URL,D42_USERNAME,D42_PASSWORD
        print building_params
        theurl = D42_URL + "buildings/"
        resp = requests.post(theurl,auth= self.auth,data = building_params,verify=False)
        print resp.raise_for_status()
        print resp.text
        
    def post_room(self,D42_URL,room_params):
        if room_params.has_key('building') != True:
            print "Please enter a Building name for your room"
        else:
            theurl = D42_URL + "rooms/"
            self.dat = requests.post(theurl, auth= self.auth,data = room_params,verify =False)
            print self.dat.text


    def add_hwmodel(self,D42_URL,hw_params):
        theurl = D42_URL + "hardwares/"
        resp = requests.post(theurl,auth= self.auth,data = hw_params,verify=False)
        print resp.raise_for_status()
        print resp.text


    def get_data(self,D42_URL,get_api):
        theurl = D42_URL + get_api
        try:
            self.dat = requests.get(theurl, auth= self.auth,verify =False)
            print self.dat.text
#response 200.GET an entity corresponding to the requested resource is sent in the response;
        except IOError,e:
            print "error"

    def post_data(self,D42_URL,params):
        theurl = D42_URL + "devices/"
        resp = requests.post(theurl,auth= self.auth,data=params,verify=False)
        print resp.raise_for_status()
        print resp.text


    def delete_data(self,D42_URL,device_id):       
        theurl = D42_URL +"devices/" + str(self.device_id)
        try:
            resp = requests.delete(theurl,auth = self.auth, verify = False)
            print resp.raise_for_status()
            print json.loads(resp.content)
            print "deleted device id: ",self.device_id
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
c.get_data(c.D42_URL,c.get_api)
#c.post_data(c.D42_URL,c.params)
#c.delete_data(c.D42_URL,c.auth,c.device_id)
#c.update_device(c.D42_URL,c.auth,c.update_params)
#c.post_building(c.D42_URL,c.building_params)
#c.post_room(c.D42_URL,c.room_params)
#c.add_hwmodel(c.D42_URL,c.hw_params)
       

