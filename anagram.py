#Problem 1: Anagrams Enter a list of Strings and return a list of anagram strings. 
def anagrams(str_p,str_l):
    list_s = [ ]
    for i in str_l:
        if i == str_p:
            pass
        elif set(i).issubset(str_p):
            list_s.append(i)
    print list_s

def main():    
   str_p = "spot"
   str_l = ["tops","pots","spot","stop"]
 #  str_l = ["eat", "tea", "tan", "ate", "nat", "bat"]
 #   anagrams_strn(str_l)
    anagrams(str_p,str_l)
main()
 
#Problem 3: Given an unsorted integer array, find the first missing positive integer.
#For example,
#Given [1,2,0] return 3,and [3,4,-1,1] return 2.

#list_l = input("enter a list:")
def missing_int():
    list_l = [3,4,-1,1]
    list_l = [i for i in list_l if i >= 0]
    list_S = sorted(list(list_l))
    for i in range(len(list_l)+1):
        if list_S[i] < 0 :
            list_S[i].remove()      
        elif list_S[i+1] == list_S[i]+ 1:
            pass
        else:
            return list_S[i] + 1
            break

int_num = missing_int()
print int_num

#Problem 2: Given two integers n and k, return all possible combinations of k numbers out
#of 1 ... n.
#For example,If n = 4 and k = 2, a solution is:        
def combinations(n,k):
    for i in range(1,k+2):    
        for j in range(1,n+1):
            if i != j and i < j:
                print [i,j]

combinations(n=4,k=2)
