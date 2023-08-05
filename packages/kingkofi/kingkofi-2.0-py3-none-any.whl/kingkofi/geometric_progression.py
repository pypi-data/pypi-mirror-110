def printGP(a, r, n):
    for i in range(0, n):
        curr_term = a * pow(r, i)
        print(curr_term, end=" ")

# a is starting number
# r is common ratio
# n is number of terms