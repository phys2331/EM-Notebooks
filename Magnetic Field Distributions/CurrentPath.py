# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:30:00 2020

@author: Thomas.Johnson

Creates arrays of 3D positions that approximate common geometric paths. 
Iterating over the array is like following a path of current.
"""

import numpy as np
import sympy as sp

class Line:
    def __init__(self, length, dl):        
                
        # todo: just use linspace?
        
        self.stepCount = int(length/dl)+1
        xshift = int(self.stepCount/2)
        
        self.path = np.zeros((self.stepCount, 3))

        self.xmin = -xshift*dl
        self.xmax = xshift*dl
        self.ymin = 0
        self.ymax = 0
        self.zmin = 0
        self.zmax = 0
        
        for i in range(0, self.stepCount):
            self.path[i] = ((i-xshift)*dl,0,0)
        
class Loop:
    def __init__(self, r, dtheta):

        self.stepCount = int((2*sp.pi)/dtheta) + 1
        self.path = np.zeros((self.stepCount, 3))               
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0        
        self.zmin = 0
        self.zmax = 0
        
        for i in range(0, self.stepCount):
            theta = (2 * i * sp.pi) / (self.stepCount-1)     
            x = r*sp.cos(theta)
            y = r*sp.sin(theta)
            
            self.path[i] = (x, y, 0)
            
            if (x > self.xmax):
                self.xmax = x
            if (x < self.xmin):
                self.xmin = x
            if (y > self.ymax):
                self.ymax = y
            if (y < self.ymin):
                self.ymin = y
                    
class Solenoid:
    def __init__(self, r, height, dh, dtheta):

        thetaIncrements = int(((2*sp.pi)/dtheta)) 
        zIncrements = int(height/dh) + 1
        
        self.stepCount = thetaIncrements * zIncrements
        self.path = np.zeros((self.stepCount, 3))               
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0        
        self.zmin = 0
        self.zmax = 0
        
        z = 0
        i = 0
        for j in range(0, zIncrements):
            
            # todo: wrap all the way around to 2pi on the last j iteration?
                
            for k in range(0, thetaIncrements):
                               
                theta = (2 * k * sp.pi) / (thetaIncrements)     
                x = r*sp.cos(theta)
                y = r*sp.sin(theta)
                
                self.path[i] = (x, y, z)
                                
                if (x > self.xmax):
                    self.xmax = x
                if (x < self.xmin):
                    self.xmin = x
                if (y > self.ymax):
                    self.ymax = y
                if (y < self.ymin):
                    self.ymin = y
                
                i+=1
                j+=1
                z+=dh
                    
                
            if (z > self.zmax):
                self.zmax = z
            if (z < self.zmin):
                self.zmin = z

    
if __name__ == "__main__":    
    print ("\nLineCharge(10,0.5)\n")
    currentPath = Line(10,0.5)
    
    for i in range(0, currentPath.stepCount):   
        print (str(currentPath.path[i]))
        
    print ("\nLoopCharge(10, sp.pi/2)\n")
    currentPath = Loop(10, sp.pi/2)
    
    for i in range(0, currentPath.stepCount):   
        print (str(currentPath.path[i]))
    
    print ("\nSolenoid(10, 2, 0.5, sp.pi/2)\n")
    currentPath = Solenoid(10, 2, 0.5, sp.pi/2)   
    
    for i in range(0, currentPath.stepCount):   
        print (str(currentPath.path[i])) 
