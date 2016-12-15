import requests
import certifi
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class device_42_app:

    D42_USERNAME = 'admin'
    D42_PASSWORD = 'adm!nd42'
    D42_URL = "https://192.168.0.20/api/1.0/"
    params = {"name" : "TXARL1-MPC1", "type" : "Physical", "virtual_host" : "yui", "Service_level" : "production", "Serial_no" : "NS4150191005", "Location" : " Los Gatos"}


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


    
c = device_42_app()
#c.get_data(c.D42_URL,c.D42_USERNAME,c.D42_PASSWORD)
c.post_data(c.D42_URL,c.D42_USERNAME,c.D42_PASSWORD,c.params)
