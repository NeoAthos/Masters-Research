#!/usr/bin/env python

import glob

pixel = 0.492
scale = 3.5

def getR( line):
    regArr=line.split(",")
    rin = str(regArr[2]) # use semi-major axis for ellipses
    rout = str(regArr[3]) # there is no trailing ")" to cut
    rout = rout[:-2]
    return (rout, rin) 

# Create region_list.txt for contour binning

#regions = glob.glob('xaf_*.reg')
regions = glob.glob('region*.reg')

fout = open('profile_radii.txt','w')

for i in range(len(regions)):
    infile1 = open('region' + str(i) + '.reg' , 'r')
        #infile2 = open('region' + str(i+1) + '.reg' , 'r')
    for line in infile1:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            continue
        else:
            line1=line

    rout , rin = getR(line1)
        #r21 , r22 = getR(line2)
    print(rin, rout)       
    fout.write(str(rin)+" "+str(rout)+"\n")
        
fout.close()
