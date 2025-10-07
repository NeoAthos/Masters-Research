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

# obsids=['15173', '15174', '16263', '16264', '904'] # Abell 85

# obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795

# obsids = ['922', '6934', '7329', '19596', '19597', '19598', '20626', '20627', '20628', '20629', '20805', '20806', '20811', '20817'] # Abell 2597


#obsids = ['3231','15187'] #Abell 2319 

#obsids = ['4203'] #Abell 3571

#obsids = ['5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052

#obsids = ['3231'] #A2319 '15187',

#obsids = ['502','1513','3209','4289','4946','4947','4948','4949','6139','6145','11713','11714'] #Abell 426

#obsids = ['9714','10672','14406','14410','14411'] #Coma

#obsids = ['10743','577'] #A754 '6797',

#obsids = ['5005','7692','15186','16564','16565'] #Abell 2142 '1196','1228',

#obsids = ['6226','6228','6229','6250','6252'] #CygnusA '5830','5831','6225',

#obsids = ['576','4969','4970'] #HydraA '575','2208','2330','2331','2332','2333','2334'

#obsids = ['891', '4977', '6101'] # Abell 2029

#obsids = ['899','7687'] #A3266

#obsids = ['5796','6257'] #HerculesA
#obsids = ['517','5826','7212'] #M87
obsids = ['495', '49896',  '6880',  '7370'] #A1835
#obsids = ['14269','14275','15485','15490','17228'] #A1795 ,'10901','12026', '12029','13106','13113',,
#'14269','14275','6159','6163'
#good '493','494','5286','5290'

#obsids = ['904','15173','15174','16263','16264'] #A85

#obsids = ['899','7687'] #A3266


#obsids = ['1669','6102'] #Abell 478,'6928','7231','7232','7233'

#obsids = ['497','498','10748','10803','10804','10805'] #Abell 2199

#obsids = ['5751','5752','5753','6292','6295','6296','7686','889'] #Abell 3667

#obsids = ['4203'] #Abell 3571

#obsids = ['4197','10468','10470','10471','10822','10918','10922','16275'] #MS0735

#obsids = ['891', '4977', '6101'] # Abell 2029

#obsids = ['504', '505', '4954','4955','5310','16223','16224','16534','16607','16608','16609','16610'] #Centaurus 

#obsids = ['16142','16143','16464','16626','16627','16633','16634','16635','16645','3200'] #Ophichius 

# obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix

# obsids= ['495', '496', '6880', '6881', '7370'] # Abell 1835

# obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664

# obsids = ['508', '2427', '6103', '7694', '12881'] # PKS0745

#obsids = ['4197', '10468', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421

#obsids = ['908','11717','12016','12017','12018'] #AWM7

#obsids = ['2218','2219'] #3C129

#obsids = ['17481'] #Triangulum

# obsids = ['506', '507', '2222', '3592', '13516', '13999', '14407'] # MACSJ1347-11

# obsids = ['2208','2330','2331','2332','2333','2334'] # Hydra-A ,'4969', '4970'

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

    # Chop summed background files to energy range, then normalize to the observation's exposure time
    x=glob.glob('bgevt2_sum_obsexpx*')[0]
    x=x.split('bgevt2_sum_obsexpx')[1]
    x=int(x.split('.fits')[0])

    os.system('dmcopy "bgevt2_sum_obsexpx%s.fits[energy=%s:%s][bin sky=1][opt mem=150]" bgtemp.fits clobber=yes' % (x,E_low,E_high))  
    os.system('dmimgcalc "bgtemp.fits" none out=%s_bgevt2_obsexp.fits op="imgout=((img1)/%f)" clobber=yes' % (obs,x))  

    os.system('dmimgcalc "%s_%s_%s.img,%s_bgevt2_obsexp.fits" none out=%s_bgsub_%s_%s.fits op="imgout=(img1-img2)" clobber=yes' %(obs, E_low, E_high,obs,obs, E_low, E_high))


    os.system('rm bgevt2_sum_obsexpx*.fits')
    os.system('rm bgtemp.fits')



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

