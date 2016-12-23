#Given a string, find the minimum number of characters to be inserted to convert it to palindrome.
#ab: Number of insertions required is 1. bab or aba
#aa: Number of insertions required is 0.



def substring():
    for i in range(len(inp)-1,-1,-1):
        word = outp[-1] + inp
        word2 = word[::-1] 
        if word2 == word:
            print "Number of insertions required is 2."
        
#        outp.insert(0,inp[i])
    


inp =  "ees"
outp = list(inp)
strn = inp[::-1]
if (strn == inp):
    print "number of insertions  required is 0"
elif len(inp) == 2:
#    word = outp[-1] + inp
    print "Number of insertions required is 1"
else:
    substring()


#for i in range(len(outp)-1,-1,-1):
#    print outp[i]
    

"""
for i in range(len(inp)-1,-1,-1):
    print i
    outp = inp[i] + outp
    print outp

"""

"""ex:
b ab
skee geeks

cb abc
"""
