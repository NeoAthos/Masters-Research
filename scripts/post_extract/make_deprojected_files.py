#!/usr/bin/env python

from deproject_spectra import *
from subprocess import check_output
from ciao_contrib.runtool import dmkeypar
import os

# obsids = ['904', '15173', '15174', '16263', '16264'] # Abell 85
# obsids = ['891', '4977', '6101'] # Abell 2029
# obsids = ['495', '496', '6880', '6881', '7370'] # Abell 1835
# obsids = ['13401', '16135', '16545', '19581', '19582', '19583', '20630', '20631', '20634', '20635', '20636', '20797'] # Phoenix
# obsids = ['1648', '7901', '17172', '17173', '17557', '17568'] # Abell 1664
# obsids = ['19596', '19598', '20627', '20629', '20806', '20817', '7329', '19597', '20626', '20628', '20805', '20811', '6934', '922'] # Abell 2597
# obsids = ['5807', '10477', '10478', '10479', '10480', '10879', '10914', '10915', '10916', '10917'] # Abell 2052
# obsids = ['508', '2427', '6103', '7694', '12881'] # PKS0745
# obsids = ['506', '507', '2222', '3592', '13516', '13999', '14407'] # MACSJ1347-11
# obsids = ['4197', '10468', '10469', '10470', '10471',
#           '10822', '10918', '10922', '16275']  # MS0735+7421
# obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795
# obsids = ['4969', '4970'] # Hydra-A
# obsids = ['4935', '5793', '17197', '17669', '17670'] # RXCJ1504
# obsids = ['2203', '9897', '13518'] # Abell 133
# obsids = ['2018', '6949', '7321', '7322'] # IC1262
obsids = ['2215', '7921'] # Abell 262
# obsids = ['3192', '16136'] # Abell 2626
# obsids = ['798', '9399', '17195', '17196', '17653', '17654', '17666'] # NGC 5044
# obsids = ['543', '4192', '7709'] # Zw 7160
# obsids = ['1668', '11758']  # AS1101
# obsids = ['909', '1651', '9371']  # ZwCl 3146
# obsids = ['497', '498', '10748', '10803', '10804', '10805']  # Abell 2199
# obsids = ['1657', '4195']  # MACS1423+24
# obsids = ['3195', '7706', '12903']  # Zw 2701
# obsids = ['8266']  # RXCJ1539

regionlist = open('region_list.txt', 'r').readlines()

for i in obsids:
    prefix = 'region'
    suffix = "_"+i+"_spec.pi"
    minspec = 0
    numspecs = len(regionlist)
    minradius = 3.
    outprefix = 'region'
    outsuffix = "_"+i+"_deproj.pi"

    spectra = readSpectra(prefix, suffix, minspec, numspecs, minradius)
    doDeprojection(spectra, 6000, minspec, outprefix, outsuffix)
    print("Adding header keywords for background, rmf and arf files")

    for j in range(len(regionlist)):
        name = prefix+str(j)+'_'+i
        specout = name+"_deproj.pi"
        bgspecout = '%s_bgspec.pi' % name
        rmfout = '%s.rmf' % name
        arfout = '%s.arf' % name
        rootspec = prefix+str(j)+suffix
        backscal = dmkeypar(rootspec, keyword='BACKSCAL', echo=True)
        exposure = dmkeypar(rootspec, keyword='EXPOSURE', echo=True)
        corrscal = dmkeypar(rootspec, keyword='CORRSCAL', echo=True)
        areascal = dmkeypar(rootspec, keyword='AREASCAL', echo=True)
        print("exposure:", exposure)
        # Update spec header
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=ANCRFILE value="'%s'" datatype=string""" % (specout,arfout))
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=RESPFILE value="'%s'" datatype=string""" % (specout,rmfout))
        os.system('punlearn dmhedit')
        os.system("""dmhedit %s filelist=none operation=add key=BACKFILE value="'%s'" datatype=string""" % (specout,bgspecout))
        os.system('punlearn dmhedit')
        os.system("dmhedit %s filelist=none operation=add key=BACKSCAL value=%s datatype=float" % (specout, float(backscal)))
        os.system('punlearn dmhedit')
        os.system("dmhedit %s filelist=none operation=add key=AREASCAL value=%s datatype=float" % (specout, float(areascal)))
        os.system('punlearn dmhedit')
        os.system("dmhedit %s filelist=none operation=add key=CORRSCAL value=%s datatype=float" % (specout, float(corrscal)))
        os.system('punlearn dmhedit')
        os.system("dmhedit %s filelist=none operation=add key=EXPOSURE value=%s datatype=float" % (specout, float(exposure)))


with open("region_list_deproj.txt", 'w') as deproj_list:
    for line in regionlist:
        if 'grp100' in line:
            deproj_list.write(line.replace("grp100", 'deproj'))
        elif 'grp30' in line:
            deproj_list.write(line.replace("grp30", 'deproj'))
        elif 'grp10' in line:
            deproj_list.write(line.replace("grp10", 'deproj'))
