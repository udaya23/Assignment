
"""Given a number your task is to complete the function convertFive which takes an integer n as argument and replaces all zeros in the number n with 5 .
Your function should return the converted number ."""

inp = 1004
#inp = list(inp)
outp = [int(x) for x in str(inp)]
for i in range(len(outp)):
    if outp[i] == 0:
        outp[i] = 5
        
print outp
        
