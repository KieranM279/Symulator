#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:54:25 2023

@author: kieran
"""
import os
#os.chdir('/Users/kieran/Documents/Symulator/')
os.chdir('C:/Users/Atlas/Desktop/Symulator/')



import pandas as pd
import random
import math
import matplotlib.pyplot as plt

#### Parameter declarations ####
## You can change these ##
parameters = {'GRID_SIZE' : 128,
              'POPULATION' : 100,
              'TICKS': 3,
              
              'INTERNAL_NEURONS': 3,
              'GENES': 8}


#### Neurone dictionary ####


neurones = {
    'input':['Age','Osc','TPo','LPo','BdE','BdW','BdN','BdS','NbD','BlE','BlW','BlS','BlN'],
    'output':['MvN','MvE','MvS','MvW','MvR','SOsc'],
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
def Age(creature_ID):
    
    Age = (population[creature_ID]['Age']/parameters['TICKS'])
    
    return(Age)

# Generate an oscillating sin wave based on tick
def Osc(creature_ID):
    
    osc_period = population[creature_ID]['Oscillator_period']
    
    y = (math.sin(population[creature_ID]['Age']/osc_period) + 1)/2
    
    return(y)

def TPo(creature_ID):
    
    # Current population
    curr_pop = len(population.keys())
    # Generate output value
    output = (curr_pop / parameters['POPULATION'])
    
    return(output)

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



neurone_f = {
    'input_f':{'Age':Age,'Osc':Osc,'TPo':TPo,'LPo':LPo,'BdE':BdE,
               'BdW':BdW,'BdN':BdN,'BdS':BdS,'NbD':NbD,'BlE':BlE,
               'BlW':BlW,'BlS':BlS,'BlN':BlN},
    'output_f':{'MvN':MvN,'MvE':MvE,'MvS':MvS,'MvW':MvW,'MvR':MvR,
                'SOsc':SOsc}
    }




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



def GenomeGen():
    
    pass

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

    
    
def GenomeCalculation(creature_ID):
    
    brain = {}
    
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
            node['sense_input'] = sense_input
            node['sense_weight'] = sense_weight
            node['sense_output'] = sense_output
            
            
            node['sense_target'] = gene_dict['output_ID']
            
            brain[g] = node
    
    # Secondly calulate the Intermediate neurones
    for g in population[creature_ID]['Genome']:
        
        if HexBin(g)[8] == '0':
            GeneInterpreter(g)
            
            

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
                                       'Oscillator_period':10,
                                       'Genome':GenomeCreate(parameters['GENES']),
                                       'Age':0}
            
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
            
            # Increase the creature's age by 1
            population[c]['Age'] += 1
            
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


def GlobalUpdateTest(x):
    
    global population
    population['creature_0']['Oscillator_period'] = x
    


GenomeCalculation('creature_0')

