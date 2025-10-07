#!/usr/bin/env python

import math
import os
import sys
import glob
import subprocess
from ciao_contrib.runtool import dmstat
from astropy.cosmology import FlatLambdaCDM as LCDM
import astropy.units as u
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy
from astropy.io import fits


import matplotlib.pyplot as plt
import matplotlib.cm as cm
from astropy.io import fits
import pyregion

def getRegionSize( line1, line2=None ):
    regArr1 = line1.split(",")
    x = float(regArr1[0][4:])
    y = float(regArr1[1])
    width = float(regArr1[2])
    height = float(regArr1[3])
    print(x,y,width,height)
    x1 = x - (width/2)
    x2 = x + (width/2)
    y1 = y - (height/2)
    y2 = y + (height/2)
    return (x1,x2,y1,y2) 

# read in the image
xray_name = (sys.argv[1])
f_xray = fits.open(xray_name)

#fout = open('profile_radii.txt','w')
regions = glob.glob('XRISM_region1.reg')
for i in range(len(regions)):
    reg = 'XRISM_region.reg'
    infile = open(reg, 'r')
    for line in infile:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            continue
        else: 
            x1, x2, y1, y2 = getRegionSize(line)
            print(x1, x2, y1, y2)       

try:
    from astropy.wcs import WCS
    from astropy.visualization.wcsaxes import WCSAxes

    wcs = WCS(f_xray[0].header)
    fig = plt.figure()
    ax = WCSAxes(fig, [0.15, 0.15, 0.75, 0.75], wcs=wcs)
    fig.add_axes(ax)
except ImportError:
    ax = plt.subplot(111)

fmt = '%1.2f'
my_cmap = copy.copy(matplotlib.cm.get_cmap('gray')) # copy the default cmap
my_cmap.set_bad((0,0,0))
ax.imshow(f_xray[0].data, cmap=my_cmap,vmin=0.01, norm=LogNorm())
test = ax.imshow(f_xray[0].data, cmap=cm.gray,norm=LogNorm(),origin="lower")
plt.colorbar(test, ax=ax,format = fmt) 

reg_name = "XRISM_region_colour.reg"		#You will have to switch this between region & region1 (region1 has no point source removal)
r = pyregion.open(reg_name).as_imagecoord(header=f_xray[0].header)
print (r[0].attr[0])
print (r[0].attr[1])
# select region shape with tag=="Group 1"
patch_list1, artist_list1 = r.get_mpl_patches_texts()

for p in patch_list1:
    ax.add_patch(p)
for t in artist_list1:
    ax.add_artist(t)

#plt.xlim(x1,x2)
#plt.ylim(y1,y2)

plt.xlim(x1-200,x2+200)
plt.ylim(y1-200,y2+200)
plt.xlabel("Right Ascension")
plt.ylabel("Declination")
plt.savefig('XRISM_region.png')
plt.show()


    
