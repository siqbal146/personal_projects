# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:17:17 2024

@author: Sadaf

Luhn algorithm:
    starting from first digit, double every other digit (double digits 1, 3, 5, etc.)
    if a doubled digit = 2 digits, then split it into it's 2 digits 
    (ie: 5 -> 10 -> 1, 0)
    add all digits together, they should be divisible by 10 (mod10 = 0)
example of a 'good' number: 4417 1234 5678 9113
"""

import sys #import system module

fail = "Invalid input, please try again." #defining fail output

ccnum_str = input("Enter your 16-digit credit card number: ") #get input from user
ccnum_new_str = ccnum_str.replace(" ","") #remove any spaces

#make sure input is valid
digits = sum(c.isdigit() for c in ccnum_str) #counts the number of digits in the input
if digits != 16: #if not a 16 digit number, then print fail output and exit program
    print (fail)
    sys.exit()

numeric_check = ccnum_new_str.isnumeric() #once spaces are removed, checks that all the inputs are numbers (no letters)
if not numeric_check: #if all inputs aren't numeric or spaces, then print fail output and exit program
    print (fail)
    sys.exit()

ccnum_array = list(ccnum_new_str) #turns string of numbers into a list
ccnum_array = [int(i) for i in ccnum_array] #converts every value from the list to an integer

#if everything passes, then time for math
i = 0 #start at first number in array (first number of credit card)
while i<16:
    ccnum_array[i] = ccnum_array[i]*2 #multiply every other number by 2
    if ccnum_array[i] > 9: #break up any 2 digit numbers (Luhn algorithm)
        ccnum_array[i] = ccnum_array[i] - 9 #example: 14 -> 1+4 (14-10 = 4, 4+1 = 5. same as 14-9.)
        #end if loop
    
    i += 2
    #end while loop

final_sum = sum(ccnum_array) #add all the numbers in the array, after all the other Luhn algorithm math is done
mod = final_sum % 10
if mod == 0:
    print ("Credit card number is valid :)")
else:
    print("Credit card number is not valid :(")