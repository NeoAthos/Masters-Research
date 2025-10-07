#!/bin/bash

# This script is configured to simulate a cluster of galaxies
# as a beta-model surface brightness profile with a temperature gradient,
# as observed with ASTRO-H instrument SXI.

#root_name="cluster_beta_tempgradient_sxi"
root_name="cluster_beta_tempgradient_sxi"

# if there's no output directory, then make it.
if [ ! -d output ]; then
    mkdir output
fi

mission="astro-h"                            # mission
instrume="sxi"                               # instrument
cal_dir="$HEASIM_SUPPORT/$mission/$instrume" # calibration directory
resp_dir="$cal_dir/response"                 # response directory
psffile="$cal_dir/psf/sxt-i_EEF_4p5keV_140617_type1.fits" # psf file
vigfile="$cal_dir/vignette/SXT_VIG_140618_type1.fits"     # vignetting file

if [ $instrume = "sxi" ] ; then
     rmf=$resp_dir/ah_sxi_20120702.rmf
     arf=$resp_dir/sxt-i_140505_ts02um_int01.8r_intall.arf
elif [ $instrume = "sxs" ] ; then
     rmf=$resp_dir/ah_sxs_7ev_20130806.rmf
     arf=$resp_dir/sxt-s_140505_ts02um_intallpxl.arf
fi

ra=207.215
dec=26.588
sourcefile="${root_name}.dat"
outfile="output/${root_name}.fits"
logfile="output/${root_name}.log"

punlearn heasim
pset heasim mission=$mission
pset heasim instrume=$instrume
pset heasim filter=none
pset heasim instmode=none
pset heasim rapoint=$ra
pset heasim decpoint=$dec
pset heasim roll=0.00
pset heasim exposure=100000.
pset heasim flagsubex=no
pset heasim subexposure=100000.
pset heasim insrcdeffile=$sourcefile
pset heasim outfile=$outfile
pset heasim psffile=$psffile
pset heasim vigfile=$vigfile
pset heasim rmffile=$rmf
pset heasim arffile=$arf
pset heasim arfrmftol=1.0e0
pset heasim intbackfile=none
pset heasim psbackfile=none
pset heasim difbackfile=none
pset heasim pszbackfile=none
pset heasim dtpileup=0.
pset heasim getinfile=no
pset heasim debug=no
pset heasim clobber=yes
pset heasim seed=1234567890
pset heasim mdbfile=$LHEA_DATA/heasim.mdb

echo "Parameters for heasim:" | tee $logfile
plist heasim 2>&1 | tee -a $logfile
heasim mode=hl 2>&1 | tee -a $logfile
