import re
import string


"""Write a program that maps a list of words into a list of integers representing the lengths of the correponding words. Write it in three different ways:
1) using a for-loop, 2) using the higher order function map(), and 3) using list comprehensions. """


#1. renaming file with todays date
"""
import os
import time
#from time import strftime
os.rename("11092016.py",time.strftime("%m_%d_%Y.py"))
"""

def len_strings(list_p):
    list_len = []
    for i in list_p:
        count = 0
        for j in i:
            count += 1
        list_len.append(count)
    print list_len
    
#list_p = raw_input("enter list of strings: ").split(",")
#len_strings(list_p)
    

#2. map function
def strings_map(list_s):
    len_str = []
    len_str = map(lambda x: len(x),list_s)
    return len_str

#list_s = raw_input("enter list of strings: ").split(",")
#print strings_map(list_s)

#3. list comprehension

def list_comp():
    str_l = ['good','morning','your']
    list_len = [len(i) for i in str_l]
    print list_len

#list_comp()


"""2. Write a version of a palindrome recogniser that accepts a file name from the user, reads each line,
and prints the line to the screen if it is a palindrome."""

def palindrome(filep):
    file_p = open(filep,"r")
    for line in file_p:
        line_l = line.strip(',')
        if line_l == line_l[::-1]:
            print line_l


filep = raw_input("enter a filename: ")
palindrome(filep)


    
    
    

    
