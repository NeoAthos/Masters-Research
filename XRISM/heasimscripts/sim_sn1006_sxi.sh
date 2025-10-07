#! /bin/sh

# if there's no output directory, then make it.
if [ ! -d output ]; then
    mkdir output
fi

mission="astro-h"                          # mission
instrume="sxi"                             # instrument
cal_dir="sxi"                              # master calibration data directory
resp_dir=$HEASIM_SUPPORT/$mission/$cal_dir/response    # response directory
psf_dir=$HEASIM_SUPPORT/$mission/$cal_dir/psf          # psf directory
vig_dir=$HEASIM_SUPPORT/$mission/$cal_dir/vignette     # vignette directory
back_dir=$HEASIM_SUPPORT/$mission/$cal_dir/background  # background directory
#source_dir=$HEASIM_SUPPORT/testdata/source_data       # directory containing source files

arf=$resp_dir/sxt-i_140505_ts02um_int01.8r_intall.arf
rmf=$resp_dir/ah_sxi_20120702.rmf
psf=$psf_dir/sxt-i_EEF_4p5keV_140617_type1.fits
vig=$vig_dir/SXT_VIG_140618_type1.fits
back=$back_dir/ah_sxi_pch_nxb_full_20110530.pi

infile=sim_sn1006_sxi.txt
outfile=output/astroH_sxi_sn1006_test1.fits                            


############# ASSIGNMENT BLOCK ##############

mission=$mission
instrume=$instrume
filter=none
instmode=none
rapoint=225.8
decpoint=-41.98
roll=0.00
flagsubex=yes
exposure=100000. 
subexposure=1.0e9
insrcdeffile=$infile
outfile=$outfile
psffile=$psf
vigfile=$vig
rmffile=$rmf
arffile=$arf
arfrmftol=1.0e0
intbackfile=$back
psbackfile=none
difbackfile=none
pszbackfile=none
dtpileup=0.0
getinfile=no
debug=no
clobber=yes
mode=ql
mdbfile=$LHEA_DATA/heasim.mdb
seed=1234567890    # if == 0, ignore and seed using system time


######### EXECUTION BLOCK ###################

punlearn heasim
heasim \
    mission=$mission \
    instrume=$instrume \
    filter=$filter \
    instmode=$instmode \
    rapoint=$rapoint \
    decpoint=$decpoint \
    roll=$roll \
    exposure=$exposure \
    flagsubex=$flagsubex \
    subexposure=$subexposure \
    insrcdeffile=$insrcdeffile \
    outfile=$outfile \
    psffile=$psffile \
    vigfile=$vigfile \
    rmffile=$rmffile \
    arffile=$arffile \
    arfrmftol=$arfrmftol \
    intbackfile=$intbackfile \
    psbackfile=$psbackfile \
    difbackfile=$difbackfile \
    pszbackfile=$pszbackfile \
    dtpileup=$dtpileup \
    getinfile=$getinfile \
    debug=$debug \
    clobber=$clobber \
    mode=$mode \
    mdbfile=$mdbfile
