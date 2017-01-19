import mock
import unittest
import requests
import smtplib
import os
#from latest_cfglogg import *
from testfixtures import LogCapture
from Device42pgm import Device_d42
#from test_module import Device_d42
from mock import patch, call

"""
def resolve_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

FILE_EXCEL = resolve_file('../device_42_project/deviceHard.xlsx')
"""

class ClientTestCase(unittest.TestCase):
    
    def setUp(self):
        self.LOCAL_INSTALL_DIR = os.path.join("../device_42_project/","config_p.cfg")
        self.client = Device_d42()
        self.room_params = {"building" : "New-Haven-DC","name": "DC room3","notes" : "Third room"}


    def test_check_column_exists(self):
        test_keys = ['id','buildings']
        actual_result = self.client.check_column_exists(test_keys)
        self.assertEqual(actual_result,False)
                

    def test_get_names_list(self):
        url = 'https://192.168.0.30/api/1.0/'
        get_api = "buildings/"
        expected_resp = ['New-Haven-DC', 'Elcamino-Drive-CA']
        actual_result = self.client.get_names_list(url,get_api)       
        self.assertEqual(actual_result,expected_resp)

    def test_for_file_exists(self):
        self.assertEqual(os.path.exists(self.LOCAL_INSTALL_DIR),True)

    def test_logger_messages(self):       
        with LogCapture() as l:
          logger_test = c.log_file()
          logger_test.info('This message is tested from test case for checking if log messages are written')

    def test_local_excel(self):
#       Test reading from a local Excel file.And chck further if all rows are read or not
        xl_workbook = xlrd.open_workbook("csv_devices.xlsx")
        self.assertTrue(xl_workbook)
        sheet = xl_workbook.sheet_by_index(0)
        num_rows = sheet.nrows
        self.assertEqual(num_rows,14)
              

    # Mock 'smtplib.SMTP' class
    @patch("smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        # Check the E-mail Build test message and send message functions of MyAPIClient.
        from_address = 'udaya.python23@gmail.com'
        to_address = ['udaasre23@gmail.com']
        # Returns a send failur for the first recipient
        error = {
            to_address[0]: 
                (450, "Requested mail action not taken: mailbox unavailable")
        }
        msg = "Test Message"
 
        # Get instance of mocked SMTP object
        instance = mock_smtp.return_value
        instance.sendmail.return_value = error
        
         # Call 'send_message' function            
        result = self.client.send_message(from_address, to_address)
        
        #check if the function is called exactly once
        self.assertEqual(instance.sendmail.call_count, 1)

        #check if function returns error unable to send e-mail
        self.assertEqual(instance.sendmail.return_value, error)


    @mock.patch('test_module.requests.get')
    def test_get_ok(self, mock_get):
        
#        Test getting a 200 OK response from the get method of MyAPIClient.
#        Construct our mock response object, giving it relevant expected
#        behaviours
        
        mock_response = mock.Mock()
        expected_status = 200
        mock_response.return_value = expected_status

        # Assign our mock response as the result of our patched function
        mock_get.return_value = mock_response

        url = 'https://192.168.0.30/api/1.0/'
        get_api = "rooms/"
        response_dict = self.client.get_data(url=url,get_api=get_api)
        
        # If we want, we can check the contents of the response
        self.assertEqual(response_dict, expected_status)

    @mock.patch('test_module.requests.post')
    def test_post_ok(self, mock_post):       
#        Test getting a 200 OK response from the post method of MyAPIClient.
#        Construct our mock response object, giving it relevant expected
#        behaviours
        mock_response = mock.Mock()
        expected_status = 200
        mock_response.return_value = expected_status

        # Assign our mock response as the result of our patched function
        mock_post.return_value = mock_response

        url = 'https://192.168.0.30/api/1.0/rooms/'
        response_dict = self.client.post_data_func(data = self.room_params, theurl=url)
        # If we want, we can check the contents of the response
        self.assertEqual(response_dict, expected_status)
                
    
if __name__ == "__main__":
    unittest.main()


