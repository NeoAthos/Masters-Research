#!/usr/bin/env python3.6

#Reproject a set of events files

import os
import sys
import glob
import subprocess
import math

# Observations to be reprojected - Put Obsid with longest exposure time first, as all objects will be reprojected to match its coordinate system
obsids=['04960']
op=''
#print("Reprojecting all obsids onto: %s" % (obsids[0]))
for i in range(len(obsids)):
	print('ddd_%s' %(obsids[i]))
    #os.system('cd 04977/reprocess')
    os.system('ls')
    # First file doesn't need reprojecting, just copying the name
    #if i == 0:
        #os.system('cp acis*evt2* %s_reproj_evt2.fits' %(obsids[0]))

    # Reproject events files to first observation defined   	
    #else:
       # print("Reprojecting: %s onto %s " %(obsids[i],obsids[0]))
        #os.system('reproject_events acis*_repro_evt2.fits* %s_reproj_evt2.fits aspect=none match="../../%s/reprocess/%s_reproj_evt2.fits" clobber=yes' % (obsids[i], obsids[0], obsids[0])) 

    #os.system('cd ../../')
print("Done")
