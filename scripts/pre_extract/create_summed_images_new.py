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

#obsids=['15173', '15174', '16263', '16264', '904'] # Abell 85

#obsids=['1601', '10722', '17147'] #Centaurus

# obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795

# obsids = ['922', '6934', '7329', '19596', '19597', '19598', '20626', '20627', '20628', '20629', '20805', '20806', '20811', '20817'] # Abell 2597

# obsids = ['890', '5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052

obsids = ['891', '4977', '6101'] # Abell 2029

#obsids = ['14269','14275','15485','15490','17228'] #A1795 ,'10901','12026', '12029','13106','13113',,

# obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix

# obsids= ['495', '496', '6880', '6881', '7370'] # Abell 1835

# obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664

# obsids = ['508', '2427', '6103', '7694', '12881'] # PKS0745

# obsids = ['4197', '10468', '10469', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421

# obsids = ['506', '507', '2222', '3592', '13516', '13999', '14407'] # MACSJ1347-11

# obsids = ['4969', '4970'] # Hydra-A

# obsids = ['4935', '5793', '17197', '17669', '17670'] # RXCJ1504

# obsids = ['2203', '9897', '13518'] # Abell 133

# obsids = ['2018', '6949', '7321', '7322'] # IC1262

# obsids = ['2215', '7921'] # Abell 262

# obsids = ['3192', '16136'] # Abell 2626

# obsids = ['798', '9399', '17195', '17196', '17653', '17654', '17666'] # NGC 5044

# obsids = ['543', '7709', '4192']  # Zw 7160

# obsids = ['1668', '11758']  # AS1101

# obsids = ['909', '1651', '9371']  # ZwCl 3146

# obsids = ['497', '498', '10748', '10803', '10804', '10805']  # Abell 2199

# obsids = ['1657', '4195']  # MACS1423+24

# obsids = ['3195', '7706', '12903']  # Zw 2701

# obsids = ['8266']  # RXCJ1539


op1=''
exposures=[]

def get_exposures(evt2name):

    # Get exposure time for each obsid
    exposure = float(subprocess.check_output('dmkeypar %s exposure echo=yes' % (evt2name), shell=True)[:-1])
    return exposure

for obs in obsids:
    print("Processing obs. id %s ..." % obs)
    os.system('cp %s/backgrounds/bgevt2_sum_obsexpx*.fits .' % (obs))     

    # Create binned image of the reprojected events files for adding
    evt2=obs+'/reprocess/'+obs+'_reproj_evt2.fits'

    # Get exposures to weight the summed exposure map
    exp = float(get_exposures(evt2))
    print(exp)
    exposures.append(exp)
    
    os.system('punlearn dmimgcalc')
    os.system('dmcopy "%s/reprocess/%s_reproj_evt2.fits[bin sky=1][energy=%s:%s][opt mem=150]" %s_%s_%s.img clobber=yes' % (obs,obs, E_low, E_high, obs, E_low, E_high))



exp_total=str(int(sum(exposures)))
print('total:',exp_total)

for i in range(len(obsids)):
# Keep track of number of summations needed for dmimgcalc
    j=i+1    
    op1=op1+'img'+str(j)+'+'

# Trim final + sign for dmimgcalc operation
op1=op1[:-1]
print(op1)



# Sum reprojected images!
os.system('dmimgcalc "*_%s_%s.img" none out=evt2_summed_%s_%s.fits op="imgout=(%s)" clobber=yes' % (E_low,E_high,E_low,E_high,op1)) #Sums together the reprojected images

os.system('dmimgcalc "*_bgevt2_obsexp.fits" none out=bg_expscaled_%s_%s.fits op="imgout=(%s)" clobber=yes' % (E_low,E_high,op1)) #Calculates the background summed image

 #background-subtracted image
os.system('dmimgcalc "*_bgsub_%s_%s.fits" none out=evt2_bgsub_%s_%s.fits op="imgout=(%s)" clobber=yes' % (E_low,E_high,E_low,E_high,op1)) 


# Remove unnecessary files
os.system('rm *_%s_%s.img' % (E_low,E_high))
os.system('rm *_bgevt2_obsexp.fits')
#os.system('rm *_bgsub_500_7000.fits')

