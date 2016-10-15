#1.the count of words in input
#2. count the word "words"

#import sys 
#words_in = sys.stdin.readlines()

words_in = raw_input("enter the words: ")
word_num = 0
in_words = sorted(str(words_in).split(" "))
count_of_words =len(in_words) 
word_num = [word_num+1 for i in in_words if i == "words"]
print "The word \"words\" is repeating {0} times in the sentence".format(len(word_num))
print "\nCount of words in the sentence you entered are {0}".format(count_of_words)

#3 each unique word, and the count of times it occurs in the input (listed in alphabetical order, each on its own line,
#  with a space between the word and count)

freq = [ ]
in_words_sort = sorted(in_words)

for i in in_words_sort:
    freq.append(in_words_sort.count(i))
dict_n = dict(zip(in_words_sort,freq))
for k,v in dict_n.items():
    print k, v


#5 alphabetically sorted letter count in the words.
"""
import string
letters = list(string.ascii_lowercase)
dict_i = dict.fromkeys(letters,0)
words = "four"
list_w = sorted(list(words))
for k in sorted(dict_i.items()):
    if k in list_w:
        dict_i[k] +=1
    else:
        dict_i[k]=0
#for k,v in dict_i.items():
#    print k,v    

"""   


"""Problem 2:

Given a non-negative integer num, repeatedly add all its digits until the
result has only one digit.
For example:
Given num = 89, the process is like: 8 + 9 = 17, 1 + 7 = 8. Since 2 has only
one digit, return it. """

num = 119
while len(str(num)) > 1:
    num = sum(map(int, str(num)))

print num

