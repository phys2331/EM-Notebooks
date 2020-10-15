# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 19:59:04 2020

@author: Thomas.Johnson
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import CurrentPath as path
import Graphics as gfx
            

# biot-savart law
def BiotSavart(I, dL, r_hat, r_mag):
    mu_0 = 1.256e-6                       # [H/m]
    coeff = (mu_0*I)/(4*np.pi)            # [HA/m]
    dl_cross_r = np.cross(dL,r_hat)       # [m]
    
    return coeff * dl_cross_r / r_mag**2  # [HA/m] = [T] 


# create a current path w/ arbitrary resolution
#current = path.Line(1, 0.1)
#current = path.Loop(1, sp.pi/8)
#current = path.Solenoid(1, 0.25, 0.005, sp.pi/8)
#current = path.Toroid(0.6, 1.0, sp.pi/8, sp.pi/32)
#current = path.KinkedLine(1,1,0.2,0.2)

current = current = path.Line(1, 0.1)
current.magnitude = 1 #[T]

# create points of interest
margin = 1                                # [m]
testPointInterval = 12

xPoints = np.linspace(int(current.xmin-margin), int(current.xmax+margin), 
                      num=testPointInterval)
yPoints = np.linspace(int(current.ymin-margin), int(current.ymax+margin), 
                      num=testPointInterval)
zPoints = np.linspace(int(current.zmin-margin), int(current.zmax+margin), 
                      num=testPointInterval)

# capture min and max values for normalization
B_ext = gfx.CartesianExtents()

# calculate B-field at each point
testPointCount = int(xPoints.shape[0]**3)
B = np.zeros((testPointCount,3))
P = np.zeros((testPointCount,3))

# todo: do this python style w/ set operations
index = 0
for i in xPoints:
    for j in yPoints:
        for k in zPoints: 
            for p in range(1, current.stepCount):
                rinitial = np.array([current.path[p,0],current.path[p,1],current.path[p,2]])
                rfinal = np.array([i,j,k])
                r = np.subtract(rfinal, rinitial)                
                r_mag = np.linalg.norm(r)                           
                r_hat = r/r_mag                                
                dl = current.path[p] - current.path[p-1]
                
                dB = BiotSavart(current.magnitude,dl,r_hat,r_mag)
                B[index] += dB
          
                B_ext.SuggestExtent(B[index])
                
            P[index] = [i,j,k]
            index+=1   
    
# plot B-field and current path (use a loop to support dynamic alpha)
fig = plt.figure(figsize=(9,9), dpi=600)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

# plot the current's path
ax.plot(current.path[:,0],current.path[:,1],current.path[:,2], linewidth=1, 
        alpha=0.8, color= "orange")
ax.scatter(current.path[:,0],current.path[:,1],current.path[:,2], s=1, 
           alpha=0.025, color="blue")
#ax.view_init(elev=0, azim=180)
#ax.set_axis_off()
  
# plot the B-field (use loop to set RGBA against normalized extents)
for i in range(0, testPointCount):
    ax.quiver(P[i,0], P[i,1], P[i,2],
              B[i,0], B[i,1], B[i,2],
              normalize=True, length=0.1, linewidth=1, arrow_length_ratio=0.5, 
              color=gfx.ColorFromCartesian(B[i], B_ext))            

plt.show()
