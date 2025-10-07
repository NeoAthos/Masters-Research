#! bin/sh

# if there's no output directory, then make it.
if [ ! -d output ]; then
    mkdir output
fi

mission="astro-h"                                      # mission
instrume="sxs"                                         # instrument
cal_dir="sxs"                                          # master calibration data directory
resp_dir=$HEASIM_SUPPORT/$mission/$cal_dir/response    # response directory
psf_dir=$HEASIM_SUPPORT/$mission/$cal_dir/psf          # psf directory
vig_dir=$HEASIM_SUPPORT/$mission/$cal_dir/vignette     # vignette directory
#source_dir=$HEASIM_SUPPORT/testdata/source_data       # directory containing source files
back_dir=$HEASIM_SUPPORT/$mission/$cal_dir/background  # int-bkg directory

arf=$resp_dir/sxt-s_140505_ts02um_intall_140618psf.arf
rmf=$resp_dir/ah_sxs_10ev_20150121.rmf
back=$back_dir/sxs_nxb_7ev_20110211_1Gs.pha
vignette=$vig_dir/SXT_VIG_140618.txt 
psf=$psf_dir/eef_from_sxs_psfimage_20140618.fits

outfile=output/astroH_plaw_burst_sxs.fits

############# ASSIGNMENT BLOCK ##############

mission=$mission
instrume=$instrume
rapoint=151.8606
decpoint=16.1085
roll=0.00
exposure=1000.
flagsubex=no
subexposure=1000.
insrcdeffile=plaw_burst.txt 
outfile=$outfile
psffile=$psf
vigfile=none
rmffile=$rmf
arffile=$arf
intbackfile=none
mdbfile=$LHEA_DATA/heasim.mdb

######### EXECUTION BLOCK ###################

punlearn heasim
heasim \
    mission=$mission \
    instrume=$instrume \
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
    intbackfile=$intbackfile \
    mdbfile=$mdbfile 

instrume="sxi"                                            # instrument
cal_dir="sxi"                                             # master calibration data directory
resp_dir=$HEASIM_SUPPORT/$mission/$cal_dir/response       # response directory
psf_dir=$HEASIM_SUPPORT/$mission/$cal_dir/psf             # psf directory
vig_dir=$HEASIM_SUPPORT/$mission/$cal_dir/vignette        # vignette directory
#source_dir=$HEASIM_SUPPORT/testdata/source_data                             # directory containing source files
back_dir=$HEASIM_SUPPORT/$mission/$cal_dir/background     # int-bkg directory

arf=$resp_dir/sxt-i_140505_ts02um_int01.8r_intall.arf
rmf=$resp_dir/ah_sxi_20120702.rmf
back=$back_dir/ah_sxi_pch_nxb_full_20110530.pi
vignette=$vig_dir/SXT_VIG_140618.txt 
psf=$psf_dir/sxt-i_EEF_4p5keV_140617.txt

outfile=output/astroH_plaw_burst_sxi.fits

############# ASSIGNMENT BLOCK ##############

mission=$mission
instrume=$instrume
rapoint=151.8606
decpoint=16.1085
roll=0.00
exposure=1000.
flagsubex=no
subexposure=1000.
insrcdeffile=plaw_burst.txt 
outfile=$outfile
psffile=$psf
vigfile=none
rmffile=$rmf
arffile=$arf
intbackfile=none
mdbfile=$LHEA_DATA/heasim.mdb

######### EXECUTION BLOCK ###################

heasim \
    mission=$mission \
    instrume=$instrume \
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
    intbackfile=$intbackfile \
    mdbfile=$mdbfile 

instrume="hxi1"                                           # instrument
cal_dir="hxi"                                             # master calibration data directory
resp_dir=$HEASIM_SUPPORT/$mission/$cal_dir/response       # response directory
psf_dir=$HEASIM_SUPPORT/$mission/$cal_dir/psf             # psf directory
vig_dir=$HEASIM_SUPPORT/$mission/$cal_dir/vignette        # vignette directory
back_dir=$HEASIM_SUPPORT/$mission/$cal_dir/background     # int-bkg directory

arf=$resp_dir/ah_hxt_pnt_r4intall_20150724.arf
rmf=$resp_dir/ah_hxi_response_20150729.rmf
back=$back_dir/ah_hxi_nxb_r4intall_20150727.pha
psf=$psf_dir/AstroH_HXI_EEF_090217.txt
vignette=$vig_dir/HXT_VIG_hm110105v2.txt

outfile=output/astroH_plaw_burst_hxi1.fits

############# ASSIGNMENT BLOCK ##############

mission=$mission
instrume=$instrume
rapoint=151.8606
decpoint=16.1085
roll=0.00
exposure=1000.
flagsubex=no
subexposure=1000.
insrcdeffile=plaw_burst.txt 
outfile=$outfile
psffile=$psf
vigfile=none
rmffile=$rmf
arffile=$arf
intbackfile=none
mdbfile=$LHEA_DATA/heasim.mdb

######### EXECUTION BLOCK ###################

heasim \
    mission=$mission \
    instrume=$instrume \
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
    intbackfile=$intbackfile \
    mdbfile=$mdbfile 
