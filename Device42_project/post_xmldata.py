# read a excel file with device data and upload it to the api from the requests post library method

import requests
import xlrd
import json
import codecs
import collections
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'
D42_URL = "https://192.168.0.20/api/1.0/"
data_s =[]

def read_from_xlsx():
    xl_workbook = xlrd.open_workbook("small_d42data.xlsx")

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


def post_method(D42_URL,D42_USERNAME,D42_PASSWORD,data_s):
    theurl = D42_URL + "devices/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    import pdb
    pdb.set_trace()
    for i in range(0,4):
        print json.dumps(data_s[i])
#        print dict(data_s[i])
        resp = requests.post(theurl,auth=(D42_USERNAME,D42_PASSWORD),verify = False, headers=headers,data = json.dumps(dict(data_s[i])))
        print resp.text
        print resp.raise_for_status()
