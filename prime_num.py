def prime_num(num):
#     num = 15
    for p in range(2,num+1):
        for i in range(2,p):
            if (p % i) == 0:
                break
        else:
            print p

num = int(input("enter your number: "))
prime_num(num)

