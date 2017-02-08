import mock
import unittest
import requests
import smtplib
import os
import xlrd
#from latest_cfglogg import *
from testfixtures import LogCapture
from Device42pgm import Device_d42
#from test_module import Device_d42
from mock import patch, call
import shutil, tempfile
from os import path
from tempfile import NamedTemporaryFile
"""
def resolve_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

FILE_EXCEL = resolve_file('../device_42_project/deviceHard.xlsx')
"""

class ClientTestCase(unittest.TestCase):
    
    def setUp(self):
        self.LOCAL_INSTALL_DIR = os.path.join("../Device42_project/","config_param.cfg")
        self.client = Device_d42()
        self.room_params = {"building" : "New-Haven-DC","name": "DC room3","notes" : "Third room"}

    def test_read_file(self):
        # Change the file name to something
        fname = 'test_file.txt'
        fp = open(fname, 'w+')
        # Write testdata to it
        fp.write('The owls are not what they seem')
        fp.close()
        data = self.client.read_file('test_file')
        self.assertEqual(data, ['The owls are not what they seem'])
        # Remove the file
        os.remove(fname)

    
    def test_read_column_names(self):
        test_keys = [' ','None', 'id', 'rack_name']
        with self.assertRaises(SystemExit) as cm:
            actual_result = self.client.read_column_names(test_keys)       
            self.assertEqual(cm.exception.code,1)
     
    def test_check_column_exists(self):
        test_keys = ['id','building']
        actual_result = self.client.check_column_exists(test_keys)
        self.assertEqual(actual_result,True)
                
    def test_get_names_list(self):
        url = 'https://192.168.0.20/api/1.0/'
        get_api = "buildings/"
        expected_resp = ['New-Haven-DC', 'Elcamino-Drive-CA','Elcamino-CA']
        actual_result = self.client.get_names_list(url,get_api)       
        self.assertEqual(actual_result,expected_resp)
    
    def test_logger_messages(self):       
        with LogCapture() as l:
          logger_test = c.log_file()
          logger_test.info('This message is tested from test case for checking if log messages are written')
    
    def test_local_excel(self):
        xl_workbook = xlrd.open_workbook("csv_devices.xlsx")
        self.assertTrue(xl_workbook)
        sheet = xl_workbook.sheet_by_index(0)
        num_rows = sheet.nrows
        dict_list_expected = []
        keys = [str(sheet.cell(0, col_index).value) for col_index in xrange(sheet.ncols)]
        for row_index in xrange(1, sheet.nrows):
            d = {keys[col_index]: str(sheet.cell(row_index, col_index).value) 
                for col_index in xrange(sheet.ncols)}
            dict_list_expected.append(d)        
        #test_read_from_xlsx to get actual data
        dict_list_actual = self.client.read_from_xlsx("csv_devices.xlsx")   
        self.assertEqual(num_rows,15)
        self.assertEqual(dict_list_expected,dict_list_actual)
    
    def test_check_mandatory_fields(self):
        actual_result = True
        field_check_actual = self.client.check_mandatory_fields(data = self.room_params, field_list = ['building','name'])
        self.assertEqual(actual_result,True)

    # Mock 'smtplib.SMTP' class
    @patch("smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        # Check the E-mail Build test message and send message functions of MyAPIClient.
        # Returns a send failur for the first recipient
        from_address = 'udaya.python23@gmail.com'
        to_address = 'udaasre23@gmail.com'
        msg = "Test Message"

        error = {
            to_address: 
                (450, "Requested mail action not taken: mailbox unavailable")
        }
 
        # Get instance of mocked SMTP object
        instance = mock_smtp.return_value
        instance.sendmail.return_value = error
        
         # Call 'send_message' function            
        result = self.client.send_message(msg, from_address, to_address)
        
        #check if the function is called exactly once
        self.assertEqual(instance.sendmail.call_count, 1)

        #check if function returns error unable to send e-mail
        self.assertEqual(instance.sendmail.return_value, error)
        
    
    @mock.patch('Device42pgm.requests.get')
    def test_get_ok(self, mock_get):
    """
        #Test getting a 200 OK response from the get method of MyAPIClient.
        #Construct our mock response object, giving it relevant expected
        #behaviours
    """       
        mock_response = mock.Mock()
        expected_status = 200
        mock_response.return_value = expected_status

        # Assign our mock response as the result of our patched function
        mock_get.return_value = mock_response

        url = 'https://192.168.0.20/api/1.0/'
        get_api = "rooms/"
        method = "GET"
        response = self.client.data_req(method = method, data = None, url = url, api_key = get_api)
        response_actual = response.status_code
        # If we want, we can check the contents of the response
        self.assertEqual(response_actual, expected_status)

    @mock.patch('Device42pgm.requests.post')
    def test_post_ok(self, mock_post):
    
        #Test getting a 200 OK response from the post method of MyAPIClient.
        #Construct our mock response object, giving it relevant expected
        #behaviours

        mock_response = mock.Mock()
        expected_status = 200
        mock_response.return_value = expected_status

        # Assign our mock response as the result of our patched function
        mock_post.return_value = mock_response

        url = "https://192.168.0.20/api/1.0/"
        api_key = "rooms/"
        method = "POST"
        response = self.client.data_req(method = method, api_key = api_key, data = self.room_params, url=url)
        response_actual = response.status_code
        # If we want, we can check the contents of the response
        self.assertEqual(response_actual, expected_status)
        

if __name__ == "__main__":
    unittest.main()


