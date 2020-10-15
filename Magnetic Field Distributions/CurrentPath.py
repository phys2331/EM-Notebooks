# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:30:00 2020

@author: Thomas.Johnson

Utility methods to generate arrays of 3D positions that approximate common  
geometric shapes. Iterating over the "path" array is like following a current.
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
    def __init__(self, r, minHeight, dh, dtheta):
        # todo: shift down on z-axis to center on origin
        # todo: emulate toroid logic to ensure exact height rather than min
        
        thetaIncrements = int(((2*sp.pi)/dtheta)) 
        zIncrements = int(minHeight/dh) + 1
        
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

class Toroid:
    def __init__(self, rInner, rOuter, dtheta, dphi):

        dToroid = rOuter - rInner
        rToroid = dToroid/2
        rCenterOfToroid = rOuter - rToroid
        
        thetaIncrements = int(((2*sp.pi)/dtheta))
        phiIncrements = int(((2*sp.pi)/dphi))
        
        self.stepCount = thetaIncrements * phiIncrements
        self.path = np.zeros((self.stepCount, 3))               
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0        
        self.zmin = 0
        self.zmax = 0
        
        i = 0        
        for j in range(0, phiIncrements):
            phi = (2 * j * sp.pi) / (phiIncrements) 
            nextPhi = (2 * (j+1) * sp.pi) / (phiIncrements)            
            currentPhi = phi
            
            dPhi = (nextPhi-phi)
            
            for k in range(0, thetaIncrements):                              
                currentPhi = phi + dPhi*(k/thetaIncrements)
                
                theta = (2 * k * sp.pi) / (thetaIncrements)
                              
                xToroid = rCenterOfToroid*sp.cos(currentPhi)
                yToroid = rCenterOfToroid*sp.sin(currentPhi)
                zToroid = 0

                # depending on where we are while we sweep, the change in x and
                # y, relative to the solenoid's spin, oscillates between -1 and 
                # +1 (just like sin and cos)
                #
                # we use that to adjust how much the solenoid's dl contributes
                # to the total x and y positions               
                xContributionFactor = sp.cos(currentPhi)
                yContributionFactor = sp.sin(currentPhi)
                
                magnitude = rToroid*sp.cos(theta)
                
                ySolenoid = yToroid + (magnitude * yContributionFactor)
                xSolenoid = xToroid + (magnitude * xContributionFactor)
                zSolenoid = zToroid + (    1     * rToroid*sp.sin(theta))
                
                self.path[i] = (xSolenoid, ySolenoid, zSolenoid)
                                
                if (xSolenoid > self.xmax):
                    self.xmax = xSolenoid
                if (xSolenoid < self.xmin):
                    self.xmin = xSolenoid
                if (ySolenoid > self.ymax):
                    self.ymax = ySolenoid
                if (ySolenoid < self.ymin):
                    self.ymin = ySolenoid
                if (zSolenoid > self.zmax):
                    self.zmax = zSolenoid
                if (zSolenoid < self.zmin):
                    self.zmin = zSolenoid                    
                
                i+=1
                           
class KinkedLine:
    def __init__(self, xlength, ylength, dx, dy):

        
        #todo: no workie
        xStepCount = int(xlength/dx)+1
        yStepCount = int(ylength/dy)+1

        xshift = int(xStepCount/2)
        #yshift = int(yStepCount/2)
        
        self.stepCount = xStepCount + yStepCount
        self.path = np.zeros((self.stepCount, 3))               
        
        for i in range(0, xStepCount):
            self.path[i] = ((i - xshift)*dx,0,0)        

        lastX = (xStepCount-1-xshift)*dx
        for i in range(0, yStepCount):
            self.path[xStepCount+i] = (lastX,i*dy,0)
                                       

        self.xmin = -xshift*dx
        self.xmax = xshift*dx
        self.ymin = 0
        self.ymax = ylength
        self.zmin = 0
        self.zmax = 0

               
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
        
    print ("\nToroid(0.5, 1.0, sp.pi/2, sp.pi/4)\n")
    currentPath = Toroid(0.5, 1.0, sp.pi/2, sp.pi/4)
    
    for i in range(0, currentPath.stepCount):   
        print (str(currentPath.path[i]))
        
    print ("\nKinkedLine(1, 1, 0.5, 0.5)\n")
    currentPath = KinkedLine(1, 1, 0.5, 0.5)
    
    for i in range(0, currentPath.stepCount):   
        print (str(currentPath.path[i]))        