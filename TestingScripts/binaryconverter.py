#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:59:09 2023

@author: kieran
"""
import math

def rev(x):
    
    # If the input is a string
    if type(x) == str:
        new_out = ''
        
        # Loop through in reverse
        for i in range(1,len(x)+1):
            new_out = new_out + (x[-i])
        
    # If the input is a list
    if type(x) == list:
        new_out = list()
        
        # Loop through in reverse
        for i in range(1,len(x)+1):
            new_out.append(x[-i])
    
    return(new_out)


def BinDec(string):
    
    square_set = [1]
    output = 0
    
    # Generate the set of squares
    for i in range(1,len(str(string))):
        
        square_set.append(2**i)
    
    # Reverse the list of squares
    square_set = rev(square_set)
    
    # Generate the final value
    for d in range(len(string)):
        output = output + (int(string[d]) * int(square_set[d]))
    
    return(output)


def DecBin(x):
    
    output = ''
    
    while(x>0):
        
        # If the number odd
        if x%2 ==1:
            
            x = (x/2)-0.5
            output = output + '1'
        
        else:
        # If the number is even
            x = x/2
            output = output + '0'

    return(rev(output))


def BinHex(x):
    
    # Define the conversion dictionary
    dictionary = {
        '0000':'0','0001':'1','0010':'2','0011':'3','0100':'4','0101':'5',
        '0110':'6','0111':'7','1000':'8','1001':'9','1010':'A','1011':'B',
        '1100':'C','1101':'D','1110':'E','1111':'F'
        }
    
    # Initialise some temporary variables
    four_bit_list = list()
    four_bit = ''
    
    # Loop through the characters in the string
    for i in range(len(x)):
        
        # Add each character into the four bits
        four_bit = (four_bit + x[-i-1])
        
        # When four bits are together add to a list
        if len(four_bit) == 4:
            
            four_bit_list.append(rev(four_bit))
            four_bit = ''
        
        # Then add the remainder
        if i == (len(x)-1):
            
            four_bit_list.append(rev(four_bit))
    
    # Reverse the list
    four_bit_list = rev(four_bit_list)
    
    # Remove my mistakes
    if four_bit_list[0] == '':
        four_bit_list.remove('')
    
    if len(four_bit_list[0]) < 4:
        
        no_z2a = 4-len(four_bit_list[0])
        zeroes = ''
        
        for z in range(no_z2a):
            zeroes = zeroes + '0'
    
        four_bit_list[0] = zeroes + four_bit_list[0]
    
    hexadecimal = ''
    for h in range(len(four_bit_list)):
        
        hexadecimal = hexadecimal + dictionary[four_bit_list[h]]
        
    return(hexadecimal)



def HexBin(x):
    
    output = ''
    dictionary = {
        '0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101',
        '6':'0110','7':'0111','8':'1000','9':'1001','A':'1010','B':'1011',
        'C':'1100','D':'1101','E':'1110','F':'1111'
        }
    
    for i in range(len(x)):
        output = (output + dictionary[x[i]])
    
    return(output)





















