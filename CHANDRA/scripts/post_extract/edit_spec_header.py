#!/usr/bin/env python

import os
import glob
import argparse
# from ciao_contrib.runtool import *


def edit_header(reg, obs):
    params={'spec': reg[:-4]+'_'+obs+'_spec.pi',
            'bgspec': reg[:-4]+'_'+obs+'_bgspec.pi',
            'rmf': reg[:-4]+'_'+obs+'.rmf',
            'arf': reg[:-4]+'_'+obs+'.arf'}

    print(params['spec'])
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


def group_spectra(reg, obs, counts):
    params={'spec': reg[:-4]+'_'+obs+'_spec.pi',
            'bgspec': reg[:-4]+'_'+obs+'_bgspec.pi',
            'rmf': reg[:-4]+'_'+obs+'.rmf',
            'arf': reg[:-4]+'_'+obs+'.arf'}

    grpout = '%s_%s_grp%s.pi' % (reg[:-4], obs, str(counts))
    os.system('punlearn grppha')
    os.system('grppha infile="%s" outfile="%s" chatter=0 comm="group min %s & chkey BACKFILE %s & chkey RESPFILE %s & chkey ANCRFILE %s & exit"' % (params['spec'],grpout,counts,params['bgspec'],params['rmf'],params['arf']))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('edithead', type=str,
                    help='Add BACKFILE, RESPFILE, ANCRFILE keywords and their values to *_spec.pi files (y/n)')
    parser.add_argument('grpspec', type=str, help='Group the unbinned spectra (y/n)')
    parser.add_argument('counts', type=int, help='number of counts per bin')
    args = parser.parse_args()


    # obsids = ['922', '6934', '7329', '19596', '19597', '19598', '20626', '20627', '20628', '20629', '20805', '20806', '20811', '20817'] # Abell 2597
    # obsids = ['493', '494', '3666', '5286', '5287', '5288', '5289', '5290', '6159', '6160', '6161', '6162', '6163', '10898', '10899', '10900', '10901', '12026', '12027', '12028', '12029', '13106', '13107', '13108', '13109', '13110', '13111', '13112', '13113', '13412', '13413', '13414', '13415', '13416', '13417', '14268', '14269', '14270', '14271', '14272', '14273', '14274', '14275', '15485', '15486', '15487', '15488', '15489', '15490', '17228'] # Abell 1795
    obsids = ['13401', '16135', '16545', '19581', '19582', '19583',
              '20630', '20631', '20634', '20635', '20636', '20797']  # Phoenix

    split = lambda x: int( x.split('region')[1].split('.')[0] ) #Extracting Spectra for Profiles
    # Get list of regions
    regions = sorted( glob.glob('region*.reg') , key=split ) #Extracting Spectra for Profiles

    for reg in regions:
        for obs in obsids:
            if args.edithead == 'y':
                edit_header(reg, obs)
            if args.grpspec == 'y':
                if args.counts:
                    group_spectra(reg, obs, args.counts)
                else:
                    sys.stderr.write("Please enter counts per bin after grpspec parameter")
                    sys.exit(1)
