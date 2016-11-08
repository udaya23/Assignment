#1.
import collections
def count_l(inp):
    list_p = []
    count = []
    for i in range(0,len(inp)):
       list_p.append(inp[i])
    d = collections.OrderedDict.fromkeys(list_p,0)
    for i in range(0,len(list_p)):
            temp = list_p[i]
            if temp not in d.keys():
                d[temp] =0
            else:
                d[temp] +=1
    print d
           
        
inp = raw_input("enter ur string:")
count_l(inp)


#2. A pangram is a sentence that contains all the letters of the English alphabet at least once, for example: The quick brown fox jumps over the lazy dog. Your task here is to write a function to check a sentence to see if it is a pangram or not.

def pangram(phrase):
    alp = "abcdefghijklmnopqrstuvwxyz"
    letters = ""
    for c in phrase:
        if c in alp:
            letters += c
    for i in letters:
        if i not in alp:
            pass
    return True


phrase = "The quick brown fox jumps over the lazy dog"    
print pangram(phrase)       

    
#3.Using the higher order function reduce(), write a function max_in_list() that takes a list of numbers and returns the largest one.



def max_in_list():
    list_l = [2,43,65,7,9]
    temp = list_l[0]
    for i in range(1,len(list_l)-1):
        if temp < list_l[i]:
            temp = list_l[i]
    print temp
        
        
#using reduce
   
max_in_list()








    
