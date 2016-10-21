from collections import OrderedDict
import re
import datetime
import ast
def bank_application():
    try:
        option = int(raw_input("To create a Bank account press 1" + "\n" + "To access an existing account press 2" + "\n"))
        if option==1:
           customer = New_BankAcc()
        elif option==2:
           customer = ExistingAcc()
    except ValueError:
        print "You Entered a wrong option"
        bank_application()

def New_BankAcc():
    dict_acc = {}
   # print "Enter yourinformation to create a account"
    Acc_no = raw_input("Account number\n> ")
    Name = raw_input("Name\n> ")
    Address = raw_input("Address\n>")
    Phone = raw_input("Phone Number\n> ")
    Balance = int(raw_input("Balance\n>"))
    dict_acc[Acc_no] = {"Name":Name,"Address":Address,"Phone":Phone,"Balance":Balance}
    with open("customer_db.txt","a+") as f:
        f.write(str(dict_acc)+"\n")       
    
def ExistingAcc():
    try:
        option = int(raw_input("\nTo Check balance enter 1" + "\n" + "To withdraw cash enter 2" + "\n" + "To deposit Cash into you account enter 3 " + "\n" + ">>")) 
        if option==1:
            check_balance()
        elif option==2:
            withdraw()
        elif option==3:
            deposit_cash()
        elif option==4:
            delete_acc()
    except ValueError:
         print "You Entered a wrong option"
         ExistingAcc()           

def check_balance():
    dict_i = {}
    date = datetime.datetime.now()
    acc_num = raw_input("Enter account number: ")
    pattern = re.compile(acc_num)
    with open('customer_db.txt','r') as f:
        for line in f:
            if pattern.search(line)!= None:
                line = line[line.find('Balance'):].split(' ')
                print line
                 #print "{0}, your Account Balance by {1} is {2}".format(dict_i[acc_num]['Name'],date,dict_i[acc_num]['Balance'])
                
def withdraw():
    acc_num = raw_input("Enter account number: ")
    amt = int(raw_input("Please enter amount to Withdraw:" + "\n" + ">>"))
    pattern = re.compile(acc_num)
    with open('customer_db.txt','r+') as f:
        for line in f:
            if pattern.search(line)!= None:
                line = line[line.find('Balance'):].split(',')
                res = int(line[0][-4:])
                res_1 = res - amt
                line = str(line[0][-4:])
                f.seek(39,0)
                f.write(line.replace(str(res),str(res_1)))
                print ("Your new account balance is {0}".format(res_1) + "\n")
                
                                 
def deposit_cash():
    acc_num = raw_input("Enter account number: ")
    amt = int(raw_input("Please enter amount to Deposit:" + "\n" + ">>"))
    pattern = re.compile(acc_num)
    with open('customer_db.txt','r+') as f:       
        for line in f:
            if pattern.search(line)!= None:
                line = line[line.find('Balance'):].split(',')
                res = int(line[0][-4:])
                res_1 = res + amt
                line = str(line[0][-4:])
                f.seek(39,0)
                f.write(line.replace(str(res),str(res_1)))
                print ("Your new credited balance is {0}".format(res_1) + "\n")
                    
def delete_acc():
    acc_num = raw_input("To delete your account enter your account number:" + "\n" + ">>")
    pattern = re.compile(acc_num)
    with open('customer_db.txt','r+') as f:
        for line in f:
            if pattern.search(line)!= None:
                dict_i = ast.literal_eval(line)
                dict_i.clear()
                print dict_i                

def main():               
 #   bank_application()
 #   ExistingAcc()
 #   check_balance()
#     withdraw()
     deposit_cash()
 #   delete_acc()
main()


