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
    os.system('asphist infile=%s outfile=%s evtfile="%s[ccd_id=%s]" clobber=yes' % (asol,asphistname,evt2name,chip))

def make_instmap(instmapname,asphistname,pbkfilename,chip,Monoenergy):

    # Create instrument map
    os.system('punlearn mkinstmap')
    #os.system('mkinstmap outfile=%s pixelgrid="1:1024:#1024,1:1024:#1024" obsfile="%s[asphist]" pbkfile=NONE dafile=NONE mirror="HRMA;AREA=1" detsubsys="ACIS-%s;IDEAL" monoenergy=%s grating=NONE spectrumfile=NONE maskfile=NONE clobber=yes' % (instmapname,asphistname,chip,Monoenergy))
    os.system('mkinstmap outfile=%s pixelgrid="1:1024:#1024,1:1024:#1024" obsfile="%s[asphist]" pbkfile=%s dafile=NONE mirror="HRMA;AREA=1" detsubsys="ACIS-%s;IDEAL" monoenergy=%s grating=NONE spectrumfile=NONE maskfile=NONE clobber=yes' % (instmapname,asphistname,pbkfilename,chip,Monoenergy))

def make_expmap(evt2img,asphistname,expmapname,instmapname):

    # Create exposure map
    os.system('get_sky_limits %s > temp.dat' % (evt2img))
    with open('temp.dat','r') as f:
        for line in f:
            xybounds=line.split()[0]
    os.system('punlearn mkexpmap')
    os.system('mkexpmap asphistfile=%s outfile=%s instmapfile=%s normalize=yes xygrid="%s" useavgaspect=no clobber=yes' % (asphistname,expmapname,instmapname,xybounds))
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
        os.system('dmcopy "%s[energy=%s:%s][bin sky=1][opt mem=135]" %s_%s_%s_evt2img.fits clobber=yes' % (evt2_reproj, E_low, E_high, obs,E_low, E_high))


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
        exp = float(get_exposures(params['evt2']))
        exposures.append(exp)

        op=''
        for i in range(len(chips)):
            j=i+1
            op=op+'img'+str(j)+'+'
        op=op[:-1]

        print('Sum exposure maps for each obsid')
        os.system('punlearn dmimgcalc')
        os.system('dmimgcalc "%s_expmap_c?_%s_%s.fits" none out=%s_expmap_%s_%s_summed.fits op="imgout=((%s)*%f)" clobber=yes' % (str(obs),str(E_low),str(E_high),str(obs),str(E_low),str(E_high),op,exp))

    op=''
    for i in range(len(exposures)):
        j=i+1
        op=op+'img'+str(j)+'+'
    op=op[:-1]
    exp_total = str(sum(exposures))



    # Weighted sum of exposure maps
    os.system('dmimgcalc "*_expmap_*_*_summed.fits" none out=expmap_%s_%s_full.fits op="imgout=((%s)/(%s))" clobber=yes' % (str(E_low),str(E_high),op,exp_total))

    expmap_file='expmap_'+str(E_low)+'_'+str(E_high)+'_full.fits'


    for reg in regions:

        ratio = str( calculate_ratio(expmap_file,reg) ) 

        print('region ratio: %s' %(ratio))
        spec = glob.glob(reg[:-4]+'_sum_spec.pi')[0]
        grpspec = glob.glob(reg[:-4]+'_sum_grp100.pi')[0]
        bgspec = glob.glob(reg[:-4]+'_sum_bgspec.pi')[0]

        # Add area scaling as keyword to spectral header
        os.system('punlearn dmhedit')
        os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (spec,ratio))
        os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (grpspec,ratio))
        os.system('dmhedit %s filelist=none operation=add key=AREASCAL value="%s" datatype=double' % (bgspec,ratio))

        # Output ratio values to a file
        fout.write(str(reg)+' '+str(ratio)+'\n')

        # Add scaling to each individual spectrum.
        # This is for when ARF summing isn't viable, and all spectra must be fit simultaneously

        for obs in obsids:
            expmap = str(obs)+'_expmap_'+str(E_low)+'_'+str(E_high)+'_summed.fits'
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

    # Get list of regions
#    regions = glob.glob('center.reg')
    regions = sorted( glob.glob('region*.reg') , key=split ) 
    regions = filter(lambda x: split(x) >= 0, regions) 


    #obsids = ['891','4977','6101']
    #obsids = ['4183','19593','20862','20863']
    obsids = ['1601', '10722', '17147'] #Centaurus #obsids=['4289','4946','4947','4948','4949','4951','4952','4953','6139','6145','6146','11713','11714','11715','11716','12025','12033','12036','12037']
    #obsids=['4960']
    #onchip0 = [[2,3,5,6,7,8],[2,3,5,6,7,8],[0,1,2,3,6]]
    #obsids = ['06101']
    #onchip0 = [[0,1,2,3,6]]
    create_files(path,obsids,E_low,E_high,Menergy)
    os.system('rm *asphist*')
    os.system('rm *instmap*')
    os.system('rm *_expmap_c*')
    os.system('rm *img.fits')
