#!/usr/bin/env python


from astropy.io import fits
import sys
from ciao_contrib.runtool import *

num_files = int(sys.argv[1])
path = sys.argv[2]

for i in range(num_files):
    specfile = path+'region%s_sum_spec.pi'%i
    arf = 'region%s_sum.arf'%i
    rmf = 'region%s_sum.rmf'%i
    bckfile = 'region%s_sum_bgspec.pi'%i

    dmhedit(infile=specfile, filelist='none',
        operation='add', key='RESPFILE', value=rmf)
    dmhedit(infile=specfile, filelist='none',
        operation='add', key='ANCRFILE', value=arf)
    dmhedit(infile=specfile, filelist='none',
        operation='add', key='BACKFILE', value=bckfile)


