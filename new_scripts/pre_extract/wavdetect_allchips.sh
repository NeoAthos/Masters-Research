#!/usr/bin/env bash

punlearn mkpsfmap
evt2name=$(ls *_reproj_evt2.fits)
summedimage=$(ls evt2_summed_*_*.fits)
if [ -e psfmap.fits ]; then
    echo 'psfmap already exists, skipping this step'
else
    echo 'making psfmap'
    mkpsfmap ${evt2name} psfmap.fits 2.3 ecf=0.9 units=physical clobber=yes
fi

psfmap=$(ls psfmap.fits)

# Workaround for clusters where wavdetect doesn't work properly unless the image is binned

if [ -e crop.reg ]; then
    dmcopy "${summedimage}[sky=region(crop.reg)]" evt_temp.fits
    dmcopy "${psfmap}[sky=region(crop.reg)]" psf_temp.fits
    summedimage=$(ls evt_temp.fits)
    psfmap=$(ls psf_temp.fits)

fi

echo 'running wavdetect'

punlearn wavdetect
pset wavdetect infile=${summedimage}
pset wavdetect outfile=wav_out.fits
pset wavdetect scellfile=wav_scell.fits
pset wavdetect imagefile=wav_image.fits
pset wavdetect defnbkgfile=wav_defnbkg.fits
pset wavdetect regfile=allsources.reg
pset wavdetect psffile=${psfmap}
pset wavdetect sigthresh= 1e-10
pset wavdetect bkgsigthresh=0.001
pset wavdetect psffile=''
pset wavdetect ellsigma=5
pset wavdetect scales="2 4"
pset wavdetect clobber=yes
wavdetect

#rm *_temp.fits
