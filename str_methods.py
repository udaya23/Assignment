# Name: UDAYA SWETA
#E-mail ID: udaya.python23@gmail.com
# Assignment 2

#1. Practice all string methods

str_n = raw_input("enter your name: ")
str_u = str_n.upper()
print "This is my name in Upper Case:",str_u
str_c = str_n.capitalize()
print "This is my name with First letter in Upper Case:",str_c
str_cn = str_n.center(15,'*')
print "This is my name in center:",str_cn
str_len = len(str_n)
print "This is the length of my name:",str_len
str_count = str_n.count("e")
print "This is the count of 'h' in my name:",str_count
#find returns index if found and -1 otherwise
str_find = str_n.find('t')
print "This is the index of 't' in my name:",str_find
#index raises an exception if str not found
str_index_num = str_n.index('th')
print "This is the index of 'th' in my name:",str_index_num
rstr_find = str_n.find('e')
print "This is the index of 'e' from backwards in my name:",rstr_find
rindex = str_n.index("s")
print "This is the index of 'h' from backwards in my name:",rindex
str_title = str_n.title()
print "This is the title version of my name:",str_title
str_swap = str_n.swapcase()
print "This is the swapcase my name:",str_swap


#1. to use other methods in string, print out only the alphabets removing punctuations from a strin

import string
str_in = "Hi, There!How are you doing?"
str_out =" "
if i in string.punctuation:
    str_out.repalce(i," ")
print "input is:   \"Hi,There!How are you doing?\" \noutput is:"  ,str_out


#2.Display a triangle of *
num_of_lines = 5
for i in range(1,num_of_lines+3,2):
    num_of_lines -= 1
    print (" " * num_of_lines)+('#' *i)



#3. Read the integer,  and print the decimal, octal, hexadecimal, and binary values from  1 to 17  with space padding so that all fields take the same width as the binary value.
#Input: 17

def num_conv():
    for i in range(num+1):
        print i,"\t",format(i,'o'),"\t",format(i,'x'),"\t",format(i,'b')
num = input("enter a number:")
num_conv()
   



