#!/usr/bin/env python

# Create summed image file in desired energy range

import os
import sys
import glob
import subprocess
import math

if len(sys.argv) != 3:
    sys.stderr.write("Usage %s E_low E_high" % sys.argv[0])
    sys.exit(1)

E_low = str(sys.argv[1])
E_high = str(sys.argv[2])
#obsids=['891','4977','6101']
obsids = ['2208','2330','2331','2332','2333','2334'] # Hydra-A ,'4969', '4970'
#obsids=['06101']
op=''
exposures=[]

def get_exposures(evt2name):

    # Get exposure time for each obsid
    exposure = float(subprocess.check_output('dmkeypar %s exposure echo=yes' % (evt2name), shell=True)[:-1])
    return exposure

for obs in obsids:
    print("Processing obs. id %s ..." % obs)
    os.system('cp %s/reprocess/*reproj_evt2.fits .' % (obs))
    os.system('cp %s/backgrounds/bgevt2_sum_obsexpx*.fits .' % (obs))     

    # Create binned image of the reprojected events files for adding
    evt2=str(obs)+'_reproj_evt2.fits'
    os.system('dmcopy "%s_reproj_evt2.fits[bin sky=1][energy=%s:%s][opt mem=135]" %s_%s_%s.img' % (obs, E_low, E_high, obs, E_low, E_high))

    # Chop summed background files to energy range, then normalize to the observation's exposure time
    x=glob.glob('bgevt2_sum_obsexpx*')[0]
    x=x.split('bgevt2_sum_obsexpx')[1]
    x=int(x.split('.fits')[0])

    os.system('dmcopy "bgevt2_sum_obsexpx%s.fits[energy=%s:%s][bin sky=1][opt mem=135]" bgtemp.fits' % (x,E_low,E_high))    

    os.system('dmimgcalc "bgtemp.fits" none out=%s_bgevt2_obsexp.fits op="imgout=(img1/%f)"' % (obs,x))

    os.system('rm bgevt2_sum_obsexpx*.fits')
    os.system('rm bgtemp.fits')


    # Get exposures to weight the summed exposure map
    exp = float(get_exposures(evt2))
    print(exp)
    exposures.append(exp)
exp_total=sum(exposures)
print('total:',exp_total)

for i in range(len(obsids)):
# Keep track of number of summations needed for dmimgcalc
    j=i+1    
    op=op+'img'+str(j)+'*'+str(exposures[i])+'+'

# Trim final + sign for dmimgcalc operation
op=op[:-1]
print(op)


# Sum reprojected images!
os.system('dmimgcalc "*_%s_%s.img" none out=evt2_summed_%s_%s.fits op="imgout=((%s)/%s)" clobber=yes' % (E_low,E_high,E_low,E_high,op,exp_total)) #Sums together the reprojected images

os.system('dmimgcalc "*_bgevt2_obsexp.fits" none out=bg_expscaled_%s_%s.fits op="imgout=((%s)/%s)" clobber=yes' % (E_low,E_high,op,exp_total)) #Calculates the background summed image

os.system('dmimgcalc "evt2_summed_%s_%s.fits,bg_expscaled_%s_%s.fits" none out=evt2_bgsub_%s_%s.fits op="imgout=(img1-img2)" clobber=yes' % (E_low,E_high,E_low,E_high,E_low,E_high)) #background-subtracted image

# Remove unnecessary files
#os.system('rm *_%s_%s.img' % (E_low,E_high))
os.system('rm *_reproj_evt2.fits')
os.system('rm *_bgevt2_obsexp.fits')

