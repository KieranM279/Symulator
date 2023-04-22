#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:54:25 2023

@author: kieran
"""
import os
os.chdir('/Users/kieran/Documents/Simulator')

import pandas as pd
import random

#### Parameter declarations ####

parameters = {'GRID_SIZE' : 10,
              'POPULATION' : 1,
              'TICKS':3}

#test


#### Useful functions ####

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

def UpdatePopulation(df, functions_list):
    
    for c in df.keys():
        
        df['Coordinates'] = MoveRandom(df['Coordinates'], field, parameters['GRID_SIZE'])
        
        
def UpdateField():
    pass




#### Outputs: These are the Actions that Each Creature can take ####

# Return a coordinate one north of the input coordinate
def MoveNorth(Coords,grid,grid_size):
    
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
def MoveSouth(Coords,grid,grid_size):
    
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
def MoveEast(Coords,grid,grid_size):
    
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
def MoveWest(Coords,grid,grid_size):
    
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

def MoveRandom(Coords,grid,grid_size):
    
    my_list = [MoveNorth, MoveSouth, MoveEast, MoveWest]
    return(random.choice(my_list)(Coords,grid,grid_size))

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
            dictionary[Creature_ID] = {'Coordinates':[x,y]}
            
            # Add coordinate to checklist
            checklist.append([x,y])
            ite = (ite + 1)
    
    # Add the creatures to the grid
    for i in dictionary.keys():
        
        grid[dictionary[i]['Coordinates'][1]][dictionary[i]['Coordinates'][0]] = 'c'
    
    return(dictionary,grid)

#### Begin the simulation ###

field = FieldGen(parameters['GRID_SIZE'])

population, field = Populate(field, 
                      parameters['GRID_SIZE'],
                      parameters['POPULATION'])


#for t in range(parameters['TICKS']) 




getArray(field).to_csv('field.csv')
