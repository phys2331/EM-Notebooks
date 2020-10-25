# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 19:59:04 2020

@author: Thomas.Johnson

Numerical integration, according the the Biot-Savart law, for arbitrary current
paths.

Example Current Paths:
    
    path.Line(1, 0.1)
    path.KinkedLine(1,1,0.2,0.2)
    path.Loop(1, sp.pi/12)
    path.Solenoid(0.25, 0.5, 0.025, sp.pi/4)
    path.Toroid(0.6, 1.0, sp.pi/6, sp.pi/32)    

"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import CurrentPath as path
import Graphics as gfx
            

# the biot-savart law
def BiotSavart(I, dL, r_hat, r_mag):
    mu_0 = 1.256e-6                       # [H/m]
    coeff = (mu_0*I)/(4*np.pi)            # [HA/m]
    dl_cross_r = np.cross(dL,r_hat)       # [m]
    
    return coeff * dl_cross_r / r_mag**2  # [HA/m] = [T] 


# create a current path
current = path.Line(1, 0.1)
current.magnitude = 1                     # [A]


# create points of interest
margin = 1                                # [m]
testPointInterval = 16

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
                u = current.path[p,0]
                v = current.path[p,1]
                w = current.path[p,2]
                
                rinitial = np.array([u,v,w])                
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


# plot B-field and current path (use a loop to support dynamic/color)
plt.style.use('dark_background')
fig = plt.figure(figsize=(9,9), dpi=600)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

ax.grid(False) 
ax.w_xaxis.pane.set_color((0.15,0.15,0.15))
ax.w_yaxis.pane.set_color((0.15,0.15,0.15))
ax.w_zaxis.pane.set_color((0.15,0.15,0.15))
ax.w_xaxis.gridlines.set_lw(3)
ax.w_yaxis.gridlines.set_lw(3)
ax.w_zaxis.gridlines.set_lw(3)
#ax.view_init(elev=0, azim=180)

  
# plot the current's path
ax.plot(current.path[:,0],current.path[:,1],current.path[:,2], 
        linewidth=0.6, color=(55/255,105/255,250/255, 0.7))

ax.scatter(current.path[:,0],current.path[:,1],current.path[:,2], 
           s=0.6, alpha=0.2, color="white")


# plot the B-field (use loop to set RGBA against normalized extents)
colorSet = gfx.VibrantOctantColorSet()

for i in range(0, testPointCount):
    ax.quiver(P[i,0], P[i,1], P[i,2],
              B[i,0], B[i,1], B[i,2],
              normalize=True, length=0.1, linewidth=1, arrow_length_ratio=0.5, 
              color=gfx.ColorFromOctant(B[i], B_ext, colorSet, 1.6))           

plt.show()
plt.style.use('default') # reset plot style
