#Given a collection of numbers, return all possible permutations.
n = [1,2,3]

for i in n:
    for j in n:
        for k in n:
            if i != j and j !=k and k != i:
                print [i,j,k]
