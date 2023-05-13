#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:37:06 2023

@author: kieran
"""

# Script to test the funtion dictionary


import random
import math

number = 10

def squared(x):
    
    line = "The square of the number is: "
    
    y = x*x
    
    output = (line + str(y))
    
    print(output)
    
    
def cube(x):
    
    line = "The cube of the number is: "
    
    y = x*x*x
    
    output = (line + str(y))
    
    print(output)
    

def third(x):
    
    line = "One third of the number is: "
        
    y = x/3
        
    output = (line + str(y))
        
    print(output)


dictionary = {'s':squared,
              'c':cube,
              't':third}

my_list = ['s', 'c', 't']

for i in range(number):
    
    dictionary[random.choice(my_list)](4)