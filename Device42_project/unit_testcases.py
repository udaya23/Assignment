import unittest
import os
from latest_cfglogg import *
from testfixtures import LogCapture


class TestConntn(unittest.TestCase):
    
    def setUp(self):
        self.LOCAL_INSTALL_DIR = os.path.join("../device_42_project/","config_p.cfg")


    def test(self):
        self.assertEqual(os.path.exists(self.LOCAL_INSTALL_DIR),True)

    def test_logger_messages(self):       
        with LogCapture() as l:
          logger_test = c.log_file()
          logger_test.info('This message is tested from test case for checking if log messages are written')
#          l.check(
#          ('Debugging logs', 'INFO', 'This message should go to the log file'),
#          ('root', 'ERROR', 'an error'),
#        )

if __name__ == '__main__':
    unittest.main(exit=False)



