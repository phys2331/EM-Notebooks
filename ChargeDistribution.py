# -*- coding: utf-8 -*-
"""
10/9/2020 - Thomas L. Johnson
"""

#import math as math
import numpy as np
import sympy as sp

class LineCharge:
    def __init__(self, length, dl):
        
        # we want to return the array of 3d positions that represent the line 
        # charge as well as the min/max x,y,z dimensions to help us identify a 
        # suitable meshgrid 
        # the order of elements in the array tells us the direction of dl
        
        # create a line of segments centered about the origin
        
        self.segmentCount = int(length/dl)+1
        halfwayIndex = int(self.segmentCount/2)
        
        self.segments = np.zeros((self.segmentCount, 3))

        # todo: fancy way to do this?
        for i in range(0, self.segmentCount):
            self.segments[i] = ((i-halfwayIndex)*dl,0,0)

        self.xmin = -halfwayIndex*dl
        self.xmax = halfwayIndex*dl
        self.ymin = 0
        self.ymax = 0
        self.zmin = 0
        self.zmax = 0
        
class LoopCharge:
    def __init__(self, r, dtheta):
        
        # create a loop of segments centered about the origin

        self.segmentCount = int((2*sp.pi)/dtheta) + 1
        self.segments = np.zeros((self.segmentCount, 3))               
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0        
        self.zmin = 0
        self.zmax = 0
        
        for i in range(0, self.segmentCount):
            theta = (2 * i * sp.pi) / (self.segmentCount-1)     
            x = r*sp.cos(theta)
            y = r*sp.sin(theta)
            
            self.segments[i] = (x, y, 0)
            
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
        
        # create a corkscrew of segments centered about the origin

        thetaIncrements = int(((2*sp.pi)/dtheta)) #don't add one since we want to move up in z-space before closing the loop
        zIncrements = int(height/dh) + 1
        
        self.segmentCount = thetaIncrements * zIncrements
        self.segments = np.zeros((self.segmentCount, 3))               
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0        
        self.zmin = 0
        self.zmax = 0
        
        z = 0
        i = 0
        for j in range(0, zIncrements):
            
            # todo: wrap all the way around to 2pi on the last j iteration
                
            for k in range(0, thetaIncrements):
                               
                theta = (2 * k * sp.pi) / (thetaIncrements)     
                x = r*sp.cos(theta)
                y = r*sp.sin(theta)
                
                self.segments[i] = (x, y, z)
                                
                if (x > self.xmax):
                    self.xmax = x
                if (x < self.xmin):
                    self.xmin = x
                if (y > self.ymax):
                    self.ymax = y
                if (y < self.ymin):
                    self.ymin = y
                
                i+=1
                    
                
            if (z > self.zmax):
                self.zmax = z
            if (z < self.zmin):
                self.zmin = z
                    
            z+=dh
    
if __name__ == "__main__":    
    print ("\nLineCharge(10,0.5)\n")
    chargeConfiguration = LineCharge(10,0.5)
    
    for i in range(0, chargeConfiguration.segmentCount):   
        print (str(chargeConfiguration.segments[i]))
        
    print ("\nLoopCharge(10, sp.pi/2)\n")
    chargeConfiguration = LoopCharge(10, sp.pi/2)
    
    for i in range(0, chargeConfiguration.segmentCount):   
        print (str(chargeConfiguration.segments[i]))
    
    print ("\nSolenoid(10, 2, 0.5, sp.pi/2)\n")
    chargeConfiguration = Solenoid(10, 2, 0.5, sp.pi/2)   
    
    for i in range(0, chargeConfiguration.segmentCount):   
        print (str(chargeConfiguration.segments[i])) 