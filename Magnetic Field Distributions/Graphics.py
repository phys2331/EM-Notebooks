# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:42:16 2020

@author: Thomas.Johnson
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
                
def ColorFromCartesian(r, ext, alphaReduction = 1):
    mag = np.linalg.norm(r)
    x = r[0]
    y = r[1]
    z = r[2]

    # normalize extents to a value between zero and one
    mag_norm = Normalize(mag, ext.mag_min, ext.mag_max)
    x_norm = Normalize(x, ext.x_min, ext.x_max)
    y_norm = Normalize(y, ext.y_min, ext.y_max)
    z_norm = Normalize(z, ext.z_min, ext.z_max)
        
    sum_norm = y_norm + x_norm + z_norm
    
    r = y_norm
    g = x_norm    
    b = z_norm
    
    a = mag_norm/alphaReduction
    
    return (r,g,b,a)

def Normalize(val, val_min, val_max):
    return (val - val_min) / (val_max - val_min)
    