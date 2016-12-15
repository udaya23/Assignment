# get and post data using requests library

import requests
import json
import certifi
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class device_42_app:

    D42_USERNAME = 'admin'
    D42_PASSWORD = 'adm!nd42'
    D42_URL = "https://192.168.0.22/api/1.0/"
    params = {"name" : "db-181-eastport", "type" : "cluster", "virtual_host" : "yui","Location" : " Los Gatos"}
    update_params = {"name" : "TXARL1-MPC2", "serial_no":"NXQQ50905WQ","asset_no":"34000803B11B3040000002SW","virtual_subtype":"1"}
    device_id = 2
    auth=(D42_USERNAME,D42_PASSWORD)


    def get_data(self,D42_URL,D42_USERNAME,D42_PASSWORD):
        theurl = D42_URL + "devices/"
        try:
            self.dat = requests.get(theurl, auth=(D42_USERNAME, D42_PASSWORD),verify =False)
            print self.dat.text
#response 200.GET an entity corresponding to the requested resource is sent in the response;
        except IOError,e:
            print "error"

    def post_data(self,D42_URL,D42_USERNAME,D42_PASSWORD,params):
        theurl = D42_URL + "devices/"
        resp = requests.post(theurl,auth=(D42_USERNAME,D42_PASSWORD),data=params,verify=False)
        print resp.raise_for_status()
        print resp.text

    def delete_data(self,D42_URL,auth,device_id):       
        theurl = D42_URL +"devices/" + str(self.device_id)
        try:
            resp = requests.delete(theurl,auth = auth, verify = False)
            print resp.raise_for_status()
            print json.loads(resp.content)
            print "deleted device id: ",self.device_id
        except requests.HTTPError:
            print ("Device id not found")

#Update an existing devices by name, serial, ID or asset number.
    def update_device(self,D42_URL,auth,update_params):
        theurl = D42_URL + "devices/"
        try:
            resp = requests.put(theurl,auth = auth,data=update_params,verify=False)
            print resp.raise_for_status()
            print json.loads(resp.content)
            print "Updated device from device name: "
        except requests.HTTPError:
            print ("Device id not found")
    
c = device_42_app()
#c.get_data(c.D42_URL,c.D42_USERNAME,c.D42_PASSWORD)
#c.post_data(c.D42_URL,c.D42_USERNAME,c.D42_PASSWORD,c.params)
#c.delete_data(c.D42_URL,c.auth,c.device_id)
c.update_device(c.D42_URL,c.auth,c.update_params)
