#!/usr/bin/env python

import glob

# Create region_list.txt for contour binning

#regions = glob.glob('xaf_*.reg')
regions = glob.glob('region*.reg')
#regions = glob.glob('XRISM_region1.reg')

fout = open('region_list.txt','a')
#fout = open('XRISMregion1_list.txt','a')

for i in range(len(regions)):
#    reg = 'xaf_' + str(i) + '.reg'

    #reg = 'XRISM_region'+ '.reg'
    reg = 'region' + str(i) + '.reg'
#    spec = reg[:-4] + '_sumc3_spec.pi'
    spec = reg[:-4] + '_sum_grp100.pi'
    #spec = reg[:-4] + '_grp30.pi'
    print('%s %s' % (reg[:-4],spec), file=fout)

fout.close()
