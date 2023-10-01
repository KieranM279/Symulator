#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:54:25 2023

@author: kieran
"""
import os
#os.chdir('/Users/kieran/Documents/Symulator/')
os.chdir('C:/Users/Atlas/Desktop/Symulator/')
#os.chdir('/Users/kieran/Documents/Symulator/')

import time
import pandas as pd
import random
import math
import shutil
#from threading import Thread

#import matplotlib.pyplot as plt

#### TODO notes ####

# Complete the pheromone updater
# Add in the pheromone field creation for saved simualtions generations only


start = time.time()

#### Parameter declarations ####
## You can change these ##
def FindParameters(filename):
    
    dictionary = {}
    
    # Open the file
    file = open(filename)
    # Parse the contents
    for ln in file.readlines():
        ln = ln.split()
        
        # Process savde gemeration list
        if ln[0] == 'SAVED_GENERATIONS':
            new_list = list()
            
            # Remove the rubbish
            ln[1] = ln[1].strip('][')
            ln[1] = ln[1].split(',')
            # Convert to numeric
            for n in ln[1]:
                new_list.append(int(n))
            ln[1] = new_list
        # Process mutation rate floating point
        elif ln[0] == 'MUTATION_RATE':
            ln[1] = float(ln[1])
        # Conver to integer  
        else:
            ln[1] = int(ln[1])
        
        dictionary[ln[0]] = ln[1]
    return(dictionary)
        
    
parameters = FindParameters('parameters.txt')


#### Neurone dictionary ####


neurones = {
    'input':['Age','Osc','TPo','LPo','BdE','BdW','BdN','BdS','NbD','BlE','BlW','BlS','BlN',
             'SPhe','SPheN','SPheS','SPheE','SPheW'],
    'output':['MvN','MvE','MvS','MvW','MvR','SOsc','OmPh'],
    }



# Generates the required directories for the output
def DirMaker():
    
    # Delete directories of they exist
    if os.path.isdir('Outputs/'):
        shutil.rmtree('Outputs/')
    if os.path.isdir('frames/'):
        shutil.rmtree('frames/')
    
    # Remake the parent directories
    os.mkdir('Outputs/')
    os.mkdir('frames/')
    
    for g in parameters['SAVED_GENERATIONS']:
        
        os.mkdir('Outputs/Generation' + str(g))
        os.mkdir('frames/Generation' + str(g))
DirMaker()

# Calulates distance between two points
def diagDist(coords1,coords2):
    
    # Convert wierd coordinate format
    x1 = Coord2Num(coords1[0])
    y1 = Coord2Num(coords1[1])
    
    x2 = (coords2[0])
    y2 = (coords2[1])
    
    # Calculate x distances
    if x1 > x2 :
        x_dif = x1-x2
    elif x2 >= x1:
        x_dif = x2-x1
    # Calculate y distances
    if y1 > y2 :
        y_dif = y1-y2
    elif y2 >= y1:
        y_dif = y2-y1
    
    # Calculate the distance
    # This is slow
    distance = math.sqrt((x_dif**2)+(y_dif**2))
    
    return(distance)

#### Survival criteria ####

def Fate(creature_ID):
    
    # Where is the creature
    location = population[creature_ID]['Coordinates']
    x = Coord2Num(location[0])
    #y = Coord2Num(location[1])
    
    # Where should they be
    line = parameters['GRID_SIZE']/2
    
    # Outcome
    if x < line:
        return("Died")
    else:
        return('Survived')

def corner_fate(creature_ID):
    
    # Where is the creature
    location = population[creature_ID]['Coordinates']
    corners = [[0,0],[127,127],[0,127],[127,0]]
    
    fate = "Died"
    
    for d in corners:
        distan = diagDist(location,d)
        
        if distan <= 10:
            fate = 'Survived'
            break
    
    return(fate)


#### Useful functions ####

# Reverses lists and sequences
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


# Converts Binary strings to decimals
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

# Converts whole integer decimals to binry strings
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

# Convert a binary string to a hexadecimal
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


# Convert a hexadecimal to a binary string
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



# Export 2D Dictionary to '.csv'
def getArray(dictionary):

    data = pd.DataFrame.from_dict(dictionary)

    return(data.transpose())

## Manipulate coordinates
# Coord to num
def Coord2Num(Coord):
    
    # Identify prefix
    Prefix = Coord[0:2]
    # Remove prefix
    num = int(Coord.strip(Prefix))
    
    return(num)

def Num2Coord(num, axis):
    
    # Generate Coordinate format
    Coord = (axis + '_' + str(num))
    
    return(Coord)


    
    

#### Inputs: These are the things that creatures can sense ####

# Calculated age based on tick
def Age(creature_ID):
    
    Age = (population[creature_ID]['Age']/parameters['TICKS'])
    
    return(Age)

# Generate an oscillating sin wave based on tick
def Osc(creature_ID):
    
    osc_period = population[creature_ID]['Oscillator_period']
    
    y = (math.sin(population[creature_ID]['Age']/osc_period) + 1)/2
    
    return(y)

# Calculate the number of creatures in the total population
# Doesn't do anything until I allow the others to kill
def TPo(creature_ID):
    
    # Current population
    curr_pop = len(population.keys())
    # Generate output value
    output = (curr_pop / parameters['POPULATION'])
    
    return(output)

# Calculates the number of creatures in the immediate vicinity
def LPo(creature_ID):
    
    # Isolate the coordinates of the individual
    Coords = population[creature_ID]['Coordinates']
    
    # Generate the size of the immediate vicinity
    xmin = (Coord2Num(Coords[0]) - 3)
    xmax = (Coord2Num(Coords[0]) + 3)
    
    ymin = (Coord2Num(Coords[1]) - 3)
    ymax = (Coord2Num(Coords[1]) + 3)
    
    
    creature_list = list()
    
    # Loop through all the creatures
    for p in population.keys():
        
        # Skip if it is this creature
        if p == creature_ID:
            continue
        
        # Isolate the other creatures coordinates
        other_coord = population[p]['Coordinates']
        other_x = Coord2Num(other_coord[0])
        other_y = Coord2Num(other_coord[1])
        
        if (other_x <= xmax and other_x >= xmin):
            
            if (other_y <= ymax and other_y >= ymin):
                
                creature_list.append(p)
    
    local_density = (len(creature_list) / 48)
    
    return(local_density)

# Senses the pheromone density at the creatures current location
def SPhe(creature_ID):
    
    # Isolate the coordinates of the creature
    Coords = population[creature_ID]['Coordinates']
    # Convert coordinates to numeric values
    x = Coord2Num(Coords[0])
    y = Coord2Num(Coords[1])
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)

# Senses the pheromone density just north of the creature
def SPheN(creature_ID):
    
    # Isolate the coordinates of the creature
    Coords = population[creature_ID]['Coordinates']
    # Convert coordinates to numeric values
    x = Coord2Num(Coords[0])
    y = (Coord2Num(Coords[1]) + 1)
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)

# Senses the pheromone density just south of the creature
def SPheS(creature_ID):
    
    # Isolate the coordinates of the creature
    Coords = population[creature_ID]['Coordinates']
    # Convert coordinates to numeric values
    x = Coord2Num(Coords[0])
    y = (Coord2Num(Coords[1]) - 1)
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)

# Senses the pheromone density just east of the creature
def SPheE(creature_ID):
    
    # Isolate the coordinates of the creature
    Coords = population[creature_ID]['Coordinates']
    # Convert coordinates to numeric values
    x = (Coord2Num(Coords[0]) + 1)
    y = Coord2Num(Coords[1])
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)

# Senses the pheromone density just west of the creature
def SPheW(creature_ID):
    
    # Isolate the coordinates of the creature
    Coords = population[creature_ID]['Coordinates']
    # Convert coordinates to numeric values
    x = (Coord2Num(Coords[0]) - 1)
    y = Coord2Num(Coords[1])
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)


## Calculate the distance from the borders
# East
def BdE(creature_ID):
    
    # Isolate the coordinated of the creaure
    Coords = population[creature_ID]['Coordinates']
    x = Coord2Num(Coords[0])
    
    # Calulate the distance from the border
    east_border = parameters['GRID_SIZE']
    border_distance = east_border - x
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/east_border)
    
    return(output)

# West
def BdW(creature_ID):
    
    # Isolate the coordinated of the creaure
    Coords = population[creature_ID]['Coordinates']
    x = Coord2Num(Coords[0])
    
    # Calulate the distance from the border
    west_border = 0
    border_distance = west_border + x
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/parameters['GRID_SIZE'])
    
    return(output)

# North
def BdN(creature_ID):
    
    # Isolate the coordinated of the creaure
    Coords = population[creature_ID]['Coordinates']
    y = Coord2Num(Coords[1])
    
    # Calulate the distance from the border
    north_border = parameters['GRID_SIZE']
    border_distance = north_border - y
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/north_border)
    
    return(output)

# South
def BdS(creature_ID):
    
    # Isolate the coordinated of the creaure
    Coords = population[creature_ID]['Coordinates']
    y = Coord2Num(Coords[1])
    
    # Calulate the distance from the border
    south_border = 0
    border_distance = south_border + y
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/parameters['GRID_SIZE'])
    
    return(output)

# Nearest border distance
def NbD(creature_ID):
    
    # Idenitify closest border distance
    dictionary = {BdS(creature_ID):'South',
                  BdN(creature_ID):'North',
                  BdE(creature_ID):'East',
                  BdW(creature_ID):'West'}
    
    listOfDist = [BdS(creature_ID),
                  BdN(creature_ID),
                  BdE(creature_ID),
                  BdW(creature_ID)]
    
    closest = max(listOfDist)
    closest = dictionary[closest]
    
    # Generate output for the nearest border distance
    if closest == 'North':
        output = BdN(creature_ID)
        
    elif closest == 'South':
        output = BdS(creature_ID)
        
    elif closest == 'East':
        output = BdE(creature_ID)
    
    elif closest == 'West':
        output = BdW(creature_ID)
    
    return(output)


# Detect a blockage to the East
def BlE(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    x = Coord2Num(Coords[0])
    
    east_edge = parameters['GRID_SIZE']
    
    i = 1
    
    while i < 5:
        
        if (x + i) >= east_edge:
            break
        
        if field[Coords[1]][Num2Coord(x+i,'x')] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)

# Detect a blockage to the East
def BlN(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    y = Coord2Num(Coords[0])
    
    north_edge = parameters['GRID_SIZE']
    
    i = 1
    
    while i < 5:
        
        if (y + i) >= north_edge:
            break
        
        if field[Num2Coord(y+i,'y')][Coords[0]] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    

# Detect a blockage to the West
def BlW(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    x = Coord2Num(Coords[0])
    
    west_edge = 0
    
    i = 1
    
    while i < 5:
        
        #print(i)
        
        if (x - i) < west_edge:
            break
        
        if field[Coords[1]][Num2Coord(x-i,'x')] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    

# Detect a blockage to the West
def BlS(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    y = Coord2Num(Coords[1])
    
    south_edge = 0
    
    i = 1
    
    while i < 5:
        
        if (y - i) < south_edge:
            break
        
        if field[Num2Coord(y-i,'y')][Coords[0]] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    
    


#### Outputs: These are the Actions that Each Creature can take ####

# Return a coordinate one north of the input coordinate
def MvN(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    grid = field
    grid_size = parameters['GRID_SIZE']
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # X coord remanes the same
    N_x = x
    
    # Increase the Y coord by one
    N_y = Coord2Num(y)
    N_y = N_y + 1
    N_y = Num2Coord(N_y, 'y')
    
    # Fail to do anything
    if (Coord2Num(N_y) > (grid_size-1)):
        new_coords = [x,y]
        
    elif grid[N_y][N_x] != '.':
        new_coords = [x,y]
        
    # Actually update global variables
    elif grid[N_y][N_x] == '.':
        new_coords = [N_x,N_y]
        
    # Or just freak out
    else:
        print("Error in move north")
    
    return(new_coords)
    

# Return a coordinate one south of the input coordinate
def MvS(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    grid = field
    #grid_size = parameters['GRID_SIZE']
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # X coord remanes the same
    N_x = x
    
    # Decrease the Y coord by one
    N_y = Coord2Num(y)
    N_y = N_y - 1
    N_y = Num2Coord(N_y, 'y')
    
    
    # Fail to do anything
    if (Coord2Num(N_y) < 0):
        new_coords = [x,y]
        
    elif grid[N_y][N_x] != '.':
        new_coords = [x,y]
        
    # Actually update global variables
    elif grid[N_y][N_x] == '.':
        new_coords = [N_x,N_y]
        
    # Or just freak out
    else:
        print("Error in move south")
    
    return(new_coords)

# Return a coordinate one east of the input coordinate
def MvE(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    grid = field
    grid_size = parameters['GRID_SIZE']
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # Y coord remanes the same
    N_y = y
    
    # Increases the X coord by one
    N_x = Coord2Num(x)
    N_x = N_x + 1
    N_x = Num2Coord(N_x, 'x')
    
    # Fail to do anything
    if (Coord2Num(N_x) > (grid_size-1)):
        new_coords = [x,y]
        
    elif grid[N_y][N_x] != '.':
        new_coords = [x,y]
        
    # Actually update global variables
    elif grid[N_y][N_x] == '.':
        new_coords = [N_x,N_y]
        
    # Or just freak out
    else:
        print("Error in move east")
    
    return(new_coords)

# Return a coordinate one west of the input coordinate
def MvW(creature_ID):
    
    Coords = population[creature_ID]['Coordinates']
    grid = field
    #grid_size = parameters['GRID_SIZE']
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # Y coord remanes the same
    N_y = y
    
    # Decreases the X coord by one
    N_x = Coord2Num(x)
    N_x = N_x - 1
    N_x = Num2Coord(N_x, 'x')
    
    
    # Fail to do anything
    if (Coord2Num(N_x) < 0):
        new_coords = [x,y]
        
    elif grid[N_y][N_x] != '.':
        new_coords = [x,y]
        
    # Actually update global variables
    elif grid[N_y][N_x] == '.':
        new_coords = [N_x,N_y]
        
    # Or just freak out
    else:
        print("Error in move west")
    
    return(new_coords)

def MvR(creature_ID):
    
    my_list = [MvE, MvS, MvE, MvW]
    return(random.choice(my_list)(creature_ID))

def OmPh(creature_ID):
    
    global pheromone_pop
    
    # Generate an ID for the burst of pheromones
    # has to be uncapped and numeric
    if pheromone_pop == {}:
        burst_id = 0
    else:
        burst_id = (max(pheromone_pop.keys())+1)
        
    # Find the creatures coordinates
    creature_coord = population[creature_ID]['Coordinates']
    
    entry = {}
    # Generate the entry for the pheromone
    entry['origin'] = creature_coord
    entry['r'] = 1
    entry['creature_ID'] = creature_ID
    entry['conc'] = 1
    entry['cells'] = []
    
    pheromone_pop[burst_id] = entry
    
    return(creature_coord)



def SOsc(cr_id,change):
    
    global population
    population[cr_id]['Oscillator_period'] = population[cr_id]['Oscillator_period'] + change



neurone_f = {
    'input_f':{'Age':Age,'Osc':Osc,'TPo':TPo,'LPo':LPo,'BdE':BdE,
               'BdW':BdW,'BdN':BdN,'BdS':BdS,'NbD':NbD,'BlE':BlE,
               'BlW':BlW,'BlS':BlS,'BlN':BlN,'SPhe':SPhe,
               'SPheN':SPheN,'SPheS':SPheS,'SPheE':SPheE,'SPheW':SPheW},
    'output_f':{'MvN':MvN,'MvE':MvE,'MvS':MvS,'MvW':MvW,'MvR':MvR,
                'SOsc':SOsc,'OmPh':OmPh}
    }



#### These functions are needed to the general running of the simulation ####

# This calculates the cell for each pheromone radius
def radiiCalc(origin,r):
    
    # Isolate the coordinates
    x = origin[0]
    y = origin[1]
    # Convert the coordinate to a numeric value
    x = Coord2Num(x)
    y = Coord2Num(y)
    
    # Calculate the 1st radius
    if r == 1:
        
        entry = [[x+1,y+1],[x-1,y-1],[x+1,y],[x-1,y],
                 [x-1,y+1],[x+1,y-1],[x,y+1],[x,y-1]]
        
    # Calculate the 2nd radius
    if r == 2:
        
        entry = [[x-1,y+2],[x,y+2],[x+1,y+2],[x-2,y+1],[x-2,y],[x-1,y-2],
                 [x-2,y-1],[x,y-2],[x+1,y-2],[x+2,y+1],[x+2,y],[x+2,y-1]]
        
    # Calculate the 3rd radius
    if r == 3:
        
         entry = [[x+3,y+1],[x+3,y-1],[x-3,y+1],[x-3,y-1],[x+3,y],[x-3,y],
                  [x+1,y+3],[x-1,y+3],[x+1,y-3],[x-1,y-3],[x,y+3],[x,y-3],
                  [x+2,y+2],[x+2,y-2],[x-2,y+2],[x-2,y-2]]
         
    # Calculate the 4th radius
    if r == 4: 
        
        entry = [[x+4,y+2],[x+4,y+1],[x+4,y-1],[x+4,y-2],[x+4,y],
                 [x-4,y+2],[x-4,y+1],[x-4,y-1],[x-4,y-2],[x-4,y],
                 [x+2,y+4],[x+1,y+4],[x-1,y+4],[x-2,y+4],[x,y+4],
                 [x+2,y-4],[x+1,y-4],[x-1,y-4],[x-2,y-4],[x,y-4],
                 [x+3,y+3],[x+3,y-3],[x-3,y+3],[x-3,y-3],
                 [x+2,y+3],[x+3,y+2],[x+2,y-3],[x+3,y-2],
                 [x-2,y+3],[x-3,y+2],[x-3,y-2],[x-2,y-3]]
        
    # Calculate the 5th radius
    if r == 5:
        
        entry = [[x+5,y+2],[x+5,y+1],[x+5,y-1],[x+5,y-2],[x+5,y],
                 [x-5,y+2],[x-5,y+1],[x-5,y-1],[x-5,y-2],[x-5,y],
                 [x+2,y+5],[x+1,y+5],[x-1,y+5],[x-2,y+5],[x,y+5],
                 [x+2,y-5],[x+1,y-5],[x-1,y-5],[x-2,y-5],[x,y-5],
                 [x+4,y+3],[x+3,y+4],[x-3,y-4],[x-4,y-3],
                 [x+4,y-3],[x+3,y-4],[x-4,y+3],[x-3,y+4]]
        
    return(entry)

# Calculates the pheromone concentration at the requested coordinate
def modified_SPhe(Coords):
    
    # Isolate the coordinates of the creature
    Coords = Coords
    # Convert coordinates to numeric values
    x = Coord2Num(Coords[0])
    y = Coord2Num(Coords[1])
    coords = [x,y]
    
    concentration_list = list()
    
    # Loop through all the pheromone bursts
    for b in pheromone_pop.keys():
        
        # If the current cell is within a burst
        if coords in pheromone_pop[b]['cells']:
            
            # Add its concentration to a growing list
            concentration_list.append(pheromone_pop[b]['conc'])
    
    # Sum all the concentrations together
    phe = sum(concentration_list)
    
    # Set max concentration to 1
    if phe > 1:
        phe = 1
    
    return(phe)


def pheromone_update2(gen):
    
    # Import the global pheromone dictionary
    global pheromone_pop
    
    # key = radius, value = concentration
    conc_conv_dict = {1:1, 2:0.8, 3:0.6, 4:0.4, 5:0.2, 6:0}
    # Loop through the bursts that have been added to the dictionary
    for b in list(pheromone_pop.keys()):
        
        # Generate the grid cells that have a pheromone in them
        pheromone_pop[b]['cells'] = radiiCalc(pheromone_pop[b]['origin'], 
                                              pheromone_pop[b]['r'])
         # Increase the redius by 1
        pheromone_pop[b]['r'] += 1
        
         # Update the concentration
        pheromone_pop[b]['conc'] = conc_conv_dict[pheromone_pop[b]['r']]
        
        # Radius must not exceed 6
        if pheromone_pop[b]['r'] == 6:
            pheromone_pop.pop(b)
    
    # For the saved generations
    if gen in parameters['SAVED_GENERATIONS']:
        
        # Import the global pheromone field
        global pheromone_field
        # Replace it almost immediately
        pheromone_field = FieldGen(parameters['GRID_SIZE'])
        
        # Loop through the y coordinates of the pheromone field
        for fy in pheromone_field.keys():
            # Loop through the x coordinates of the pheromone field
            for fx in pheromone_field[fy].keys():
                
                # Calculate the pheromone concentration for the current coordinates
                pheromone_field[fy][fx] = modified_SPhe([fx,fy])
                


# This function creates the first randomly generated genome for 
def GenomeCreate(gene_num):
    
    genome = list()
    
    # Do this for every gene in the genome
    for i in range(gene_num):
        
        gene = ''
        options = ['0','1']
        
        for b in range(0,32,1):
            
            gene = gene + random.choice(options)
        
        genome.append(BinHex(gene))
    
    return(genome)

# Just a function to print the genome is a convenient way
def GenomePrinter(genome):
    
    counter = 0
    line = ''
    for i in genome:
        
        counter += 1
        line = line + i + ' '
        
        # Print every fourth line
        if counter == 4:
            print(line)
            counter = 0
            line = ''
        # Print the remiander
        if i == genome[-1]:
            print(line)

def WeightInterpreter(string):
    
    weight = (-4 + (8*(BinDec(string)/65535)))
    
    return(weight)

def GeneInterpreter(gene):
    
    print("==========================================")
    print(gene)
    gene = HexBin(gene)
    print(gene[0] + ' ' + gene[1:8] + ' '+ gene[8] + ' ' + gene[9:16] + ' ' + gene[16:32])
    gene_dict = {}
    
    # Generate the ratio for the inoput and outputs
    source_ratio = int(BinDec(gene[1:8]))/127
    output_ratio = int(BinDec(gene[9:16]))/127
    
    # Identify the input neurone
    if gene[0] == '0':
        
        gene_dict['source'] = 'Sensory neurone'
        source_index = round(source_ratio * (len(neurones['input'])-1))
        source_ID = neurones['input'][source_index]
        
    elif gene[0] == '1':
        
        gene_dict['source'] = 'Internal neurone'
        source_index = round(source_ratio * (parameters['INTERNAL_NEURONS']-1))
        source_ID = source_index
        
    # Identify the output neurone
    if gene[8] == '0':
        
        gene_dict['output'] = 'Internal neurone'
        output_index = round(output_ratio * (parameters['INTERNAL_NEURONS']-1))
        output_ID = output_index
    elif gene[8] == '1':
        
        gene_dict['output'] = 'Action neurone'
        output_index = round(output_ratio * (len(neurones['output'])-1))
        output_ID = neurones['output'][output_index]
    
    gene_dict['source_ID'] = source_ID
    gene_dict['output_ID'] = output_ID
    
    gene_dict['weight'] = WeightInterpreter(gene[16:32])
    
    print("------------------------------------------")
    print(gene_dict['source'] + ': ' + str(gene_dict['source_ID']))
    print(gene_dict['output'] + ': ' + str(gene_dict['output_ID']))
    print('Weight: ' + str(gene_dict['weight']))

def GenePCInterpreter(gene):
    
    gene = HexBin(gene)
    gene_dict = {}
    
    # Generate the ratio for the inoput and outputs
    source_ratio = int(BinDec(gene[1:8]))/127
    output_ratio = int(BinDec(gene[9:16]))/127
    
    # Identify the input neurone
    if gene[0] == '0':
        
        gene_dict['source'] = 'Sensory neurone'
        source_index = round(source_ratio * (len(neurones['input'])-1))
        source_ID = neurones['input'][source_index]
        
    elif gene[0] == '1':
        
        gene_dict['source'] = 'Internal neurone'
        source_index = round(source_ratio * (parameters['INTERNAL_NEURONS']-1))
        source_ID = source_index
        
    # Identify the output neurone
    if gene[8] == '0':
        
        gene_dict['output'] = 'Internal neurone'
        output_index = round(output_ratio * (parameters['INTERNAL_NEURONS']-1))
        output_ID = output_index
    elif gene[8] == '1':
        
        gene_dict['output'] = 'Action neurone'
        output_index = round(output_ratio * (len(neurones['output'])-1))
        output_ID = neurones['output'][output_index]
    
    gene_dict['source_ID'] = source_ID
    gene_dict['output_ID'] = output_ID
    
    gene_dict['weight'] = WeightInterpreter(gene[16:32])
    
    return(gene_dict)


# Iterates the gene printer over an entire creatues genome
def GenomeReader(creature_ID):
    
    for i in population[creature_ID]['Genome']:
        
        GeneInterpreter(i)

def Gene_Checker(creature_ID):
    
    output_list = list()
    direction_list = list()
    
    for g in population[creature_ID]['Genome']:
        
        # Generate gene dictionary
        gene_dict = GenePCInterpreter(g)
        
        # If there connection is between 2 internal neurones
        if gene_dict['source'] == gene_dict['output']:
            
            # If the connection is between the same neurone
            if (gene_dict['source_ID'] == gene_dict['output_ID']):
                output_list.append(g)
            else:
                
                direction = [gene_dict['source_ID'],gene_dict['output_ID']]
                
                # If reverse direction in direcion list
                if rev(direction) in direction_list:
                    output_list.append(g)
                else:
                    direction_list.append(direction)
    
    return(output_list)

def stat_updater(df,pheromone_df,gen):
    
    global stats
    
    entry = {'Survived':0,
             'Died':0}
    
    for i in df.keys():
        
        entry[df[i]['status']] += 1
    
    bursts = 0
    
    for b in pheromone_df.keys():
        
        if pheromone_df[b]['r'] == 1:
            
            bursts +=1
    
    entry['emisions'] = bursts
    
    stats[gen] = entry
    
    
    
def ready_checker(creature_ID):
    
    dictionary = {}
    # Create a dictionry to mark if an internal neurone is ready
    for internal in range(parameters['INTERNAL_NEURONS']):
        dictionary[internal] = {'status':'nope','input_check':list()}
        
        
    for g in population[creature_ID]['Genome']:
        
        gene_dict = GenePCInterpreter(g)
        
        if((gene_dict['output'] == 'Internal neurone') and
           (gene_dict['source'] == 'Internal neurone')):
            
            
            dictionary[gene_dict['source_ID']]['input_check'].append(1)
    
    for int_gene in dictionary.keys():
        
        if sum(dictionary[int_gene]['input_check']) == 0:
            
            dictionary[int_gene]['status'] = 'Yes'
    return(dictionary)
    
def DecisionMaker(df):
    
    what_am_i_doing = list()
    
    # Loop through calculated action neurones
    for i in df.keys():
        
        if df[i] <= 0:
            continue
        else:
            
            # Generate the chances of success or failure
            success_multiplier = (round(df[i]*1000))
            failure_multiplier = 1000 - success_multiplier
            
            option_list = (['yes']*success_multiplier) + (['no']*failure_multiplier)
            
            # Genreate the final choice
            outcome = random.choice(option_list)
            
            if outcome == 'no':
                continue
            else:
                what_am_i_doing.append(i)
    
    return(what_am_i_doing)
            

def GenomeCalculation(creature_ID):
    
    brain = {}
    gene_skip = Gene_Checker(creature_ID)
    
    # First calculate the action potential of all of the inputs
    for g in population[creature_ID]['Genome']:
        
        if HexBin(g)[0] == '0':
            
            node = {}
            
            #GeneInterpreter(g)
            gene_dict = GenePCInterpreter(g)
            
            # Calculate the strength of the sensory neurones action potential
            sense_input =  neurone_f['input_f'][gene_dict['source_ID']](creature_ID)
            sense_weight = gene_dict['weight']
            sense_output = sense_input * sense_weight
            
            # Save the output and the calculation to a dictionary
            node['node_input'] = sense_input
            node['node_weight'] = sense_weight
            node['node_output'] = sense_output
            
            
            node['node_target'] = gene_dict['output_ID']
            
            brain[g] = node
    
    # Import a dictionary of ready neurones
    ready_dict = ready_checker(creature_ID)

    
    
    # Second pass: Intermediate neurones with only sense inputs
    for g in population[creature_ID]['Genome']:
        
        # Skip the useless genes
        if g in gene_skip:
            continue
        
        # If the source is an intermediate neurone
        if HexBin(g)[0] == '1':
            
            gene_dict = GenePCInterpreter(g)
            
            # If the gene is ready to be calculated
            if ready_dict[gene_dict['source_ID']]['status'] == 'Yes':
                
                in_list_p1 = list()
                
                # Search the brain for inputs
                for b in brain.keys():
                    
                    # Find the relevent inputs from the already calculated genes
                    if brain[b]['node_target'] == gene_dict['source_ID']:
                        in_list_p1.append(brain[b]['node_output'])
                        
                node = {}
                node['node_input'] = math.tanh(sum(in_list_p1))
                node['node_weight'] = gene_dict['weight']
                node['node_output'] = node['node_input'] * node['node_weight']
                node['node_target'] = gene_dict['output_ID']
                
                brain[g] = node
    
    
    
    # Third pass: Intermediate neurones with only sense inputs
    for g in population[creature_ID]['Genome']:
        
        # Skip the useless genes
        if g in gene_skip:
            continue
        
        # If the source is an intermediate neurone
        if HexBin(g)[0] == '1':
            
            gene_dict = GenePCInterpreter(g)
            
            # If was previously not ready to be calculated (It should be now)
            if ready_dict[gene_dict['source_ID']]['status'] == 'nope':
                
                in_list_p2 = list()
                
                # Search the brain for inputs
                for b in brain.keys():
                    
                    # Find the relevent inputs from the already calculated genes
                    if brain[b]['node_target'] == gene_dict['source_ID']:
                        in_list_p2.append(brain[b]['node_output'])
                        
                node = {}
                node['node_input'] = math.tanh(sum(in_list_p2))
                node['node_weight'] = gene_dict['weight']
                node['node_output'] = node['node_input'] * node['node_weight']
                node['node_target'] = gene_dict['output_ID']
                
                brain[g] = node
    
    action_list = list()
    # Fourth pass: The Actions neurones
    
    # Make a list of the actions that the creature has access to
    for g in population[creature_ID]['Genome']:
        
        if HexBin(g)[8] == '1':
            gene_dict = GenePCInterpreter(g)
            
            if gene_dict['output_ID'] in action_list:
                continue
            
            action_list.append(gene_dict['output_ID'])
    
    # Make a dictionary of all the final choices the that the creature can make
    # Dictionary of action neurones and final weighting
    choice_dict = {}
    
    for a in action_list:
        
        action_in_list = list()
        
        for b in brain.keys():
            
            if brain[b]['node_target'] == a:
                action_in_list.append(brain[b]['node_output'])
    
        choice_dict[a] = math.tanh(sum(action_in_list))
    
    #print(choice_dict)
    
    what_am_i_doing = DecisionMaker(choice_dict)
    
    return(what_am_i_doing)

def mutate(genome):
    
    rate = parameters['MUTATION_RATE']
    df = {"0":"1","1":"0"}
    choice = ['yes','no']

    # Loop through the length of the genome
    for g in range(len(genome)):
        
        gene = HexBin(genome[g])
        new_gene = ''
        
        # Loop through each base
        for b in gene:
            
            # Decide if base will change
            outcome = random.choices(choice,
                                     weights = [rate,(1-rate)],
                                     k=1)
            
            # Insert new base
            if outcome == ['no']:
                new_gene = new_gene + b
            elif outcome == ['yes']:
                new_gene = new_gene + df[b]
        
        # Insert new gene
        genome[g] = BinHex(new_gene)

    return(genome)




#### Environment creation ####

def FieldGen(grid_size):
    
    dictionary = {}
    for y in range(grid_size):
        
        y_coord = ('y_'+str(y))
        
        entry = {}
        for x in range(grid_size):
            
            x_coord = ('x_'+str(x))
            entry[x_coord] = "."
            
        dictionary[y_coord] = entry
        
    return(dictionary)


#### Populate the world ####

def Populate(grid, grid_size, n):
    
    dictionary = {}
    checklist = list()
    ite = 0
    
    # Loop until population reaches chosen size
    while(len(dictionary.keys()) < n):
        
        # Generate the ID for the creature
        Creature_ID = ('creature_' + str(ite))
        
        # Generate the coordinates of the creature
        x = random.randrange(0,grid_size,1)
        y = random.randrange(0,grid_size,1)
        # Modify coordinate format
        x = Num2Coord(x,'x')
        y = Num2Coord(y,'y')
        
        # As long as location is not populated
        if [x,y] not in checklist:
            
            # Add creature to population dictionary
            dictionary[Creature_ID] = {'Coordinates':[x,y],
                                       'Oscillator_period':10,
                                       'Genome':GenomeCreate(parameters['GENES']),
                                       'Age':0,
                                       'status':'unconfirmed'}
            
            # Add coordinate to checklist
            checklist.append([x,y])
            ite = (ite + 1)
    
    # Add the creatures to the grid
    for i in dictionary.keys():
        
        grid[dictionary[i]['Coordinates'][1]][dictionary[i]['Coordinates'][0]] = 'c'
    
    return(dictionary,grid)

#### Begin the simulation ###

print("Generating empty world...")
# Generate an empty field in the physical world
field = FieldGen(parameters['GRID_SIZE'])

# Generate identical field in the pheromone field
pheromone_field = FieldGen(parameters['GRID_SIZE'])
pheromone_pop = {}

print("Populating world...")
population, field = Populate(field, 
                      parameters['GRID_SIZE'],
                      parameters['POPULATION'])

# Just a place holder for the stats dictionary
stats = {}

def gen_sim(gen):
    
    global population
    global field
    print("=================================================================")
    print("Simulating generation: " +str(gen))
    for t in range(parameters['TICKS']):
        
        if t%20 == 0:
            print(t)
            
            
        # Update the pheromone field
        pheromone_update2(gen)
        
        
        for c in population.keys():
            
            # Increase the creature's age by 1
            population[c]['Age'] += 1
            
            # Calculate what the creature is going to do
            action_list = GenomeCalculation(c)
            
            # If there are any actions to carry out
            if len(action_list) > 0:
                
                # Loop through the actions
                for a in action_list:
                    
                    old_coordinates = population[c]['Coordinates']
                    
                    if a == 'SOsc':
                       neurone_f['output_f'][a](c,1)
                       continue
                   
                    # Call the actual action function
                    new_coordinates = neurone_f['output_f'][a](c)
                    
                    # Update the grid
                    field[old_coordinates[1]][old_coordinates[0]] = '.'
                    field[new_coordinates[1]][new_coordinates[0]] = 'c'
                    
                    population[c]['Coordinates'] = new_coordinates
        
        # This function selectively kills the creatures
        Death()
        
        if gen in parameters['SAVED_GENERATIONS']:
            filename_field = ('Outputs/Generation'+ str(gen) +'/'+ str(t) + '_field.csv')
            filename_pop = ('Outputs/Generation'+ str(gen) +'/'+ str(t) + '_populations.csv')
            filename_pheromone = ('Outputs/Generation'+ str(gen) +'/'+ str(t) + '_pheromone.csv')
            getArray(field).to_csv(filename_field)
            getArray(population).to_csv(filename_pop)
            getArray(pheromone_field).to_csv(filename_pheromone)



def Death():
    
    # Import the real population
    global population
    
    # Update the fate of all the creatures
    for c in population.keys():
        population[c]['status'] = Fate(c)
    

def Inheritance():
    
    global population
    global field
    
    new_population, new_field = Populate(FieldGen(parameters['GRID_SIZE']), 
                          parameters['GRID_SIZE'],
                          parameters['POPULATION'])
    
    survived_list = list()
    # Loop though the whole populations
    for c in population.keys():
        # Note the ones who survived
        if population[c]['status'] == 'Survived':
            survived_list.append(c)
    
    # Loop through the new population
    for b in new_population.keys():
        
        # Choose two new parents
        cr_parents = random.sample(survived_list,2)
        cr_id_a = cr_parents[0]
        cr_id_b = cr_parents[1]
        
        # Comine the parent genomes
        genome_soup = population[cr_id_a]['Genome'] + population[cr_id_b]['Genome']
        
        # Generate the new offspring's genome
        new_genome = random.sample(genome_soup,parameters['GENES'])
        
        new_genome = mutate(new_genome)
        
        # Give it to the new creature
        new_population[b]['Genome'] = new_genome
    
    population = new_population
    field = new_field
        
    
    
    

def Simulation():
    
    for g in range(parameters['GENERATIONS']):
        
        # This simulates one generation
        gen_sim(g)
        
        # Will update the stat dictionary
        stat_updater(population, pheromone_pop, g)
        
        # Create the new generation
        Inheritance()
        
        if g%100 == 0:
            temp_filename = ('Outputs/gen'+str(g)+'_stat_summary.csv')
            getArray(stats).to_csv(temp_filename)
    
    getArray(stats).to_csv('Outputs/stat_summary.csv')
    

Simulation()

#def print_1000():
#    
#    for i in range(100000):
#        print(i)

#def print_hello():
#    
#    for i in range(100000):
#        print("hello")
#
#print_1000()

#t1 = Thread(target=print_1000)
#t2 = Thread(target=print_hello)
#t1.start()
#t2.start()

end = time.time()

print("Time ellapsed:" + str(end-start) + ' seconds')