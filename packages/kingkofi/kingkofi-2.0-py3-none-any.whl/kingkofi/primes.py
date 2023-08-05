def show_primes(x, y):
    for num in range(x, y + 1):
        if num > 1: # all numbers greater than 1
            for i in range(2, num): # Don't forget 2; it's a prime number too!
                if (num % i) == 0: # if number is divisble by i...
                    break # Stop program
            else: # If not...
                print(num) # Display the number