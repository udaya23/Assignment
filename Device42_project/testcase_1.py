import mock
import unittest

from test_module import Device_d42


class ClientTestCase(unittest.TestCase):

    def setUp(self):

        self.client = Device_d42()

    @mock.patch('test_module.requests.get')
    def test_get_ok(self, mock_get):
        """
        Test getting a 200 OK response from the _get method of MyAPIClient.
        """
        # Construct our mock response object, giving it relevant expected
        # behaviours
        import pdb
        pdb.set_trace()
        mock_response = mock.Mock()
        expected_status = 200
        mock_response.return_value = expected_status

        # Assign our mock response as the result of our patched function
        mock_get.return_value = mock_response

        url = 'https://192.168.0.29/api/1.0/'
        get_api = "rooms/"
        response_dict = self.client.get_data(url=url,get_api=get_api)
        print response_dict

        # Check that our function made the expected internal calls
#        mock_get.assert_called_once_with(url=url)
#        self.assertEqual(1, mock_response)

        # If we want, we can check the contents of the response
        self.assertEqual(response_dict, expected_status)

if __name__ == "__main__":
    unittest.main()
