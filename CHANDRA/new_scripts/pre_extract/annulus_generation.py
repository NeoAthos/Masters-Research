#!/usr/bin/env python

import math
import os
import sys
import glob
import subprocess

if __name__ == '__main__':

# Input cluster name:
    if len(sys.argv) != 3:
        print ("Usage: %s cluster_name counts/bin" % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    clustername = sys.argv[1]
    bin_cts = float(sys.argv[2])

    # Read in from cluster data file.
    # Gives central position of Cluster, and whether or not there is a central point source.

    #This script use to read in data from a file but it only really read in the physical coordinates
    #of the centre, so its much faster to just hard code the coordinates in, as I have below. 
    #However I'll leave this file reading code in here for any future generations though.

############################################################
    # file = open('/home/connor/DATA/data_massprof')
    # for line in file:
    #     if line.startswith('%s' % clustername):
    #         spl = line.split()
    #         xpos = float(spl[5])
    #         ypos = float(spl[6])
    #         innermost_radius = float(spl[7])
    #     else:
    #         continue

    # file.close()
#############################################################

    #Physical Coordinates of Cluster Centre
    xpos, ypos = 4177.998, 3973.9977 #A2029
    #xpos, ypos = 4155.1352, 4053.2943    #RBS0533

    print("Cluster Centre:(x,y)=(%s,%s)" % (xpos,ypos))
    
    cldir = '/home/neolnx/Documents/XRISMprep/' + clustername + '/' #For Home/root directory
    #cldir = '/media/connor/Omega_Data/cluster_data/fixerupper/' + clustername + '/' #For Omega_Data Drive
    print("Directory: %s" % (cldir))
    evt2_bgsub = glob.glob(cldir + 'evt2_bgsub*.fits')[0]
#    evt2_bgsub = glob.glob('raw*.fits')[0]
    pt_sources = cldir + '/wavdetect/allsources.reg'

    # Creates a binned image with pt. sources removed if it does not already exist.
    if os.path.isfile('evt2_excps.fits') == False:
        print("Creating background subtracted image with point sources removed...")
        os.system('dmcopy "%s[exclude sky=region(%s)][bin sky=1][opt mem=550]" evt2_excps.fits clobber=yes' % (evt2_bgsub,pt_sources))
        print("Finished...")   
    evt2 = 'evt2_excps.fits'
    # Initial conditions for loop to work properly. Set R_max so that annuli don't go off chip.
    #r_outer = innermost_radius
    #print(innermost_radius)
    # r_width = 1.0
    r_width = 0.25
    #r_max = 1000
    #r_width = 0.5
    r_max = 600
    i=0 

    # Create region that encompasses all regions useda
    allannuli = open('annuli_all.reg','w')
    #allannuli.write('# Region file format: CIAO version 1.0' + '\n')

    r_outer = 0 #Set outer annulus radius equal to 0 initially. You may want to change this if you're not interested in any central properties of the cluster
    print("Generating Annuli...")

    # Generate annuli!
    while r_outer < r_max:
        r_inner = r_outer
        counts = 0
        # The bin widths start as the previous bin's width, and propagate outwards.
        while counts < bin_cts:
            
            if counts==0:
                r_outer = r_outer + r_width/2.0
            else:
                r_outer = r_outer + r_width/10.0

            os.system('punlearn dmstat')
            os.system('dmstat "%s[sky=annulus(%s,%s,%s,%s)]" centroid=no verbose=0' % (evt2,xpos,ypos,r_inner,r_outer))
            counts = (float(subprocess.check_output('pget dmstat out_sum', shell=True))) #multiply by 2.0 for no reason - Somehow decreases the size of each annulus and generating more regions, and also allowing more counts per region
            # counts = (float(subprocess.check_output('pget dmstat out_sum', shell=True)
            if r_outer > r_max:
                break
        
        
        r_width = r_outer - r_inner

        regout = open('region'+str(i)+'.reg','w')
        #regout.write('# Region file format: CIAO version 1.0' + '\n')   
        regout.write('annulus(%s,%s,%s,%s)' % (xpos,ypos,r_inner,r_outer) + '\n')
        allannuli.write('annulus(%s,%s,%s,%s)' % (xpos,ypos,r_inner,r_outer) + '\n')
        
        bin_cts = 1.1 * bin_cts
        i = i + 1

        if i > 26:
            print ("WARNING: Number of bins exceeds limit for clmass")
        print (r_inner,r_outer,counts)
        
        

