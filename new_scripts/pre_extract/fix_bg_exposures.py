#!/usr/bin/env python3


# fix the exposure times of a background events file so that the
# count rate in the 9.5-12 keV band is the same as a foreground events
# file

from astropy.io import fits
#import numarray as N
import os
import sys

if len(sys.argv) != 4:
    sys.stderr.write("Usage %s infile_evt2.fits backfile_evt2.fits ccd_id" % sys.argv[0])
    sys.exit(1)

inevt2 = sys.argv[1]
bgevt2 = sys.argv[2]
#chip = sys.argv[3].lower()
ccd = sys.argv[3]

#if chip not in ('i', 's'):
#    sys.stderr.write("Chip must be I or S")
#    sys.exit(1)
print("ccd: %s" %ccd)

def getRate(filename):
    '''Get the high energy count rate.'''

    # get number of good events

#    if chip == 'i':
#        ccd = '0:3'
#    else:
#        ccd = '7'
    
    cmd = 'dmstat "%s[ccd_id=%s][energy=9500:12000][cols pi]"' % (filename, ccd)
    good = None
    for l in os.popen(cmd, 'r'):
        p = l.split()
        if p[0] == 'good:':
            good = int(p[1])
            print('good:%s' %good)
            break

    assert good != None

    cmd = 'dmkeypar "%s" EXPOSURE echo+' % filename
    exposure = float( os.popen(cmd, 'r').read() )

    return good/exposure

fgrate = getRate(inevt2)
bgrate = getRate(bgevt2)


ratio = fgrate/bgrate
print("Old ratio:", ratio)


bgevt = fits.open(bgevt2, 'update')
phead = bgevt['EVENTS'].header
phead['TSTOP'] = (phead['TSTOP'] - phead['TSTART']) / ratio + phead['TSTART']
ehead = bgevt['EVENTS'].header
ehead['EXPOSURE'] /= ratio
if 'LIVETIME' in ehead:
    ehead['LIVETIME'] /= ratio
if 'ONTIME' in ehead:
    ehead['ONTIME'] /= ratio
ehead['TSTOP'] = (ehead['TSTOP'] - ehead['TSTART']) / ratio + ehead['TSTART']

ehead.add_history('Exposure time decreased by %f to match 9.5-12 keV rate' % ratio)
ehead.add_history('Done by fix_bg_exposures.py')

bgevt.close()

fgrate = getRate(inevt2)
bgrate = getRate(bgevt2)
ratio = fgrate/bgrate
print("New ratio:", ratio)