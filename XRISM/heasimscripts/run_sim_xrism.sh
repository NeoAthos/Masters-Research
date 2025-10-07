#! bin/sh

# This script is configured to execute a point source power law simulation, as observed
# with ASTRO-H instrument SXI.  Edit parameters to change.

# if there's no output directory, then make it.
if [ ! -d output ]; then
    mkdir output
fi

mission="xrism"                                           # mission
instrume="sxs"                                            # instrume
cal_dir="$HEASIM_SUPPORT/$mission/resolve"                                               # master calibration data directory
resp_dir="$HEASIM_SUPPORT/$mission/resolve/response"    # response directory
psf_dir="$cal_dir/psf"          # psf directory
vig_dir="$cal_dir/vignette"     # vignette directory
back_dir=$HEASIM_SUPPORT/$mission/resolve/background  # background directory
source_dir=$HEASIM_SUPPORT/testdata/source_data                          # directory containing source files

arf="$resp_dir/resolve_bet_spec_noGV_20190611.arf"
rmf="$resp_dir/resolve_h5ev_2019a.rmf"
outfile=output/astroH_sxi_plaw.fits                            


############# ASSIGNMENT BLOCK ##############

mission="hitomi"
instrume=$instrume
filter=none
instmode=none
rapoint=150.00
decpoint=50.00
roll=0.00
exposure=10000.
flagsubex=no
#subexposure=1000.
insrcdeffile=$source_dir/plaw_test.txt
outfile=$outfile
psffile=$psf_dir/sxs_psfimage_20140618.fits
vigfile=$vig_dir/SXT_VIG_140618.txt
rmffile=$rmf
arffile=$arf
arfrmftol=1.0e0
intbackfile=$back_dir/resolve_h5ev_2019a_rslnxb.pha
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
opt=""
#opt="gdb --args"
#opt="valgrind -v --leak-check=full --show-reachable=yes"

punlearn heasim
$opt heasim \
    mission=$mission \
    instrume=$instrume \
    filter=$filter \
    instmode=$instmode \
    rapoint=$rapoint \
    decpoint=$decpoint \
    roll=$roll \
    exposure=$exposure \
    flagsubex=$flagsubex \
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
    mdbfile=$mdbfile \
    seed=$seed






