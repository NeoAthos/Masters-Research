#!/usr/bin/env python

import numpy
import os
import sys
import glob
import subprocess

""" Code to calculate corrective factor for projct keywords due to chip gaps, point sources, bad pixels """

def make_asphist(asol,asphistname,evt2name,chip):

    # Create aspect histogram
    os.system('punlearn asphist')
    os.system('asphist infile=%s outfile=%s evtfile="%s[ccd_id=%s]" clobber=no' % (asol,asphistname,evt2name,chip))

def make_instmap(instmapname,asphistname,pbkfilename,chip,Monoenergy):

    # Create instrument map
    os.system('punlearn mkinstmap')
    #os.system('mkinstmap outfile=%s pixelgrid="1:1024:#1024,1:1024:#1024" obsfile="%s[asphist]" pbkfile=NONE dafile=NONE mirror="HRMA;AREA=1" detsubsys="ACIS-%s;IDEAL" monoenergy=%s grating=NONE spectrumfile=NONE maskfile=NONE clobber=yes' % (instmapname,asphistname,chip,Monoenergy))
    os.system('mkinstmap outfile=%s pixelgrid="1:1024:#1024,1:1024:#1024" obsfile="%s[asphist]" pbkfile=%s dafile=NONE mirror="HRMA;AREA=1" detsubsys="ACIS-%s;IDEAL" monoenergy=%s grating=NONE spectrumfile=NONE maskfile=NONE clobber=no' % (instmapname,asphistname,pbkfilename,chip,Monoenergy))

def make_expmap(evt2img,asphistname,expmapname,instmapname):

    # Create exposure map
    os.system('get_sky_limits %s > temp.dat' % (evt2img))
    with open('temp.dat','r') as f:
        for line in f:
            xybounds=line.split()[0]
    os.system('punlearn mkexpmap')
    os.system('mkexpmap asphistfile=%s outfile=%s instmapfile=%s normalize=yes xygrid="%s" useavgaspect=no clobber=no' % (asphistname,expmapname,instmapname,xybounds))
    os.remove('temp.dat')

def calculate_ratio(expmapname,regname):
    
    # Calculate ratio of effective area to annulus area
    os.system('punlearn dmstat')
    os.system('dmstat "%s[sky=region(%s)]" centroid=no verbose=0' % (expmapname,regname))
    ratio = float(subprocess.check_output('pget dmstat out_mean', shell=True))
    print(ratio)
    return ratio

def get_exposures(evt2name):

    # Get exposure time for each obsid
    exposure = float(subprocess.check_output('dmkeypar %s exposure echo=yes' % (evt2name), shell=True)[:-1])
    return exposure

def create_files(path,obsids,E_low,E_high,Monoenergy):

    exposures=[]
    fout = open('area_corr.txt', 'a')

    
    for i,obs in enumerate(obsids):
        
        #onchip=onchip0[i]

        print("Processing obs. id %s ..." % obs)
        obsidpath = path + str(obs)

        # Construct parameter list
        evtpath = path

        evt2_reproj=obsidpath+'/reprocess/' + str(obs) + '_reproj_evt2.fits'
        os.system('punlearn dmkeypar')
        det=str(subprocess.check_output('dmkeypar %s detnam echo=yes' %(evt2_reproj),shell=True)[0:-1]).split('-')[1]
        chips=[]
        for ccd in det[0:-1]:
            chips.append(ccd)
        print('DETNAM:',chips)

        os.system('punlearn ardlib')
        os.system('acis_set_ardlib %s/reprocess/acisf*_new_bpix1.fits' %(obsidpath))

        print('Make binned image of evt file:')
        os.system('punlearn dmcopy')
        os.system('dmcopy "%s[energy=%s:%s][bin sky=1][opt mem=135]" %s_%s_%s_evt2img.fits clobber=no' % (evt2_reproj, E_low, E_high, obs,E_low, E_high))


        for chip in chips:

            print('Processing ccd_id:', chip)

            params = {'evt2': evtpath + str(obs) +  '/reprocess/' + str(obs) + '_reproj_evt2.fits',
                      'evt2img': str(obs) +'_'+str(E_low)+'_'+str(E_high)+'_evt2img.fits',
                      'bpix': glob.glob(obsidpath + '/reprocess/acisf*_new_bpix1.fits')[0],
                      'asol': glob.glob(obsidpath + '/reprocess/pcadf*_asol1.fits')[0],
                      'pbk': glob.glob(obsidpath + '/reprocess/acisf*_pbk0.fits')[0],
                      'msk': glob.glob(obsidpath + '/reprocess/acisf*_msk1.fits')[0],
                      'asphist': str(obs) + '_asphist_c' + str(chip) + '.fits',
                      'instmap': str(obs) + '_instmap_c' + str(chip) + '.fits',
                      'expmap': str(obs) + '_expmap_c' +str(chip)+'_'+str(E_low)+'_'+str(E_high) + '.fits',
                      }

            print('Make asphist:')
            make_asphist(params['asol'],params['asphist'],params['evt2'],chip)


            print('Make instmap:')
            make_instmap(params['instmap'],params['asphist'],params['pbk'],chip,Monoenergy)

            print('Make expmap:')
            make_expmap(params['evt2img'],params['asphist'],params['expmap'],params['instmap'])


        # Get exposures to weight the summed exposure map
        # params = {'evt2': path + str(obs) +  '/reprocess/' + str(obs) + '_reproj_evt2.fits'} ##### Added by me for A1795
        exp = float(get_exposures(params['evt2']))
        exposures.append(exp)

        op=''
        for i in range(len(chips)):
            j=i+1
            op=op+'img'+str(j)+'+'
        op=op[:-1]

        print('Sum exposure maps for each obsid')
        os.system('punlearn dmimgcalc')
        os.system('dmimgcalc "%s_expmap_c?_%s_%s.fits" none out=%s_expmap_%s_%s_summed.fits op="imgout=((%s)*%f)" clobber=no' % (str(obs),str(E_low),str(E_high),str(obs),str(E_low),str(E_high),op,exp))

        
    op=''
    for i in range(len(exposures)):
        j=i+1
        op=op+'img'+str(j)+'+'
    op=op[:-1]
    exp_total = str(sum(exposures))

    # op = 'img1+img2+img3+img4+img5' ##### Added by me for A1795
    # exp_total = '717399.592284412' ##### Added by me for A1795
    # os.system('mkdir part5') ##### Added by me for A1795
    # for obs in obsids: ##### Added by me for A1795
    #     os.system('cp ' + obs + '_expmap_*_*_summed.fits ./part5/') ##### Added by me for A1795




    # # Weighted sum of exposure maps
    # os.system('dmimgcalc "*_expmap_*_*_summed.fits" none out=expmap_%s_%s_full.fits op="imgout=((%s)/(%s))" clobber=no' % (str(E_low),str(E_high),op,exp_total))

    # os.system('dmimgcalc "expmap_*_*_full*.fits" none out=expmap_%s_%s_full.fits op="imgout=((%s)/(%s))" clobber=yes' % (str(E_low),str(E_high),op,exp_total)) ##### Added by me for A1795
    # os.system('dmimgcalc "./part5/*_expmap_*_*_summed.fits" none out=expmap_%s_%s_full1.fits op="imgout=(%s)" clobber=yes' % (str(E_low),str(E_high),op)) ##### Added by me for A1795
    # os.system('rm -rf part5') ##### Added by me for A1795

    # expmap_file='expmap_'+str(E_low)+'_'+str(E_high)+'_full.fits'


    for reg in regions:

        # ratio = str( calculate_ratio(expmap_file,reg) ) 

        # print('region ratio: %s' %(ratio))
        # spec = glob.glob(reg[:-4]+'_sum_spec.pi')[0]
        # if len(glob.glob(reg[:-4]+'_sum_grp100.pi')) != 0: 
        #     grpspec = glob.glob(reg[:-4]+'_sum_grp100.pi')[0]
        # else:
        #     grpspec = glob.glob(reg[:-4]+'_sum_grp30.pi')[0]
        #     # grpspec = glob.glob(reg[:-4]+'_sum_grp15.pi')[0]
        # bgspec = glob.glob(reg[:-4]+'_sum_bgspec.pi')[0]

        # # Add area scaling as keyword to spectral header
        # os.system('punlearn dmhedit')
        # os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (spec,ratio))
        # os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (grpspec,ratio))
        # os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (bgspec,ratio))

        # # Output ratio values to a file
        # fout.write(str(reg)+' '+str(ratio)+'\n')

        # # Add scaling to each individual spectrum.
        # # This is for when ARF summing isn't viable, and all spectra must be fit simultaneously

        for obs in obsids:
            expmap = str(obs)+'_expmap_'+str(E_low)+'_'+str(E_high)+'_summed.fits'
            # spec = reg[:-4]+'_'+str(obs)+'_grp30.pi'
            spec = reg[:-4]+'_'+str(obs)+'_grp100.pi'
            
            bgspec = reg[:-4]+'_'+str(obs)+'_bgspec.pi'

            if os.path.isfile('%s' % (spec)) == True:
                exp = float(subprocess.check_output('dmkeypar %s EXPOSURE echo=yes' % (spec), shell=True)[:-1])
                ratio = str( calculate_ratio(expmap,reg)/exp )
                
                print('obsid ratio: %s!' %(ratio))
                
                os.system('punlearn dmhedit')
                os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (spec,ratio))
                os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (bgspec,ratio))
                
            else:
                continue



if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.stderr.write("Usage %s path_to_obsids E_low E_high Monoenergy" % sys.argv[3])
        sys.exit(1)
 

    # Run in regions directory, supply path from there to obsids
    path = str(sys.argv[1])
    E_low=sys.argv[2]
    E_high=sys.argv[3]
    Menergy=sys.argv[4]
   
      # Define function that separates integer from region*.reg
    split = lambda x: int( x.split('region')[1].split('.')[0] )
    # split = lambda x: int( x.split('cavity')[1].split('.')[0] )

    # Get list of regions
#    regions = glob.glob('center.reg')
    regions = sorted( glob.glob('region*.reg') , key=split ) 
    # regions = sorted( glob.glob('cavity*.reg') , key=split ) 
    regions = filter(lambda x: split(x) >= 0, regions) 


    # obsids = ['904', '15173', '15174', '16263', '16264'] # Abell 85
    #obsids = ['891', '4977', '6101'] # Abell 2029
    #obsids = ['4197', '10468', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421
    #obsids = ['908','11717','12016','12017','12018']
    #obsids = ['504', '505', '4954','4955','5310','16223','16224','16534','16607','16608','16609','16610'] #Centaurus 
    #obsids = ['16142','16143','16464','16626','16627','16633','16634','16635','16645','3200'] #Ophichius 
    #obsids = ['2218','2219'] #3C129
    #obsids = ['3231','15187'] #Abell 2319
    #obsids = ['4203'] #Abell 3571
    #obsids = ['9714','10672','14406','14410','14411'] #Coma
    #obsids = ['10743','577'] #A754 '6797',
    #obsids = ['5005','7692','15186','16564','16565'] #Abell 2142 '1196','1228',
    #obsids = ['497','498','10748','10803','10804','10805'] #Abell 2199
    #obsids = ['1669','6102'] #Abell 478
    #obsids = ['5751','5752','5753','6292','6295','6296','7686','889'] #Abell 3667
    #obsids = ['575','576','4969','4970'] #HydraA ,'2208','2330','2331','2332','2333','2334'
    #obsids = ['6226','6228','6229','6250','6252'] #CygnusA '5830','5831','6225',
    #obsids = ['14269','14275','15485','15490','17228'] #A1795
    #obsids = ['5796','6257'] #HerculesA
    obsids = ['517','5826','7212'] #M87
    #obsids = ['1513','3209','4289','4946','4947','4948','4949','6139','6145','11713','11714'] #Abell 426
    #obsids = ['4203']  #A3571
    # obsids = ['4197','10468','10470','10471','10822','10918','10922','16275'] #MS0735
    # obsids = ['495', '496', '6880', '6881', '7370'] # Abell 1835
    # obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix
    # obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664
    # obsids = ['19596', '19598', '20627', '20629', '20806', '20817', '7329', '19597', '20626', '20628', '20805', '20811', '6934', '922'] # Abell 2597
    # obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix
    #obsids = ['5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052
    # obsids = ['508', '2427', '6103', '7694', '12881'] # PKS0745
    # obsids = ['506', '507', '2222', '3592', '13516', '13999', '14407'] # MACSJ1347-11
    # obsids = ['4197', '10468', '10469', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421
    # obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795
    # obsids = ['4969', '4970'] # Hydra-A
    # obsids = ['4935', '5793', '17197', '17669', '17670'] # RXCJ1504
    # obsids = ['2203', '9897', '13518'] # Abell 133
    # obsids = ['2018', '6949', '7321', '7322'] # IC1262
    # obsids = ['2215', '7921'] # Abell 262
    # obsids = ['3192', '16136'] # Abell 2626
    # obsids = ['798', '9399', '17195', '17196', '17653', '17654', '17666'] # NGC 5044
    # obsids = ['543', '4192', '7709'] # Zw 7160
    # obsids = ['1668', '11758']  # AS1101
    # obsids = ['909', '1651', '9371']  # ZwCl 3146
    #obsids = ['497', '498', '10748', '10803', '10804', '10805']  # Abell 2199
    # obsids = ['1657', '4195']  # MACS1423+24
    # obsids = ['3195', '7706', '12903']  # Zw 2701
    # obsids = ['8266']  # RXCJ1539
    
    create_files(path,obsids,E_low,E_high,Menergy)

    os.system('rm *asphist*')
    os.system('rm *instmap*')
    os.system('rm *_expmap_c*')
    os.system('rm *img.fits')
