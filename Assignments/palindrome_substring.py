#Given a string, find the minimum number of characters to be inserted to convert it to palindrome.
#ab: Number of insertions required is 1. bab or aba
#aa: Number of insertions required is 0.

inp =  "geeks"
outp = inp
for i in range(len(inp)-1,-1,-1):
    print i
    outp = inp[i] + outp
    print outp

"""
ex:
b ab
skee geeks

cb abc
"""
