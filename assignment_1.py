# Name: UDAYA SWETA
#E-mail ID: udaya.python23@gmail.com
# Assignment 1

#1. Take a command line argument and assign it to variable ‘input1’, and print input1 on console and then take input2 from user and print result of  input1 + input2.
"""
import sys

input1 = sys.argv[1]
print input1
input2 = raw_input("enter your input: ")
print input1+input2
"""

#2. Write a program asking for user's name and age (input and raw_input). Display asking for user's name and age (input and raw_input). Display a message conveying user the year that he will turn 80 years old.
"""
import datetime
i = datetime.datetime.now()
name = raw_input("enter your name: ")
age = input("enter your age: ")
yr = int(i.year)
while age < 80:
    age += 1
    yr += 1
    if (age == 80):
        print '{0} will be {1} years old in {2}'.format(name,age,yr)
    else
        pass
"""

#3. Triangle of #

num_of_lines = 5
for i in range(1,num_of_lines+3,2):
    num_of_lines -= 1
    print ((" " * num_of_lines)+('#' *i))
 

