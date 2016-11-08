import unittest
import MySQLdb
from unittest_cnct import *


class TestConntn(unittest.TestCase):
    
    def setUp(self):
        self.connt = MySQLdb.connect(host="localhost",port= 3306,user="root",passwd="$sweta$",db="Northwind")
        self.cursor = self.connt.cursor()
        self.conobj,self.curobj = c.connect(1,0.02)

# -----------> TestCase #1: checking if connection object is 0 or 1       
    def test_connect(self):
        self.assertNotEqual(self.connt,0)
#        self.assertEqual(self.conobj,self.connt)



# -----------> TestCase #2: checking if table exists or not. In this case test fails since "Table 'northwind.employe' doesn't exist"     
    def test_assertTableNotExists(self):
         q = "select count(*) from %s" %("Northwind.employe")
         self.assertRaises(self.connt.cursor().execute(q))


# -----------> TestCase #3: SELECT FUNCTION :checking for the len of rows returned check self.assertEqual(len(rows),1)

    def test_select(self):
        c.select(c.connect,c.log_file,name="Northwind.employees",dict_d = {'EmployeeID':[3],'City':"Seattle"})
        query = "SELECT * FROM %s WHERE %s IN (%s) " % ("Northwind.employees","EmployeeID" ,3)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.assertNotEqual(len(rows),1)   #returns error since len(row) returned will be 2 checked against 1


# -----------> TestCase #4: INSERT FUNCTION :checking for the len of rows returned check self.assertEqual(len(rows),1)


               
    def teardown(self):
        self.connt.rollback()
        self.connt.close()
        self.connt = None

if __name__ == '__main__':
    unittest.main()


#        self.assertEqual(self.conn,0)




