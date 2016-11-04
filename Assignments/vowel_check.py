#2.Write a function that takes a character (i.e. a string of length 1) and returns True if it is a vowel, False otherwise.
#(a)

def vowel_checking():
    vowel = "aeiou"
    while True:
        inp = raw_input("enter a letter:")
        try:
             len(inp) == 1
             break
        except ValueError:
            print "Input entered is not suitable"
    
    if inp in vowel:
        return True
    else:
        return False

print vowel_checking()
 
