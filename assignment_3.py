#1.the count of words in input
def count_words(str_in):
    freq = [ ]
    in_words = sorted(str(str_in).split(" "))
    count_of_words =len(in_words)
    print "Output:\n{}\nwords".format(count_of_words)
    for i in in_words:
        if i != " ":
            freq.append(in_words.count(i))
    dict_n = dict(zip(in_words,freq))
    for k,v in sorted(dict_n.items()):
        print k, v

#5 alphabetically sorted letter count in the words.
from collections import OrderedDict
import string
def count_alp(str_in):
    list_w = [ ]
    dict_i = OrderedDict()
    dict_i = dict_i.fromkeys(list(string.ascii_lowercase),0)
    for i in str_in:
        if i in dict_i.keys():
            dict_i[i] += 1
        else:
            dict_i[i] = 1
    for k,v in dict_i.items():
        print k,v

def main():
    str_in = raw_input("input:")
    count_words(str_in)

    count_alp(str_in)
main()

"""
Problem 2:

Given a non-negative integer num, repeatedly add all its digits until the
result has only one digit.
For example:
Given num = 89, the process is like: 8 + 9 = 17, 1 + 7 = 8. Since 2 has only
one digit, return it. 
"""
def sum_digits():
    num = 119
    while len(str(num)) > 1:
        num_i = sum(map(int, str(num)))
        return num_i

#num_i = sum_digits()

