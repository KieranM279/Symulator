#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:54:25 2023

@author: kieran
"""
import os
#os.chdir('/Users/kieran/Documents/Symulator/')
os.chdir('/home/kieran/Documents/Symulator/')

import pandas as pd
import random
import math
import matplotlib.pyplot as plt

#### Parameter declarations ####
## You can change these ##
parameters = {'GRID_SIZE' : 128,
              'POPULATION' : 100,
              'TICKS':3,
              
              'INTERNAL_NEURONS':3,
              'GENES':4}


#### Neurone dictionary ####


neurones = {
    'input':{'Age','Osc','TPo','LPo','BdE','BdW','BdN','BdS','NbD','BlE','BlW','BlS','BlN'},
    'output':{'MvN','MvE','MvS','MvW','MvR','SOsc'}
    }




## You probably don't want to change these ##
input_args = {}


#test


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


    
    
        
        
def UpdateField():
    pass

#### Inputs: These are the things that creatures can sense ####

# Calculated age based on tick
def Age(tick,total_ticks):
    
    Age = (tick/total_ticks)
    
    return(Age)

# Generate an oscillating sin wave based on tick
def Osc(tick,pop_dict,cr_id):
    
    osc_period = pop_dict[cr_id]['Oscillator_period']
    
    y = (math.sin(tick/osc_period) + 1)/2
    
    return(y)

def TPo(pop_dict):
    
    # Current population
    curr_pop = len(pop_dict.keys())
    # Generate output value
    output = (curr_pop / parameters['POPULATION'])
    
    return(output)

def LPo(pop_dict,cr_id,grid):
    
    # Isolate the coordinates of the individual
    Coords = pop_dict[cr_id]['Coordinates']
    
    # Generate the size of the immediate vicinity
    xmin = (Coord2Num(Coords[0]) - 3)
    xmax = (Coord2Num(Coords[0]) + 3)
    
    ymin = (Coord2Num(Coords[1]) - 3)
    ymax = (Coord2Num(Coords[1]) + 3)
    
    
    creature_list = list()
    
    # Loop through all the creatures
    for p in pop_dict.keys():
        
        # Skip if it is this creature
        if p == cr_id:
            continue
        
        # Isolate the other creatures coordinates
        other_coord = pop_dict[p]['Coordinates']
        other_x = Coord2Num(other_coord[0])
        other_y = Coord2Num(other_coord[1])
        
        if (other_x <= xmax and other_x >= xmin):
            
            if (other_y <= ymax and other_y >= ymin):
                
                creature_list.append(p)
    
    local_density = (len(creature_list) / 48)
    
    return(local_density)

## Calculate the distance from the borders
# East
def BdE(pop_dict,cr_id):
    
    # Isolate the coordinated of the creaure
    Coords = pop_dict[cr_id]['Coordinates']
    x = Coord2Num(Coords[0])
    
    # Calulate the distance from the border
    east_border = parameters['GRID_SIZE']
    border_distance = east_border - x
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/east_border)
    
    return(output)

# West
def BdW(pop_dict,cr_id):
    
    # Isolate the coordinated of the creaure
    Coords = pop_dict[cr_id]['Coordinates']
    x = Coord2Num(Coords[0])
    
    # Calulate the distance from the border
    west_border = 0
    border_distance = west_border + x
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/parameters['GRID_SIZE'])
    
    return(output)

# North
def BdN(pop_dict,cr_id):
    
    # Isolate the coordinated of the creaure
    Coords = pop_dict[cr_id]['Coordinates']
    y = Coord2Num(Coords[1])
    
    # Calulate the distance from the border
    north_border = parameters['GRID_SIZE']
    border_distance = north_border - y
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/north_border)
    
    return(output)

# South
def BdS(pop_dict,cr_id):
    
    # Isolate the coordinated of the creaure
    Coords = pop_dict[cr_id]['Coordinates']
    y = Coord2Num(Coords[1])
    
    # Calulate the distance from the border
    south_border = 0
    border_distance = south_border + y
    
    # Generate proportional output responce from the distance
    output = 1 - (border_distance/parameters['GRID_SIZE'])
    
    return(output)

# Nearest border distance
def NbD(pop_dict,cr_id):
    
    # Idenitify closest border distance
    dictionary = {BdS(pop_dict,cr_id):'South',
                  BdN(pop_dict,cr_id):'North',
                  BdE(pop_dict,cr_id):'East',
                  BdW(pop_dict,cr_id):'West'}
    
    listOfDist = [BdS(pop_dict,cr_id),
                  BdN(pop_dict,cr_id),
                  BdE(pop_dict,cr_id),
                  BdW(pop_dict,cr_id)]
    
    closest = max(listOfDist)
    closest = dictionary[closest]
    
    # Generate output for the nearest border distance
    if closest == 'North':
        output = BdN(pop_dict,cr_id)
        
    elif closest == 'South':
        output = BdS(pop_dict,cr_id)
        
    elif closest == 'East':
        output = BdE(pop_dict,cr_id)
    
    elif closest == 'West':
        output = BdW(pop_dict,cr_id)
    
    return(output)


# Detect a blockage to the East
def BlE(pop_dict,cr_id,grid):
    
    Coords = pop_dict[cr_id]['Coordinates']
    x = Coord2Num(Coords[0])
    
    east_edge = parameters['GRID_SIZE']
    
    i = 1
    
    while i < 5:
        
        if (x + i) >= east_edge:
            break
        
        if grid[Coords[1]][Num2Coord(x+i,'x')] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)

# Detect a blockage to the East
def BlN(pop_dict,cr_id,grid):
    
    Coords = pop_dict[cr_id]['Coordinates']
    y = Coord2Num(Coords[0])
    
    north_edge = parameters['GRID_SIZE']
    
    i = 1
    
    while i < 5:
        
        if (y + i) >= north_edge:
            break
        
        if grid[Num2Coord(y+i,'y')][Coords[0]] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    

# Detect a blockage to the West
def BlW(pop_dict,cr_id,grid):
    
    Coords = pop_dict[cr_id]['Coordinates']
    x = Coord2Num(Coords[0])
    
    west_edge = 0
    
    i = 1
    
    while i < 5:
        
        #print(i)
        
        if (x - i) < west_edge:
            break
        
        if grid[Coords[1]][Num2Coord(x-i,'x')] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    

# Detect a blockage to the West
def BlS(pop_dict,cr_id,grid):
    
    Coords = pop_dict[cr_id]['Coordinates']
    y = Coord2Num(Coords[1])
    
    south_edge = 0
    
    i = 1
    
    while i < 5:
        
        #print(i)
        
        if (y - i) < south_edge:
            break
        
        if grid[Num2Coord(y-i,'y')][Coords[0]] != '.':
            break
        
        i = i + 1
    
    output = 1-(i/5)
    
    return(output)
    
    


#### Outputs: These are the Actions that Each Creature can take ####

# Return a coordinate one north of the input coordinate
def MvN(Coords,grid,grid_size):
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # X coord remanes the same
    N_x = x
    
    # Increase the Y coord by one
    N_y = Coord2Num(y)
    N_y = N_y + 1
    N_y = Num2Coord(N_y, 'y')
    
    
    if (Coord2Num(N_y) > (grid_size-1)):
        return([x,y])
    elif grid[N_y][N_x] != '.':
        return([x,y])
    elif grid[N_y][N_x] == '.':
        return([N_x,N_y])
    else:
        print("Error in move north")
        return("help")

# Return a coordinate one south of the input coordinate
def MvS(Coords,grid,grid_size):
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # X coord remanes the same
    N_x = x
    
    # Decrease the Y coord by one
    N_y = Coord2Num(y)
    N_y = N_y - 1
    N_y = Num2Coord(N_y, 'y')
    
    
    if (Coord2Num(N_y) < 0):
        return([x,y])
    elif grid[N_y][N_x] != '.':
        return([x,y])
    elif grid[N_y][N_x] == '.':
        return([N_x,N_y])
    else:
        print("Error in move south")
        return("help")

# Return a coordinate one east of the input coordinate
def MvE(Coords,grid,grid_size):
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # Y coord remanes the same
    N_y = y
    
    # Increases the X coord by one
    N_x = Coord2Num(x)
    N_x = N_x + 1
    N_x = Num2Coord(N_x, 'x')
    
    
    if (Coord2Num(N_x) > (grid_size-1)):
        return([x,y])
    elif grid[N_y][N_x] != '.':
        return([x,y])
    elif grid[N_y][N_x] == '.':
        return([N_x,N_y])
    else:
        print("Error in move East")
        return("help")

# Return a coordinate one west of the input coordinate
def MvW(Coords,grid,grid_size):
    
    # The Current coordinates
    x = Coords[0]
    y = Coords[1]
    
    # Y coord remanes the same
    N_y = y
    
    # Decreases the X coord by one
    N_x = Coord2Num(x)
    N_x = N_x - 1
    N_x = Num2Coord(N_x, 'x')
    
    
    if (Coord2Num(N_x) < 0):
        return([x,y])
    elif grid[N_y][N_x] != '.':
        return([x,y])
    elif grid[N_y][N_x] == '.':
        return([N_x,N_y])
    else:
        print("Error in move West")
        return("help")

def MvR(Coords,grid,grid_size):
    
    my_list = [MvE, MvS, MvE, MvW]
    return(random.choice(my_list)(Coords,grid,grid_size))

def OmPh(pop_dict,cr_id):
    pass


def SOsc(cr_id,change):
    
    global population
    population[cr_id]['Oscillator_period'] = population[cr_id]['Oscillator_period'] + change


def weightGen():
    
    type_list = ['0','1']
    weight = ''
    
    for i in range(16):
        
        weight = weight + random.choice(type_list)
        
    return(weight)
#def GenomeGenerate():
#    
#    dictionary = {}
#    
#    
#    input_neurons = ['Age','Osc','TPo','LPo','BdE','BdW','BdN','BdS','NbD','BlE',
#                     'BlW','BlS','BlN']
#    
#    internal_neurons  = list(range(parameters['INTERNAL_NEURONS']))
#    
#    output_neurons = ['MvN','MvE','MvS','MvW','MvR','SOsc']
#    
#    type_list = [0,1]
#    
#    for p in population.keys():
#        
#        entry = {}
#        
#        for g in range(parameters['GENES']):
#            
#            source = random.choice(type_list)
#            sink = random.choice(type_list)
#            
#            if source == 0 and sink == 0:
#                
#                entry[g] = {'source_type':0,
#                            'source':random.choice(input_neurons),
#                            'sink_type':0,
#                            'sink':random.choice(internal_neurons),
#                            'weight':round(random.uniform(-4, 4),5)}
#                
#            elif source == 0 and sink == 1:
#                
#                entry[g] = {'source_type':0,
#                            'source':random.choice(input_neurons),
#                            'sink_type':1,
#                            'sink':random.choice(output_neurons),
#                            'weight':round(random.uniform(-4, 4),5)}
#                
#            elif source == 1 and sink == 0:
#                
#                entry[g] = {'source_type':1,
#                            'source':random.choice(internal_neurons),
#                            'sink_type':0,
#                            'sink':random.choice(internal_neurons),
#                            'weight':round(random.uniform(-4, 4),5)}
#            
#            elif source == 1 and sink == 1:
#                
#                entry[g] = {'source_type':1,
#                            'source':random.choice(internal_neurons),
#                            'sink_type':1,
#                            'sink':random.choice(output_neurons),
#                            'weight':round(random.uniform(-4, 4),5)}
#            
#        dictionary[p] = entry
#        
#    return(dictionary)
    
    
def GenomePrinter(cr_id,df):
    
    df = df[cr_id]
    
    genome = list()
    
    for g in df.keys():
        
        gene_list = list()
        for codo in df[g].values():
            gene_list.append(str(codo))
        
        gene = '|'.join(gene_list)
        
        genome.append(gene)
    
    genome = '\t'.join(genome)
    
    print(genome)
    

    
    

#### Environment creation ####

def FieldGen(grid_size):
    print("Generating empty world...")
    
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
    print("Populating world...")
    
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
                                       'Oscillator_period':10}
            
            # Add coordinate to checklist
            checklist.append([x,y])
            ite = (ite + 1)
    
    # Add the creatures to the grid
    for i in dictionary.keys():
        
        grid[dictionary[i]['Coordinates'][1]][dictionary[i]['Coordinates'][0]] = 'c'
    
    return(dictionary,grid)

#### Begin the simulation ###

# Generate an empty field in the physical world
field = FieldGen(parameters['GRID_SIZE'])

# Generate identical field in the pheromone field
pheromone_field = FieldGen(parameters['GRID_SIZE'])

population, field = Populate(field, 
                      parameters['GRID_SIZE'],
                      parameters['POPULATION'])

actions = [MvR]

def MainLoop():
    
    for t in range(parameters['TICKS']):
        
        for c in population.keys():
            
            # Isolate the current coordinate
            Coords = population[c]['Coordinates']
            
            # Generate the new Coordinates
            New_Coords = random.choice(actions)(Coords,field,parameters['GRID_SIZE'])
            
            # Update the Populations data
            population[c]['Coordinates'] = New_Coords
            
            # Update the Fields
            y = Coords[1]
            x = Coords[0]
            
            N_y = New_Coords[1]
            N_x = New_Coords[0]
            
            field[y][x] = '.'
            field[N_y][N_x] = 'c'
        
        filename_field = ('Outputs/' + str(t) + '_field.csv')
        filename_pop = ('Outputs/' + str(t) + '_populations.csv')
        getArray(field).to_csv(filename_field)
        getArray(population).to_csv(filename_pop)

MainLoop()


#test = GenomeGenerate()

#GenomePrinter('creature_0', test)

