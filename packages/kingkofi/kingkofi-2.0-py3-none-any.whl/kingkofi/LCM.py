def computeLCM(x, y):
    if x > y: # Choose the greater number
        greater = x
    else:
        greater = y
    
    while (True): # Loopin' time! :)
        if ((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1
    return lcm