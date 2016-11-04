import string
#1. Try different ways to check for a palindrome

#(a). Take a string from user input and return True if palindrome

def is_palindrome(inp):
    rev =  ''.join(i for i in inp[::-1])
    if rev == inp:
        return True

inp= raw_input("enter a string: ") 
print is_palindrome(inp)



#(b). Take a list of words from user and return a list with palindrome words

def is_palindrome(inp_list):
    out_list = []
    for i in inp_list:
        rev = ''.join(j for j in i[::-1])
        if rev == i:
            out_list.append(i)
    print out_list


inp_list = map(str,raw_input("enter a list:").split(","))
is_palindrome(inp_list)


#(c) Take a string fronm user and return true for a palindrome with out using any in-built functions

def is_palindrome(inp):
    j = -1
    for i in range(len(inp)-1):
        if inp[i] == inp[j]:
            j += -1
        else:
            return False            
        return True
    
inp= raw_input("enter a string: ") 
print is_palindrome(inp)


#(d) Take a string and ingnore any punctuations or digits in word and check for a palindrome or not
def is_palindrome(inp):
        punc_dig = "!@#$%^&*()12345678910"
        inp = ''.join(i for i in inp if i not in punc_dig)
        rev_inp = inp[::-1]
        if rev_inp == inp:
            return True
        else:
            return False

inp= raw_input("enter a string: ") 
print is_palindrome(inp)
