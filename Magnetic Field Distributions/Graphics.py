# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:42:16 2020

@author: Thomas.Johnson

Utility methods related to graphics.

"""

import numpy as np

# for normalization
class CartesianExtents:
    def __init__(self):
        self.mag_min = np.finfo(np.float64).max
        self.mag_max = np.finfo(np.float64).min
        
        self.y_min = np.finfo(np.float64).max
        self.y_max = np.finfo(np.float64).min
        
        self.x_min = np.finfo(np.float64).max
        self.x_max = np.finfo(np.float64).max
        
        self.z_min = np.finfo(np.float64).max
        self.z_max = np.finfo(np.float64).max
        
    def SuggestExtent(self, r):
        mag = np.linalg.norm(r)
        x = r[0]
        y = r[1]
        z = r[2]
               
        
        if (mag > self.mag_max):
            self.mag_max = mag
        if (mag < self.mag_min):
            self.mag_min = mag        
    
        if (x > self.x_max):
            self.x_max = x
        if (x < self.x_min):
            self.x_min = x  
            
        if (y > self.y_max):
            self.y_max = y
        if (y < self.y_min):
            self.y_min = y

        if (z > self.z_max):
            self.z_max = z
        if (z < self.z_min):
            self.z_min = z    

def ColorFromOctant(vector, ext, colorSet, alphaReduction = 1):
    
    # select a color based on the octant a particular vector points to
    
    mag = np.linalg.norm(vector)
    x = vector[0]
    y = vector[1]
    z = vector[2]

    # normalize extents to a value between zero and one
    mag_norm = Normalize(mag, ext.mag_min, ext.mag_max)
    
    binaryNumber = str(int(x < 0))+str(int(y < 0))+str(int(z < 0))
    octant = int(binaryNumber,2)

    r = colorSet[octant,0]
    g = colorSet[octant,1]
    b = colorSet[octant,2]
    
    a = mag_norm/alphaReduction
    
    return (r,g,b,a)

def VibrantOctantColorSet():
    octantColorSet = np.zeros((8, 3))
    
    octantColorSet[0] = (1,0,0.482) # pink
    octantColorSet[1] = (0.816,0,1) # purple
    octantColorSet[2] = (0,0.282,1) # ocean blue
    octantColorSet[3] = (1,0.533,0) # deep orange
    octantColorSet[4] = (0,0.914,1) # light blue
    octantColorSet[5] = (0,1,0.082) # neon green
    octantColorSet[6] = (0.298,0.682,0) # terminal green
    octantColorSet[7] = (1,1,0) # hideous yellow
        
    return octantColorSet

def Normalize(val, val_min, val_max):
    return (val - val_min) / (val_max - val_min)
    