#!/usr/bin/env python

import os
import sys
import numpy
from astropy.io import fits
import glob

# Take a blank sky background file + add a time column
# Then extract factor x evt2 exptime from this

def trimbackground(bgevt2,obsevt2,factor):

    # New background filename
    bgevt2new = bgevt2[:-5] + '_wtime.fits'
    bgevt2trim = bgevt2[:-5] + '_obsexpx' + str(factor) + '.fits'

    # Get obs exposure time
    obshdulist = fits.open(obsevt2)
    sechdr = obshdulist[1].header
    obsexptime = sechdr['EXPOSURE']
    obshdulist.close()

    print("Observation exposure: %f s" % obsexptime)

    # Read in background events file
    bghdulist = fits.open(bgevt2)
    bgsechdr = bghdulist[1].header
    bgexptime = bgsechdr['EXPOSURE']

    print("Background exposure: %f s" % bgexptime)

    bgtbdata = bghdulist[1].data
    bghdulist.close()
    no_of_bgevts = len(bgtbdata)

    print("Number of background events: %d" % no_of_bgevts)

    bgtimes = []

    # Generate random times
    for i in range(no_of_bgevts):
        t = numpy.random.uniform(0.,bgexptime)
        bgtimes.append(t)

    bgtimes = numpy.array(bgtimes)
    print(bgtimes)

    print("Generated %d random times" % len(bgtimes))

    # Add these times as an extra column
    coltime = fits.Column(name='time', format='D', unit='s', array=bgtimes)
    cols = fits.ColDefs([coltime])
    newtbdata = fits.BinTableHDU.from_columns(cols)
    newtbdata.writeto('temp.fits')

    os.system('cp %s %s' % (bgevt2,bgevt2new))
    os.system('punlearn faddcol')
    os.system('faddcol %s temp.fits time' % (bgevt2new))
    os.remove('temp.fits')

    # Sort columns on time
    print("Sorting event file on time column ...")
    os.system('punlearn fsort')
    os.system('fsort %s[1] time method="heap"' % (bgevt2new))

    # Trim down exposure time of background obs to 10 x obs.
    timelimit = factor*obsexptime
    os.system('punlearn dmcopy')
    os.system('dmcopy "%s[time=0:%f]" %s' % (bgevt2new,timelimit,bgevt2trim))
    os.system('punlearn fparkey')
    os.system('fparkey %f "%s[1]" EXPOSURE' % (timelimit, bgevt2trim))

    # Remove time column from final background file
    os.system('punlearn fdelcol')
    os.system('fdelcol %s+1 time N Y' % (bgevt2trim))

    os.remove(bgevt2new)

    return bgevt2trim

if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s factor bgevt2names" %(sys.argv[0]))
        sys.exit(1)

    factor = int(sys.argv[1])
    bgevt2files = sys.argv[2:]

    bgtrimnames = []

    for bgevt2 in bgevt2files:

        # Find observation of relevant chip
        obsevt2 = 'evt2_c' + str(bgevt2[8]) + '.fits'

        # Generate trimmed background file
        bgevt2trimname = trimbackground(bgevt2,obsevt2,factor)
        bgtrimnames.append(bgevt2trimname)

    # Merge these separate events files
    bgtrimnames = numpy.array(bgtrimnames)
    bgnamestring = ','.join(str(name) for name in bgtrimnames)
    os.system('punlearn dmmerge')
    os.system('dmmerge "%s" bgevt2_sum_obsexpx%s.fits' % (bgnamestring,str(factor)))

    # Set exposure time in header
    evt2name = glob.glob('acis*_evt2.fits')[0]
    hdulist = fits.open(evt2name)
    prihdr = hdulist[1].header
    obsexptime = prihdr['EXPOSURE']
    hdulist.close()

    bgobsexptime = factor*obsexptime

    os.system('punlearn dmhedit')
    os.system('dmhedit bgevt2_sum_obsexpx%s.fits filelist=none operation=add key=EXPOSURE value=%f datatype=indef' % (str(factor),bgobsexptime))

    # Zip up big bg events files
    for name in bgtrimnames:
        os.system('gzip %s' % name)

