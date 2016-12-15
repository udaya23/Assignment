import requests
import xlrd
import json
import codecs
import certifi
import base64
import collections
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'
D42_URL = "https://192.168.0.22/api/1.0/"
data_s =[]

def read_from_xlsx():
    xl_workbook = xlrd.open_workbook("csv_devices.xlsx")

    xl_sheet = xl_workbook.sheet_by_index(0)
    first_row = []

    for col in range(xl_sheet.ncols):
        first_row.append( xl_sheet.cell_value(0,col) )
#    data_s =[]
    for row in range(1, xl_sheet.nrows):
        elm = collections.OrderedDict()
#        elm = {}
        for col in range(xl_sheet.ncols):
            elm[first_row[col]]=xl_sheet.cell_value(row,col)
        data_s.append(elm)       
    return data_s

#params = {"name" : "TXARL1-MCC2","type": "physical"}

def post_data(D42_URL,D42_USERNAME,D42_PASSWORD,data_s):
    theurl = D42_URL + "devices/"
#    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    headers = {'Content-type': 'application/x-www-form-urlencoded',\
    			'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD)}
    auth=(D42_USERNAME,D42_PASSWORD)
#    import pdb
#    pdb.set_trace()
    for i in range(0,1):
        data = data_s[i]
#        print json.dumps(data_s[i])
#        print dict(data_s[i])
#    data = json.dumps(params)
        print data
        resp = requests.post(theurl,auth= auth,headers = headers,verify = False,data = data)
        print resp.text
        print resp.raise_for_status()


    

data_s = read_from_xlsx()
post_data(D42_URL,D42_USERNAME,D42_PASSWORD,data_s)



