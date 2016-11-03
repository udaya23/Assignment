import MySQLdb
import time
import collections
from time import strftime
import logging
from datetime import datetime
from ConfigParser import SafeConfigParser

class Connection_db:
#everytime a instance is created for this class, the two fucntions to read the credentails of DB and connecting to the DB will be executed and return the connection object
     def __init__(self):
          self.update_from_config()
          self.conn,self.cursor = self.connect(1,200)

          
     def log_file(self):
          logger = logging.getLogger('Debugging logs')
          logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
          fh = logging.FileHandler(strftime("mylogfile_%H_%M_%m_%d_%Y.log"))
          fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
          formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
          fh.setFormatter(formatter)
# add the handlers to logger
          logger.addHandler(fh)
          return logger


     def update_from_config(self):          
          self.logger = self.log_file()
          self.logger.info("Reading all the credentials to connect to the database.....")
#reads a single section of a config file as a dict
          parser = SafeConfigParser()
          parser.read('config_db.cfg')
          section = parser.sections()[0]
          options = collections.OrderedDict(parser.items(section))
          self.dict = options.values()

           
     def connect(self,attempt_count,wait_interval):
          self.logger = self.log_file()          
#fucntion to connect to a database and will return the cursor and conn object to the database
          for self.attempt_number in range(attempt_count):
             try:
                 conn = MySQLdb.connect(host=self.dict[0],port= int(self.dict[1]),user=self.dict[2],passwd=self.dict[3],db=self.dict[4])
                 cursor = conn.cursor()
                 self.logger.info("Connecting to the database.....")
                 if conn:
                      break
             except Exception, e:
                 self.logger.error("Error with Connecting to database %d: %s" % (e.args[0], e.args[1]))
                 conn.rollback()
                 time.sleep(wait_interval)
                 connect()
          return conn,cursor

     def select(self,connect,log_file,name,dict_d):
#giving the number of attempts to make for connecting to database and wait time before making another attempt
          list_l = list(dict_d.values()[1])
          str_s= str(dict_d.keys()[1])  #EmployeeID
          query = "SELECT * FROM Northwind.employees WHERE %s IN (%s) " % ((str_s) , ','.join(str(n) for n in list_l))
          try:
               self.cursor.execute(query)
               self.logger.info("Executing SELECT statement (%s)" %query)
               for row in self.cursor.fetchall():
                    for i in range(0,len(row)-5):
                         print row[i]
          except MySQLdb.error,e:
               self.logger.error("Error in Selection query %d: %s" % (e.args[0], e.args[1]))

 
     def insert(self,connect,name,dict_d):
          columns = ','.join(dict_d.keys())
          values = dict_d.values()
          columns = columns.split(',')
          try:
               sql = "INSERT INTO Northwind.employees (%s, %s,%s) VALUES (%d, '%s', '%s')" % (columns[1],columns[2],columns[0],values[1],values[2],values[0]);
               self.cursor.execute(sql)
               self.logger.info("Executing INSERT statement (%s)" %sql)
               self.conn.commit()
          except MySQLdb.error,e:
               self.logger.error("Error with Inserting data %d: %s" % (e.args[0], e.args[1]))
               self.conn.rollback()
               close_connection()
               
     def update(self,connect,name,dict_d):
          dict_d = collections.OrderedDict(dict_d)
          emp_id = dict_d.keys()[1]
          try:
               sql = "UPDATE Northwind.employees SET {}".format(','.join('{}="{}"'.format(k,v) for k,v in dict_d.items()))
               sql += " WHERE %s=%s" %(emp_id,dict_d.values()[1])
               result = self.cursor.execute(sql)
               self.conn.commit()
          except MySQLdb.error,e:
               self.logger.error("Error with Inserting data %d: %s" % (e.args[0], e.args[1]))
               self.conn.rollback()
           
     def close_connection(self,connect):
          if conn:
              self.cursor.close()
              self.conn.close()
          
              

c = Connection_db()
c.select(c.connect,c.log_file,name="Northwind.employees",dict_d = {'EmployeeID':[3,7],'City':"Seattle"})
#c.insert(c.connect,name = "Northwind.employees",dict_d = {"EmployeeID" :13,"FirstName" : "zara", "LastName" : "Thomas"})
#c.update(c.connect,name="Northwind.employees",dict_d = {"EmployeeID":'13','FirstName':"stacy",'LastName':"Mandy",'Title':"CA"})
#c.close_connection(c.connect)              

"""     
#use-cases:
1.connect to db with correct userid,etc
2. connnect a db with wrong arg
3.cnt with empty agrs
#when we reate a log file use date time module and create a log file with date so each lof file will be created for a new day

"""
    
    


