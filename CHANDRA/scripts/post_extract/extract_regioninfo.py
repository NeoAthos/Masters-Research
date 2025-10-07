#!/usr/bin/env python

import glob

pixel = 0.492
scale = 3.5

def getR( line1, line2=None ):
    regArr1 = line1.split(",")

    if line.startswith("ellipse"):
        if line2 is None:
            print("Elliptical annuli must have an inner ellipse excluded")
            sys.exit(1)
        regArr2 = line2.split(",")
        innerR = regArr2[2] # use semi-major axis for ellipses
        outerR = regArr1[2] # there is no trailing ")" to cut
    else:
        innerR = regArr1[2]
        if regArr1[3].endswith(")"): outerR = regArray1[3][:-1]
        else: outerR = regArr1[3][:-2]

    return ( innerR, outerR ) 

# Create region_list.txt for contour binning

#regions = glob.glob('xaf_*.reg')
regions = glob.glob('region*.reg')

fout = open('profile_radii.txt','w')

for i in range(len(regions)):
    reg = 'region' + str(i) + '.reg'
    infile = open('region' + str(i) + '.reg' , 'r')
    for line in infile:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            continue
        else: 
            rin , rout = getR(line)
            print(rin, rout)       
            fout.write(str(rin)+" "+str(rout)+"\n")
        
fout.close()
