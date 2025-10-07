#!/usr/bin/env python
import numpy
import os
import sys
import glob
from astropy.io import fits as pyfits
import pdb
from subprocess import check_output


""" Code to extract spectra from regions produced by contour binning """

def make_spectrum(evt2name,region,specname):

    #os.system('punlearn specextract combine=yes') #new
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

   #os.system('punlearn mkrmf')
    #os.system('mkrmf infile=CALDB outfile=%s energy=0.3:9.5:0.005 channel=1:1024:1 chantype=PI wmap="%s[WMAP]" gain=CALDB asolfile=%s' % (rmfout,spec,asol))

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

def generate_spectra(path,obsids,onchip,regionfile):

    weights = []
    weightmaps = []
    spectra = []
    bgspectra = []
    arffiles = []
    rmffiles = []
    sumweightmap = regionfile[:-4] + '_sum_detmap.fits'


    for obs,chip in zip(obsids,onchip):
    # for obs in obsids:
    #     obs=int(obs)

    #     weights = []
    #     weightmaps = []
    #     spectra = []
    #     bgspectra = []
    #     arffiles = []
    #     rmffiles = []
    #     sumweightmap = regionfile[:-4] + '_sum_detmap.fits'

    #     print(obs)

    #     term=str(obs)+'/reprocess/'+str(obs)+'_reproj_evt2.fits'
    #     print(term)

    #     evt2_reproj=glob.glob(term)[0] 
    #     det=str(subprocess.check_output('dmkeypar %s detnam echo=yes' %(evt2_reproj),shell=True)[0:-1])
    #     print(det)
    #     onchip=[]
    #     for ccd in det.split('-')[1]:
    #         onchip.append(ccd)
    #     onchip=onchip[0:len(onchip)-1]
    #     print(onchip)
    #     chip=onchip[1]
    #     chip=int(chip)
    #     print('chip:',chip)




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
                #   'bgevt2': evtpath + str(obs) + '/backgrounds/bgevt2_sum_obsexpx.fits',
                  'bpix': glob.glob(obsidpath + '/reprocess/acisf?????_new_bpix1.fits')[0],
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
            indexval = numpy.where(tempval==obs)[0][0]

            # Modify onchip and obsids
            onchip.pop(indexval)
            obsids.pop(indexval)
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

        # Update spec header
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=ANCRFILE value="'%s'" datatype=string""" % (
            params['spec'], params['arf']))
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=RESPFILE value="'%s'" datatype=string""" % (
            params['spec'], params['rmf']))
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=BACKFILE value="'%s'" datatype=string""" % (
            params['spec'], params['bgspec']))

        # And group the spectra if needed:
        grpout = '%s_grp30.pi' % name
        os.system('punlearn grppha')
        os.system('grppha infile="%s" outfile="%s" chatter=0 comm="group min 30 & chkey BACKFILE %s & chkey RESPFILE %s & chkey ANCRFILE %s & exit"' % (params['spec'],grpout,params['bgspec'],params['rmf'],params['arf']))

    #     # Get weight for total arf
    #     weights.append(ctsweight)
    #     spectra.append(params['spec'])
    #     bgspectra.append(params['bgspec'])
    #     arffiles.append(params['arf'])
    #     rmffiles.append(params['rmf'])

    # # Turn into arrays
    # weights = numpy.array(weights)
    # spectra = numpy.array(spectra)
    # bgspectra = numpy.array(bgspectra)
    # arffiles = numpy.array(arffiles)
    # rmffiles = numpy.array(rmffiles)

    # print(onchip, obsids)

    # # Sum together all spectra!

    # sclweights = weights/sum(weights)

    # # Workaround to avoid segfault from adding too many spectra simultaneously
    # # (Happens when adding ~18+ spectra)
    # print('len spectra={}'.format(len(spectra)))
    # x = (len(spectra)-1)//10 +1
    # print('x is: {}'.format(x))
    # dummy_weights = []
    # specout = regionfile[:-4] + '_sum_spec.pi'
    # bgspecout = regionfile[:-4] + '_sum_bgspec.pi'
    # arfout = regionfile[:-4] + '_sum.arf'
    # rmfout = regionfile[:-4] + '_sum.rmf'

    # if x > 1:
    #     for i in range(x):
    #         dummy_weights.append(1.0)

    #         specout_temp='spec'+str(i)+'temp.pi'
    #         spectra_temp=spectra[10*i:10*i+10]

    #         bgspecout_temp='bgspec'+str(i)+'temp.pi'
    #         bgspectra_temp=bgspectra[10*i:10*i+10]

    #         arfout_temp='arf'+str(i)+'temp.arf'
    #         arffiles_temp=arffiles[10*i:10*i+10]

    #         rmfout_temp='rmf'+str(i)+'temp.rmf'
    #         rmffiles_temp=rmffiles[10*i:10*i+10]

    #         sclweights_temp=sclweights[10*i:10*i+10]

    #         add_spectra(spectra_temp,specout_temp)
    #         add_spectra(bgspectra_temp,bgspecout_temp)
    #         add_arfs(arffiles_temp,arfout_temp,sclweights_temp)
    #         add_rmfs(rmffiles_temp,rmfout_temp,sclweights_temp)

    #     spectra_temp=glob.glob('spec*temp.pi')
    #     bgspectra_temp=glob.glob('bgspec*temp.pi')
    #     arffiles_temp=glob.glob('*temp.arf')
    #     rmffiles_temp=glob.glob('*temp.rmf')

    #     print("Summing spectra ...")
    #     add_spectra(spectra_temp,specout)

    #     print("Summing background spectra ...")
    #     add_spectra(bgspectra_temp,bgspecout)

    #     print("Weighting total arf by counts ...")       
    #     add_arfs(arffiles_temp,arfout,dummy_weights)

    #     print("Generating rmfs ...")      
    #     add_rmfs(rmffiles_temp,rmfout,dummy_weights)        

    #     os.system('rm *spec*temp.pi')
    #     os.system('rm *temp.*f')

    # else:
    #     print("Summing spectra ...")       
    #     add_spectra(spectra,specout)

    #     print("Summing background spectra ...")      
    #     add_spectra(bgspectra,bgspecout)
  
    # # Produce weighted arf file
    #     print("Weighting total arf by counts ...")        
    #     add_arfs(arffiles,arfout,sclweights)

    # # Run mkacisrmf on total weight map
    #     print("Generating rmfs ...")       
    #     add_rmfs(rmffiles,rmfout,sclweights)

#     #Group spectra
#    print("Grouping spectrum ...")
#    grpout = regionfile[:-4] + '_sum_grp30.pi'
#    os.system('punlearn grppha')
#    os.system('grppha infile="%s" outfile="%s" chatter=0 comm="group min 30 & chkey BACKFILE %s & chkey RESPFILE %s & chkey ANCRFILE %s & #exit"' % (specout,grpout,bgspecout,rmfout,arfout))

#     # Update spec header
    # os.system('punlearn dmhedit')
    # os.system("""dmhedit %s filelist=none operation=add key=ANCRFILE value="'%s'" datatype=string""" % (specout,arfout))
    # os.system('punlearn dmhedit')
    # os.system("""dmhedit %s filelist=none operation=add key=RESPFILE value="'%s'" datatype=string""" % (specout,rmfout))
    # os.system('punlearn dmhedit')
    # os.system("""dmhedit %s filelist=none operation=add key=BACKFILE value="'%s'" datatype=string""" % (specout,bgspecout))

#     # Remove files?
# #    for i in xrange(len(spectra)):
# #        os.remove(spectra[i])
# #        os.remove(bgspectra[i])
# #        os.remove(arffiles[i])
# #        os.remove(rmffiles[i])
        
    os.system('rm *.weight')
    os.system('rm *_tdet.fits')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage %s path_to_obsids" % sys.argv[0])
        sys.exit(1)

    # Run in regions directory, supply path from there to obsids
    path = str(sys.argv[1])
    print(path)
    
    # Define function that separates integer from region*.reg
    # split = lambda x: int( x.split('region')[1].split('.')[0] )
    #split = lambda x: int( x.split('xaf_')[1].split('.')[0] ) #Extracting Spectra for Maps
    
    split = lambda x: int( x.split('region')[1].split('.')[0] ) #Extracting Spectra for Profiles
    #   ^ correct one
    # split = lambda x: int( x.split('cavity')[1].split('.')[0] ) #Extracting Spectra for Profiles
    # split = lambda x: int( x.split('offjet2_')[1].split('.')[0] ) #Extracting Spectra for Profiles relative to jet direction

    # Get list of regions
    regions = sorted( glob.glob('region*.reg') , key=split ) #Extracting Spectra for Profiles
    print(regions)
    #  ^ correct one
    
    # regions = sorted( glob.glob('cavity*.reg') , key=split ) #Extracting Spectra for Profiles
    # regions = sorted( glob.glob('offjet2_*.reg') , key=split ) #Extracting Spectra for Profiles relative to jet direction
   # regions = glob.glob('center*.reg')
    
    # Filter regions in case spectra extraction did not finish
    # regions = filter(lambda x: split(x) >= 0, regions) 
    #  ^ correct one

    # regions=['cavity.reg']

    # obsids = ['904', '15173', '15174', '16263', '16264'] # Abell 85

    # obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795

    #obsids = ['891', '4977','6101']  # Abell 2029
    
    #obsids = ['504', '505', '4954','4955','5310','16223','16224','16534','16607','16608','16609','16610'] #Centaurus 
    
    obsids = ['16142','16143','16464','16626','16627','16633','16634','16635','16645','3200'] #Ophichius 
    
    # obsids = ['3231'] #Abell 2319 '15187', 

    #obsids = ['502','503','1513'] #Abell 426

    #obsids = ['4197','10468','10470','10471','10822','10918','10922','16275'] #MS0735
    
    #obsids = ['4203']  #Abell 3571

    # obsids= ['495', '496', '6880', '6881', '7370'] # Abell 1835

    # obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix

    # obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664

    # obsids = ['922', '6934', '7329', '19596', '19597', '19598', '20626', '20627', '20628', '20629', '20805', '20806', '20811', '20817'] # Abell 2597

   # obsids = ['5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052

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

    # obsids = ['3195', '7706', '12903']  # Zw 2701
    
    #obsids = ['10743','577'] #A754
    
    obsids = ['6225','6226','6228','6229','6250','6252'] #CygnusA '5830','5831',
    

    for reg in regions:

    # List of observations: 
    # Extract spectra from front and back-illuminated chips separately!
    # Only use summed spectra when confident that the ARFs are quite similar!
        
        # onchip = [0,0,0,0,0] # Abell 85
        #onchip = [7,3]  # A2029
        onchip = [1,1,1,1,1,3]  # A2029
        #onchip = [7,7,7,7,7,7,7,7,7,7,7,7]  # Centaurus
        # onchip = [3,2] #A2319
        # onchip = [2]
        #onchip = [3,7,7] #A426
        #onchip = [7] #A3571
        # onchip = [7,3,3,3,3,3,3,3] # MS0735
        # onchip = [7,7,3,3,3]  # A1835
        # onchip = [3,3,3,3,3,3,3,3,3,3,3,3]  # phoenix
        # onchip = [7,7,7,7,7,7] # Abell 1664
        # onchip = [7,7,7,7,7,7,7,7,7,7,7,7,7,7] # Abell 2597
        #onchip = [7,7,7,7,7,7,7,7,7,7] # A2052
        # onchip = [7,7,3,3,7] # PKS0745
        # onchip = [7,3,3,3,3,3,3,3,3] # MS0735
        # onchip = [7,7,7,3,3,3,3] # MACS1347
        # onchip = [7,7,7,7,7,7,3,3,1,7,0,3,3,1,3,7,5,3,3,7,7,7,7,3,3,3,3,3,3,2,2,0,0,1,1,7,7,3,3,3,0,1,2,7,7,3,3,3,0,3] # Abell 1795
        # onchip = [7,7] # Hydra-A
        # onchip = [3,3,3,3,3] # RXCJ1504
        # onchip = [3,3,3] # Abell 133
        # onchip = [7,3,3,3] # IC1262
        # onchip = [7,7] # Abell 262
        # onchip = [7,7] # Abell 2626
        # onchip = [7,7,7,7,7,7,7] # NGC 5044
        # onchip = [3,3,3] # Zw 7160

        testfile = reg[:-4] + '_sumc0_grp30.pi'

        if os.path.isfile(testfile):
            continue
        else:
            # print(obs, reg)
            generate_spectra(path,obsids,onchip,reg)
