#!/usr/bin/env python
import numpy
import os
import sys
import glob
from astropy.io import fits as pyfits
import pdb
from subprocess import check_output


import subprocess
import math



print("running")
""" Code to extract spectra from regions produced by contour binning """

def make_spectrum(evt2name,region,specname):

    os.system('punlearn dmextract')
    os.system('dmextract %s"[sky=region(%s)][bin pi]" %s wmap="[energy=500:7000][bin det=8]" error=gaussian' % (evt2name,region,specname))

def make_background(bgevt2name,region,bgspecname): 

    os.system('punlearn dmextract')
    os.system('dmextract %s"[sky=region(%s)][bin pi]" %s error=gaussian' % (bgevt2name, region, bgspecname))

def set_ardlib(bpixname):

    os.system('punlearn ardlib')
    os.system('acis_set_ardlib %s absolutepath=yes' % bpixname)

def getregioncounts(evt2name,regionfile):

   #   # Create image
   #  os.system('punlearn dmcopy')
   #  os.system('dmcopy "%s[sky=region(%s)][energy=500:7000][bin sky=1]" img.fits' % (evt2name,regionfile))
   #  os.system('punlearn dmstat')
   #  os.system('dmstat "img.fits[sky=region(%s)]" centroid=no' % regionfile)
   #  counts = float( check_output('pget dmstat out_sum', shell=True) )
   # # os.remove('img.fits')

    # return counts
    #Create image
    global total_counts
    os.system('punlearn dmcopy')
    print(evt2name)
    print(regionfile)
    os.system('dmcopy "%s[sky=region(%s)][energy=500:7000][bin sky=1]" img.fits' %(evt2name,regionfile))

    os.system('punlearn dmstat')
    os.system('dmstat "img.fits[sky=region(%s)]" centroid=no' % regionfile)
    os.system('pget dmstat out_sum > temp.dat')
    ctsfile = open('temp.dat','r')
    try:
        counts = float(ctsfile.read()) 
        print(counts)
        total_counts+=counts
        print(total_counts)
        print("THIS IS THE COUNTS VALUE")
    except ValueError:
        pdb.set_trace()
    ctsfile.close()
    os.remove('temp.dat')
    os.remove('img.fits')
    
    return counts

def make_asphist(asol,asphistname,evt2name,chip):

    os.system('punlearn asphist')
    os.system('asphist infile=%s outfile=%s evtfile="%s[ccd_id=%d]"' % (asol,asphistname,evt2name,chip))

def make_wmap(evt2name,regionfile,asphistname,wmapname):
    
    os.system('punlearn sky2tdet')
    os.system('sky2tdet "%s[energy=500:7000][sky=region(%s)][bin sky=1]" %s "%s[wmap]"' % (evt2name,regionfile,asphistname,wmapname))

def make_arf(wmapname,arfname,weightname,pbkfile,mskfile):

    os.system('punlearn mkwarf')
    os.system('mkwarf infile="%s[WMAP]" outfile=%s egridspec=0.3:9.5:0.005 threshold=0 weightfile=%s spectrumfile="" clobber=yes pbkfile="%s" dafile=CALDB mskfile="%s"' % (wmapname,arfname,weightname,pbkfile,mskfile))

def make_rmf(rmfout,spec,asol):

    os.system('punlearn mkacisrmf')
    os.system('mkacisrmf infile=CALDB outfile=%s energy=0.3:9.5:0.005 channel=1:1024:1 chantype=PI wmap="%s[WMAP]" gain=CALDB asolfile=%s' % (rmfout,spec,asol))

def make_weightmap(evt2name,regionname,weightname):
    
    os.system('punlearn dmcopy')
    os.system('dmcopy "%s[sky=region(%s)][energy=500:7000][bin det=8]" %s' % (evt2name,regionname,weightname))

def add_spectra(spectra,specout):

    # Generate expr string
    exprstr = spectra[0]
    for spec in spectra[1:]:
        exprstr += '+%s' % spec

    # BACKSCAL keyword is taken from first spectrum
    hdulist = pyfits.open(spectra[0])
    backscalval = hdulist[1].header['BACKSCAL']
    hdulist.close()

    # Sum spectra
    os.system('punlearn mathpha')
    os.system('mathpha expr="%s" units="C" outfil="%s" exposure="CALC" areascal="NULL" backscal=%e ncomments=1 ERRMETH="POISS-0" comment1="Added files %s with MATHPHA"' % (exprstr,specout,backscalval,exprstr))

def add_arfs(arffiles,arfout,weights):

    # Generate expr string
    exprstr = arffiles[0]
    wgtstr = str(weights[0])
    for arf,wgt in zip(arffiles[1:],weights[1:]):
        exprstr += ',%s' % arf
        wgtstr += ',%f' % wgt
        
    os.system('punlearn addarf')
    os.system('addarf %s %s %s' % (exprstr,wgtstr,arfout))

def add_rmfs(rmffiles,rmfout,weights):

    # Generate expr string
    exprstr = rmffiles[0]
    wgtstr = str(weights[0])
    for rmf,wgt in zip(rmffiles[1:],weights[1:]):
        exprstr += ',%s' % rmf
        wgtstr += ',%f' % wgt
        
    os.system('punlearn addrmf')
    os.system('addrmf %s %s %s' % (exprstr,wgtstr,rmfout))

def generate_spectra(path,obsids,regionfile):

    weights = []
    weightmaps = []
    spectra = []
    bgspectra = []
    arffiles = []
    rmffiles = []
    sumweightmap = regionfile[:-4] + '_sum_detmap.fits'
    global grplist





    #for obs in zip(obsids,onchip):
    for obs in obsids:
        obs=int(obs)

        weights = []
        weightmaps = []
        spectra = []
        bgspectra = []
        arffiles = []
        rmffiles = []
        sumweightmap = regionfile[:-4] + '_sum_detmap.fits'

        print(obs)

        term=str(obs)+'/reprocess/'+str(obs)+'_reproj_evt2.fits'
        print(term)

        evt2_reproj=glob.glob(term)[0] 
        det=str(subprocess.check_output('dmkeypar %s detnam echo=yes' %(evt2_reproj),shell=True)[0:-1])
        print(det)
        onchip=[]
        for ccd in det.split('-')[1]:
            onchip.append(ccd)
        onchip=onchip[0:len(onchip)-1]
        print(onchip)
        chip=onchip[1]
        chip=int(chip)
        print('chip:',chip)


        print("Processing obs. id %s ..." % obs)
        
        obsidpath = path + str(obs)
        
    
        # Construct parameter list
#        evtpath = path + 'merge/'
        evtpath = path
        name = '%s_%s' % (regionfile[:-4],str(obs))
        print(obsidpath)
        params = {'evt2': evtpath + str(obs) +  '/reprocess/' + str(obs) + '_reproj_evt2.fits',
                  #'bgevt2': evtpath + str(obs) + '/reprocess/' + str(obs) + '_reproj_bgevt2.fits',
                  #'bgevt2': evtpath + str(obs) + '/reprocess/bgevt2_c3*reproj.fits',
                  'bgevt2': evtpath + str(obs) + '/backgrounds/bgevt2_sum_obsexp*.fits',
                  'bpix': glob.glob(obsidpath + '/reprocess/acisf*_new_bpix1.fits')[0],
                  'reg': regionfile,
                  'spec': '%s_spec.pi' % name,
                  'bgspec': '%s_bgspec.pi' % name,
                  'rmf': '%s.rmf' % name,
                  'arf': '%s.arf' % name,
                  'weight': '%s.weight' % name,
                  'detmap': '%s_detmap.fits' % name,
                  'asol': glob.glob(obsidpath + '/reprocess/pcadf*_asol1.fits')[0],
                  'pbk': glob.glob(obsidpath + '/reprocess/acisf*_pbk0.fits')[0],
                  'msk': glob.glob(obsidpath + '/reprocess/acisf*_msk1.fits')[0],
                  'wmap': '%s_tdet.fits' % name,
                  'asphist': str(obs) + '_asphist_c' + str(chip) + '.fits'
                  }



        # Determine whether region is on chip, get region counts 0.5-7keV
        ctsweight = getregioncounts(params['evt2'],params['reg'])
        print(ctsweight)
        if ctsweight < 1.0:
            print("Region off chip, excluding this obs. id.")

            tempval = numpy.array(obsids)
            print(tempval)
            indexval = numpy.where(tempval==str(obs))[0][0]
            print(indexval)

            # Modify onchip and obsids
            #onchip.pop(indexval)
            #obsids.pop(indexval)
            print(obsids)
            print(onchip)
            continue
      
        
        # Make spectra!
        set_ardlib(params['bpix'])
        print("Extracting spectra ...")
        make_spectrum(params['evt2'],params['reg'],params['spec'])
        print("Extracting background spectra ...")
        make_background(params['bgevt2'],params['reg'],params['bgspec'])

        if not os.path.exists(params['asphist']):
            make_asphist(params['asol'],params['asphist'],params['evt2'],chip)

        print("Making Weight Map ...")
        make_wmap(params['evt2'],params['reg'],params['asphist'],params['wmap'])
        print("Making ARF ...")
        make_arf(params['wmap'],params['arf'],params['weight'],params['pbk'],params['msk'])
        print("Making RMF ...")
        make_rmf(params['rmf'],params['spec'],params['asol'])

        # And group the spectra if needed:
        grpout = '%s_grp100.pi' % name
        grplist.append(grpout)
        os.system('punlearn grppha')
        os.system('grppha infile="%s" outfile="%s" chatter=0 comm="group min 100 & chkey BACKFILE %s & chkey RESPFILE %s & chkey ANCRFILE %s & exit"' % (params['spec'],grpout,params['bgspec'],params['rmf'],params['arf']))

        # Get weight for total arf
        weights.append(ctsweight)
        spectra.append(params['spec'])
        bgspectra.append(params['bgspec'])
        arffiles.append(params['arf'])
        rmffiles.append(params['rmf'])

    # Turn into arrays
    weights = numpy.array(weights)
    spectra = numpy.array(spectra)
    bgspectra = numpy.array(bgspectra)
    arffiles = numpy.array(arffiles)
    rmffiles = numpy.array(rmffiles)

    #print(onchip, obsids)

    # Sum together all spectra!

    sclweights = weights/sum(weights)

    # Workaround to avoid segfault from adding too many spectra simultaneously
    # (Happens when adding ~18+ spectra)
    print('len spectra={}'.format(len(spectra)))
    x = (len(spectra)-1)//10 +1
    print('x is: {}'.format(x))
    dummy_weights = []
    specout = regionfile[:-4] + '_sum_spec.pi'
    bgspecout = regionfile[:-4] + '_sum_bgspec.pi'
    arfout = regionfile[:-4] + '_sum.arf'
    rmfout = regionfile[:-4] + '_sum.rmf'

    if x > 1:
        for i in range(x):
            dummy_weights.append(1.0)

            specout_temp='spec'+str(i)+'temp.pi'
            spectra_temp=spectra[10*i:10*i+10]

            bgspecout_temp='bgspec'+str(i)+'temp.pi'
            bgspectra_temp=bgspectra[10*i:10*i+10]

            arfout_temp='arf'+str(i)+'temp.arf'
            arffiles_temp=arffiles[10*i:10*i+10]

            rmfout_temp='rmf'+str(i)+'temp.rmf'
            rmffiles_temp=rmffiles[10*i:10*i+10]

            sclweights_temp=sclweights[10*i:10*i+10]

            add_spectra(spectra_temp,specout_temp)
            add_spectra(bgspectra_temp,bgspecout_temp)
            add_arfs(arffiles_temp,arfout_temp,sclweights_temp)
            add_rmfs(rmffiles_temp,rmfout_temp,sclweights_temp)

        spectra_temp=glob.glob('spec*temp.pi')
        bgspectra_temp=glob.glob('bgspec*temp.pi')
        arffiles_temp=glob.glob('*temp.arf')
        rmffiles_temp=glob.glob('*temp.rmf')

        print("Summing spectra ...")
        add_spectra(spectra_temp,specout)

        print("Summing background spectra ...")
        add_spectra(bgspectra_temp,bgspecout)

        print("Weighting total arf by counts ...")       
        add_arfs(arffiles_temp,arfout,dummy_weights)

        print("Generating rmfs ...")      
        add_rmfs(rmffiles_temp,rmfout,dummy_weights)        

        os.system('rm *spec*temp.pi')
        os.system('rm *temp.*f')

    else:
        print("Summing spectra ...")
        print(spectra)       
        add_spectra(spectra,specout)

        print("Summing background spectra ...")      
        add_spectra(bgspectra,bgspecout)
  
    # Produce weighted arf file
        print("Weighting total arf by counts ...")        
        add_arfs(arffiles,arfout,sclweights)

    # Run mkacisrmf on total weight map
        print("Generating rmfs ...")       
        add_rmfs(rmffiles,rmfout,sclweights)

    # Group spectra
    print("Grouping spectrum ...")
    grpout = regionfile[:-4] + '_sum_grp100.pi'
    combine_name = regionfile[:-4] + '_sum'
    os.system('punlearn grppha')
    os.system('grppha infile="%s" outfile="%s" chatter=0 comm="group min 30 & chkey BACKFILE %s & chkey RESPFILE %s & chkey ANCRFILE %s & exit"' % (specout,grpout,bgspecout,rmfout,arfout))

    # Update spec header
    os.system('punlearn dmhedit')
    os.system("""dmhedit %s filelist=none operation=add key=ANCRFILE value="'%s'" datatype=string""" % (specout,arfout))
    os.system('punlearn dmhedit')
    os.system("""dmhedit %s filelist=none operation=add key=RESPFILE value="'%s'" datatype=string""" % (specout,rmfout))
    os.system('punlearn dmhedit')
    os.system("""dmhedit %s filelist=none operation=add key=BACKFILE value="'%s'" datatype=string""" % (specout,bgspecout))
    grplist = ', '.join(grplist)
    os.system("combine_spectra src_spectra='%s' outroot=%s " % (grplist,combine_name))

    # Remove files?
#    for i in xrange(len(spectra)):
#        os.remove(spectra[i])
#        os.remove(bgspectra[i])
#        os.remove(arffiles[i])
#        os.remove(rmffiles[i])
        
    os.system('rm *.weight')
    os.system('rm *_tdet.fits')
    grplist = []

if __name__ == "__main__":
    print("here")
    if len(sys.argv) != 2:
        sys.stderr.write("Usage %s path_to_obsids" % sys.argv[0])
        sys.exit(1)

    # Run in regions directory, supply path from there to obsids
    path = str(sys.argv[1])
    print(path)
    total_counts = 0
    grplist = []		#for combining spectra properly
    # Define function that separates integer from region*.reg
    # split = lambda x: int( x.split('region')[1].split('.')[0] )
    #split = lambda x: int( x.split('xaf_')[1].split('.')[0] ) #Extracting Spectra for Maps
    
    #split = lambda x: int( x.split('region')[1].split('.')[0] ) #Extracting Spectra for Profiles (uncomment)
    #print(split)
    split = lambda x: ( x.split('XRISM_regionN')[1].split('.')[0] ) #Extracting Spectra for Profiles
    #split = lambda x: ( x.split('XRISM_shift1')[1].split('.')[0] ) #Extracting Spectra for Profiles
    #print(split)
    # split = lambda x: int( x.split('offjet2_')[1].split('.')[0] ) #Extracting Spectra for Profiles relative to jet direction

    # Get list of regions
    
    #regions = sorted( glob.glob('region*.reg') , key=split ) #Extracting Spectra for Maps NORMAL UNCHECK THIS
    
    regions = sorted( glob.glob('XRISM_regionN.reg') , key=split ) #Extracting Spectra for XRISM
    #regions = sorted( glob.glob('XRISM_shift1.reg') , key=split ) #Extracting Spectra for XRISM
    # regions = sorted( glob.glob('offjet2_*.reg') , key=split ) #Extracting Spectra for Profiles relative to jet direction
#    regions = glob.glob('center*.reg')

    print(regions)
    # Filter regions in case spectra extraction did not finish
    #regions = filter(lambda x: split(x) >= 0, regions) 
    #print(regions)

    #regions=['region12.reg']

    for reg in regions:

    # List of observations: 
    # Extract spectra from front and back-illuminated chips separately!
    # Only use summed spectra when confident that the ARFs are quite similar!
        #obsids=['555','556','1086','1112','1113','1114','9714','10672']
        #obsids=['891','4977','6101'] #A2029
        #obsids = ['1601', '10722', '17147'] #Centaurus
        #obsids = ['4197', '10468', '10470', '10471', '10822', '10918', '10922', '16275'] # MS0735+7421
        #'13993','13994','13995','13996','14406','14410','14411','14415']
        #obsids = ['908','11717','12016','12017','12018'] #AWM7
        #obsids = ['504', '505', '4954','4955','5310','16223','16224','16534','16607','16608','16609','16610'] #Centaurus 
        #obsids = ['16142','16143','16464','16626','16627','16633','16634','16635','16645','3200'] #Ophichius         
        #obsids = ['1513','3209','4289','4946','4947','4948','4949','6139','6145','11713','11714'] #Abell 426
        #obsids = ['3231','15187'] #Abell 2319
        #obsids = ['4203'] #Abell 3571
        #obsids = ['9714','10672','14406','14410','14411'] #Coma
        #obsids = ['10743','577'] #A754
        #obsids = ['497','498','10748','10803','10804','10805'] #Abell 2199 
        #obsids = ['5005','7692','15186','16564','16565'] #Abell 2142 '1196','1228',
        #obsids = ['4197','10468','10470','10471','10822','10918','10922','16275'] #MS0735
        #obsids = ['904','15173','15174','16263','16264']
        #obsids = ['899','7687'] #A3266
        #obsids = ['497','498','10748','10803','10804','10805'] #Abell 2199
        #obsids = ['5751','5752','5753','6292','6295','6296','7686','889'] #Abell 3667
        #obsids = ['6226','6228','6229','6250','6252'] #CygnusA '5830','5831','6225',
        #obsids = ['14269','14275','15485','15490','17228'] #A1795
        #obsids = ['495','49896','6880','7370'] #A1835
        obsids = ['576','4969','4970'] #HydraA ,'2208','2330','2331','2332','2333','2334','575',
        #obsids = ['517','5826','7212'] #M87
	#obsids = ['904','15173','15174','16263','16264'] #A85
        #obsids = ['2218','2219'] #3C129
        #obsids=['360','6225','5831','1707','6226','6250','5830','6229','6228','6252','17505','17145','17530','17650','17144','17141','17710','17528','17143','17524','18441','17526','17527','18682','18641','18683','17508','18688','17146','18846','17506','18861','18871','17133','17510','17509','17518','17521','18886','17138','17513','17516','17523','17512','17139','17517','19888','17140','17507','17520','19956','17514','17529','17519','17135','17136','19996','19989','17515','20043','20044','17137','17522','20059','17142','17525','20063','17511','20077','20048','17134','20079']
        #obsids=['360','6225','5831','1707','6226','6250','5830','6229','6228','6252','17505','17145','17530','17650','17144','17141','17710','17528','17143','17524','18441','17526','17527','18682','18641','18683','17508','18688','18846','17506','18861','18871','17133','17510','17509','17518','17521','18886','17138','17513','17516','17523','17512','17139','17517','19888','17140','17507','17520','19956','17514','17529','17519','17135','17136','19996','19989','17515','20043','20044','17137','17522','20059','17142','17525','20063','17511','20077','20048','17134','20079']
        #obsids=['18846','17506','18861','18871','17133','17510','17509','17518','17521','18886','17138','17513','17516','17523','17512','17139','17517','19888','17140','17507','17520','19956','17514','17529','17519','17135','17136','19996','19989','17515','20043','20044','17137','17522','20059','17142','17525','20063','17511','20077','20048','17134','20079']
        #obsids=['17506','17146','18688','5830','6229','6228']#,'17521','18886','17138']
        #onchip = [2,3,5,6,7,8]

        testfile = reg[:-4] + '_sumc0_grp20.pi'

        if os.path.isfile(testfile):
            continue
        else:
            generate_spectra(path,obsids,reg)
