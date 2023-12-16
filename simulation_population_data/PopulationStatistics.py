#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:49:27 2023

@author: kieran
"""

import os
os.chdir('/Users/kieran/Desktop/simulation_population_data/')
import pandas as pd

#### Old functions that are already present in the main simulation script ####


#### New functions for population statistics analysis ####


def cleanGene(string):
    
    
    if len(string) == 11:
        
        string = string[2:10]
        
    elif len(string) == 12:
        
        string = string[3:11]
        
    elif len(string) == 13:
        
        string = string[2:10]
    
    else:
        print("Error, unknown gene format")
        
    return(string)



# Custom import of populations_spreadsheet
def readPopulationData2(filename):
    
    # Open file
    dictionary = {}
    file = open(filename)
    
    # Loop through the lines in the file
    for ln in file.readlines():
        
        # Quick removal of unused metadata
        ln = ln.strip()
        ln = ln.split(',')
        
        # Skip the header line
        if len(ln) == 6:
            continue
        
        # Isolate the creature's ID
        creature_id = ln[0]
        
        # Isolate the x coordinate
        x_coord = str(ln[1])
        x_coord = x_coord[3:len(x_coord)-1]
        
        # Isolate the y coordinate
        y_coord = str(ln[2])
        y_coord = y_coord[2:-3]
        
        # reGenerate the genomes
        genome = list()
        for g in ln[4:36]:
            
            # Clean each gene and add to the list
            genome.append(cleanGene(g))
        
        # Add all the data to an single dictionary entry
        entry = {'Coordinates':[x_coord,y_coord],
                 'Oscillator_period':int(ln[3]),
                 'Genome':genome,
                 'Age':int(ln[36]),
                 'status':ln[37]}
        
        # Add the individual's entry to a growing dictionary
        dictionary[creature_id] = entry
    return(dictionary)


output = readPopulationData2('0_populations.csv')
