#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:59:19 2023

@author: kieran
"""

# Script to test out pheromone radii

def radiiCalc(origin,r):
    
    x = origin[0]
    y = origin[1]
    
    # Calculate the 1st radius
    if r == 1:
        
        entry = [[x+1,y+1],[x-1,y-1],[x+1,y],[x-1,y],
                 [x-1,y-1],[x+1,y-1],[x,y+1],[x,y-1]]
        
    # Calculate the 2nd radius
    if r == 2:
        
        entry = [[x-1,y+2],[x,y+2],[x+1,y+2],[x-2,y+1],[x-2,y],[x-1,y-2],
                 [x-1,y-2],[x,y-2],[x+1,y-2],[x+2,y+1],[x+2,y],[x+2,y-1]]
        
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

