"""
Assignments on I/O :
Write a program that given a text file will create a new text file in which all the lines from the original file are numbered from 1 to n (where n is the number of lines in the file).
Write a program that will calculate the average word length of a text stored in a file (i.e the sum of all the lengths of the word tokens in the text, divided by the number of word tokens).
"""

"""
def counting_lines():
    lines = []
    filen = raw_input("enter the file name: ")
    fp = open(filen, "r")
    fd = open("opnum.txt", "w+")
    count = 0 
    for line in fp.read().split('\n'):
        lines.append(line)
    fp.close()


    for count,line in enumerate(lines):            
        fd.write(str(count+1) + " " +line)


counting_lines()

"""
