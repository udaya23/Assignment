import MySQLdb
import time
#import configparser
import collections
from ConfigParser import SafeConfigParser

class Connection_db:
#everytime a instance is created for this class, the two fucntions to read the credentails of DB and connecting to the DB will be executed and return the connection object
     def __init__(self):
          self.update_from_config()
          self.conn,self.cursor = self.connect(3,200)
          

     def update_from_config(self):
#reads a single section of a config file as a dict
          parser = SafeConfigParser()
          parser.read('config_db.cfg')
          section = parser.sections()[0]
          options = collections.OrderedDict(parser.items(section))
          self.dict = options.values()

           
     def connect(self, attempt_count, wait_interval):
#fucntion to connect to a database and will return the cursor and conn object to the database
          for self.attempt_number in range(attempt_count):
             try:
                 conn = MySQLdb.connect(host=self.dict[0],port= int(self.dict[1]),user=self.dict[2],passwd=self.dict[3],db=self.dict[4])
                 cursor = conn.cursor()
             except MySQLdb.Error, e:
                 print "MySQL Error %d: %s", e.args[0], e.args[1]
                 conn.rollback()
                 time.sleep(wait_interval)
                 connect()
          return conn,cursor

     def select(self,connect,name,dict_d):
#giving the number of attempts to make for connecting to database and wait time before making another attempt
          list_l = list(dict_d.values()[1])
          str_s= str(dict_d.keys()[1])  #EmployeeID
          query = "SELECT * FROM Northwind.employees WHERE %s IN (%s) " % ((str_s) , ','.join(str(n) for n in list_l))
          try:
               self.cursor.execute(query)
               for row in self.cursor.fetchall():
                    for i in range(0,len(row)-5):
                         print row[i]
          except MySQLdb.error:
               print "Error has occured,closing the connection object"
               close_connection()

     def insert(self,connect,name,dict_d):
          columns = ','.join(dict_d.keys())
          values = dict_d.values()
          columns = columns.split(',')
          try:
               sql = "INSERT INTO Northwind.employees (%s, %s,%s) VALUES (%d, '%s', '%s')" % (columns[1],columns[2],columns[0],values[1],values[2],values[0]);
               print sql
               self.cursor.execute(sql)
               self.conn.commit()
          except MySQLdb.OperationalError:
               print "Query failed"
               self.conn.rollback()
               close_connection()

     def close_connection(self,connect):
         self.cursor.close()
         self.conn.close()

          
c = Connection_db()
#c.select(c.connect,name="Northwind.employees",dict_d = {'EmployeeID':[3,7],'City':"Seattle"})
#c.insert(c.connect,name = "Northwind.employees",dict_d = {"EmployeeID" :13,"FirstName" : "zara", "LastName" : "Thomas"})
c.close_connection(c.connect)              
     


    
    
    


