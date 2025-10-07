#!/usr/bin/env python

import math
import os
import sys
import glob
import subprocess
from ciao_contrib.runtool import dmstat
from astropy.cosmology import FlatLambdaCDM as LCDM
import astropy.units as u

cosmo = LCDM(70, 0.3)

if __name__ == '__main__':

# Input cluster name:
    # if len(sys.argv) != 4:
    #     print("Usage: %s evt2_file point_source_file counts/bin" % sys.argv[0], file=sys.stderr)
    #     sys.exit(1)

 
    if len(sys.argv) != 5:
        print("Usage: %s evt2_file point_source_file counts/bin redshift" %
              sys.argv[0], file=sys.stderr)
        sys.exit(1)

    evt2_file = sys.argv[1]
    pt_sources=sys.argv[2]
    bin_cts = float(sys.argv[3])

    if len(sys.argv) == 5:
        z = float(sys.argv[4])

    asec_per_kpc = cosmo.arcsec_per_kpc_proper(z).value

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

    # Physical Coordinates of Cluster Centre
    #xpos, ypos = 3858.7144, 4406.1456    # Abell 85
    #xpos, ypos = 3374.28,3992.56 	#A3266
    #xpos, ypos = 3982.3242,4013.4776	#HerculesA
    xpos, ypos = 4115.1667,4011.4722	#M87
    # xpos, ypos = 4061.9515, 4091.7727    # Abell 1795
    # xpos, ypos = 4083.821, 4091.6523     # Abell 2597
    #xpos, ypos = 4112.0449, 3963.6242    # Abell 2052
    #xpos, ypos = 4193.0192, 3997.31      # Abell 2029
    #xpos, ypos = 4086.79,4262.79	#centaurus
    #xpos,ypos = 4056.12,4247.07    #Ophiuchus
    #xpos, ypos = 3947.7475, 4093.9265	#3C129
    #xpos, ypos = 4381.45, 3478.49	#AWM7 
    #xpos, ypos = 4433.55,  4205.58	#Abell 2319
    #xpos, ypos = 4008.19, 4114.68       #Abell 3571
    #xpos, ypos = 4152.73, 4344.67	#Coma
    #xpos, ypos = 4644.93,4433.88	#Abell 754
    #xpos, ypos = 4080.68,3952.18	# Abell 2142
    #xpos, ypos = 4239.61,4151.70	#Abell 2199
    #xpos, ypos = 4647.7, 4451.9 	#Abell 3667
    #xpos, ypos = 4138.77, 4297.34 	#Abell 478
    #xpos, ypos = 3950.224,4234.9488	 	#CygnusA
    #xpos, ypos = 4064.03,4099.49	 	#Abell 1795
    #xpos, ypos = 4045.17,  3978		#Abell 426
    #xpos, ypos = 4312.53,  4318.94	#MS0735
    # xpos, ypos = 4376, 3835              # Phoenix
    # xpos, ypos = 4008.2473, 4341.372     # Abell 1835
    # xpos, ypos = 4155.1352, 4053.2943    # RBS0533
    # xpos, ypos = 4141.0269, 4005.3346    # Abell 1664
    # xpos, ypos = 4184.4023, 4175.6444    # PKS0745
    # xpos, ypos = 4314.0875, 4316.4922    # MS07
    # xpos, ypos = 4038.5885, 4230.6792    # MACS1347
    #xpos, ypos = 4150.5809, 3962.7113    # Hydra-A
    # xpos, ypos = 3904.3717, 4244.3535    # RXCJ1504
    # xpos, ypos = 4145.5201, 3972.9265    # Abell 133
    # xpos, ypos = 4062.3777, 3962.3569    # IC1262
    # xpos, ypos = 4071.39, 4072.1691      # Abell 262
    # xpos, ypos = 4048.155, 4215.9264     # Abell 2626
    # xpos, ypos = 4069.4801, 4283.1246    # NGC 5044
    # xpos, ypos = 3733.683, 4583.6244     # Zw 7061
    # xpos, ypos = 4267.0368, 4053.1774    # AS1101
    # xpos, ypos = 4179.2408, 3977.4543    # ZwCl 3146
    # xpos, ypos = 4240.0529, 4151.8693    # Abell 2199
    # xpos, ypos = 4049.966, 4232.9969    # MACS1423+24
    # xpos, ypos = 4003.6653, 4015.3206    # Zw 2701
    # xpos, ypos = 4230.2897, 4312.8458    # RXCJ1539


    print("Cluster Centre:(x,y)=(%s,%s)" % (xpos,ypos))

    # Creates a binned image with pt. sources removed if it does not already exist.
    if os.path.isfile('evt2_excps.fits') == False:
        print("Creating background subtracted exposure corrected image with point sources removed...")
        os.system('dmcopy "%s[exclude sky=region(%s)][bin sky=1][opt mem=550]" evt2_excps.fits clobber=yes' % (evt2_file,pt_sources))
        print("Finished...")   
    evt2 = 'evt2_excps.fits'
    # Initial conditions for loop to work properly. Set R_max so that annuli don't go off chip.
    #r_outer = innermost_radius
    #print(innermost_radius)
    r_width0 = 1.0
    r_width = 3.0
    # r_width = 0.5
    r_max = 1000
    #r_width = 0.5
    r_max = 200*asec_per_kpc/0.492
    i=0 
    r_mid = 30*asec_per_kpc/0.492
    print("30 kpc at pixel:", r_mid)
    print("200 kpc at pixel:", r_max)

    # Create region that encompasses all regions useda
    allannuli = open('annuli_all.reg','w')
    allannuli.write('# Region file format: CIAO version 1.0' + '\n')

    r_outer = 0 #Set outer annulus radius equal to 0 initially. You may want to change this if you're not interested in any central properties of the cluster
    print("Generating Annuli...")

    # Generate annuli!
    while r_outer < r_max:
        r_inner = r_outer
        counts = 0
        # The bin widths start as the previous bin's width, and propagate outwards.
        while counts < bin_cts:
            
            # if counts==0:
            if r_outer <= r_mid :
                r_outer = r_outer + r_width0/2
            else:
                r_outer = r_outer + r_width
                
            dmstat("%s[sky=annulus(%s,%s,%s,%s)]"% (evt2,xpos,ypos,r_inner,r_outer), centroid=False, verbose=0)
            counts = float(dmstat.out_sum)
            # os.system('punlearn dmstat')
            # os.system('dmstat "%s[sky=annulus(%s,%s,%s,%s)]" centroid=no verbose=0' % (evt2,xpos,ypos,r_inner,r_outer))
            # counts = (float(subprocess.check_output('pget dmstat out_sum', shell=True))) #multiply by 2.0 for no reason - Somehow decreases the size of each annulus and generating more regions, and also allowing more counts per region
            # counts = (float(subprocess.check_output('pget dmstat out_sum', shell=True)))
            if r_outer > r_max:
                break
        
        
        r_width = r_outer - r_inner
        r_width0 = r_width0*1.5

        #regout = open('region'+str(i)+'.reg','w')
        #regout.write('# Region file format: CIAO version 1.0' + '\n')   
        #regout.write('annulus(%s,%s,%s,%s)' % (xpos,ypos,r_inner,r_outer) + '\n')
        allannuli.write('annulus(%s,%s,%s,%s)' % (xpos,ypos,r_inner,r_outer) + '\n')
        
        if r_outer > r_mid:
            bin_cts = 3 * bin_cts
        i = i + 1

        if i > 26:
            print("WARNING: Number of bins exceeds limit for clmass")
        print(r_inner,r_outer,counts)
        
        

