#!/usr/bin/env python

import os
import sys
import glob
import subprocess
import math

# obsids=['15173', '15174', '16263', '16264', '904']  # Abell 85

# obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795

# obsids = ['922', '6934', '7329', '19596', '19597', '19598', '20626', '20627', '20628', '20629', '20805', '20806', '20811', '20817'] # Abell 2597

#obsids = ['3231','15187'] #Abell 2319
#obsids = ['4203'] #Abell 3571

#obsids = ['17481'] #Triangulum '1227','1281',

#obsids = ['10743','577'] #A754 ,'6797'

#obsids = ['5005','7692','15186','16564','16565'] #Abell 2142 '1196','1228',

#obsids = ['497','498','10748','10803','10804','10805'] #Abell 2199

#obsids = ['5751','5752','5753','6292','6295','6296','7686','889'] #Abell 3667

#obsids = ['1669','6102','6928','7231','7232','7233'] #Abell 478

#obsids = ['5830','5831','6225','6226','6228','6229','6250','6252'] #CygnusA

#obsids = ['575','576','2208','2330','2331','2332','2333','2334','4969','4970'] #HydraA

#obsids = ['493','494','5286','5290','6159','6163','10901','12026','12029','13106','13113','14269','14275','15485','15490','17228'] #A1795

#obsids = ['904','15173','15174','16263','16264'] #A85

#obsids = ['899','7687'] #A3266

#obsids = ['5796','6257'] #HerculesA

#obsids = ['517','5826','7212'] #M87
obsids = ['495', '49896',  '6880',  '7370'] #A1835
#obsids = ['5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052

#obsids = ['891','4977','6101'] # Abell 2029 '4977' causing issues

#obsids = ['504', '505', '4954','4955','5310','16223','16224','16534','16607','16608','16609','16610'] #Centaurus

#obsids = ['16142','16143','16464','16626','16627','16633','16634','16635','16645','3200'] #Ophichius 

#obsids = ['9714','10672','13394','13395','13396','14406','14410','14411'] #Coma

#obsids = ['502','1513','3209','4289','4946','4947','4948','4949','6139','6145','11713','11714'] #Abell 426

#obsids = ['3231'] #Abell 2319 '15187',

#obsids = ['4197','10468','10470','10471','10822','10918','10922','16275'] #MS0735

#obsids = ['908','11717','12016','12017','12018'] #AWM7

#obsids = ['2218','2219'] #3C129

# obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix

# obsids= ['495', '496', '6880', '6881', '7370'] # Abell 1835

# obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664

# obsids = ['508', '2427', '6103', '7694', '12881'] # PKS0745

# obsids = ['4197', '10468', '10469', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421

# obsids = ['506', '507', '2222', '3592', '13516', '13999', '14407'] # MACSJ1347-11

# obsids = ['2208','2330','2331','2332','2333','2334','4969', '4970'] # Hydra-A

# obsids = ['4935', '5793', '17197', '17669', '17670'] # RXCJ1504

# obsids = ['2203', '9897', '13518'] # Abell 133

# obsids = ['2018', '6949', '7321', '7322'] # IC1262

# obsids = ['2215', '7921'] # AAbell 262

# obsids = ['3192', '16136'] # Abell 2626

# obsids = ['798', '9399', '17195', '17196', '17653', '17654', '17666'] # NGC 5044

# obsids = ['543', '7709', '4192']  # Zw 7160

# obsids = ['1668', '11758']  # AS1101

# obsids = ['909', '1651', '9371']  # ZwCl 3146

# obsids = ['497', '498', '10748', '10803', '10804', '10805']  # Abell 2199

# obsids = ['1657', '4195']  # MACS1423+24

# obsids = ['3195', '7706', '12903']  # Zw 2701

# obsids = ['8266']  # RXCJ1539


for obs in obsids:
    os.chdir('%s/' % (obs))
    os.system('mkdir backgrounds')
    os.chdir('backgrounds/')
    os.system('cp ../reprocess/acis*evt* .')
    os.system('cp ../reprocess/*asol1.lis .')
    os.system('cp ../reprocess/chips.reg .')


    ## read chips for each observation
    evt2_reproj = glob.glob('../reprocess/*reproj_evt2.fits')[0]
    det = str(subprocess.check_output('dmkeypar %s detnam echo=yes' %
              (evt2_reproj), shell=True)[0:-1])
    print(det)
    chips = []
    for ccd in det.split('-')[1]:
        chips.append(ccd)
    print(chips)

    for ccd in chips:
        if ccd not in ['0', '1', '2', '3', '5', '6', '7', '8']:
            chips.remove(ccd)
    print(chips)
    
    if "'" in chips:
        chips.remove("'")
    print(chips)

    factor = 10000.0
    evt2 = glob.glob('acisf?????_evt2.fits')[0]
    print(evt2,"HERE")
    asp = '@'+glob.glob('*asol1.lis')[0]
    exp_obs = float(subprocess.check_output(
        'dmkeypar %s exposure echo=yes' % (evt2), shell=True))
    for ccd_id in chips:
        print(ccd_id)
        print("HERE")
        os.system('exec ../../../scripts/pre_extract/makeblanksky_auto.sh %s' % (ccd_id))
        bgevt2 = 'bgevt2_c'+str(ccd_id)+'_reproj.fits' #bgevt2 = 'evt2_c'+str(ccd_id)+'_bg.fits' ORIGINAL
        exp_bg = float(subprocess.check_output('dmkeypar %s exposure echo=yes' % (bgevt2), shell=True))

        if exp_bg/exp_obs < factor:
            factor = exp_bg/exp_obs
            print(factor)
        else:
            continue

    x = int(math.floor(factor))
    print("HERE1")
    os.system(
        'exec /home/neolnx/Documents/XRISMprep/scripts/pre_extract/sumblankskyfields.py %s bgevt2_c?_reproj.fits' % (x))  #evt2_c?_bg.fits
    print("HERE2")
    os.system('punlearn reproject_events')
    print("HERE3")
    os.system('reproject_events bgevt2_sum_obsexpx%s.fits temp.fits aspect=none match=%s random=0' % (
        x, evt2_reproj))
    print("HERE4")
    os.system('rm bgevt2_sum_obsexpx%s.fits' % (x))
    os.system('mv temp.fits bgevt2_sum_obsexpx%s.fits' % (x))
    os.chdir('../../')
