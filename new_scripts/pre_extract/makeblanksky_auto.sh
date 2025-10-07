#!/usr/bin/env bash
##############################################################################
# Version 1.0: 
#
##############################################################################

set -x

echo -n "First run copy_files_chandra and process_chandra with CTI correction"
evt2name=$(ls acis*_evt2.fits)

ccd_id=$1

punlearn dmcopy
dmcopy "${evt2name}[ccd_id=${ccd_id}]" evt2_c${ccd_id}.fits

# Find relevant background file => remove block indicator
bkgrnd_file_mod=$(acis_bkgrnd_lookup evt2_c${ccd_id}.fits)
bkgrnd_file=$(echo $bkgrnd_file_mod |cut -d'[' -f1)
cp ${bkgrnd_file} ./bgevt2_c${ccd_id}.fits


datamode=$(dmkeypar evt2_c${ccd_id}.fits DATAMODE echo+)

# Apply VFAINT filtering!
if [[ $datamode = VFAINT ]] ; then
    punlearn fcopy
    fcopy bgevt2_c${ccd_id}.fits"[events][status==bxxxxxxxx0xxxxxxxxxxxxxxxxxxxxxxx]" bgevt2_c${ccd_id}_filt.fits
else
    cp bgevt2_c${ccd_id}.fits bgevt2_c${ccd_id}_filt.fits
fi

# Process background file in identical way
dmkeypar evt2_c${ccd_id}.fits GAINFILE echo+
dmkeypar bgevt2_c${ccd_id}.fits GAINFILE echo+

#gfile=$(dmkeypar evt2_c${ccd_id}.fits GAINFILE echo+)

#punlearn acis_process_events
#acis_process_events infile=bgevt2_c${ccd_id}_filt.fits outfile=bgevt2_c${ccd_id}_newgainfilt.fits acaofffile=NONE stop="none" doevtgrade=no apply_cti=yes apply_tgain=no calculate_pi=yes pix_adj=NONE check_vf_pha=yes gainfile=$CALDB/data/chandra/acis/det_gain/${gfile} eventdef="{s:ccd_id,s:node_id,i:expno,s:chip,s:tdet,f:det,f:sky,s:phas,l:pha,l:pha_ro,f:energy,l:pi,s:fltgrade,s:grade,x:status}"
cp bgevt2_c${ccd_id}_filt.fits bgevt2_c${ccd_id}_newgainfilt.fits

dmkeypar evt2_c${ccd_id}.fits GAINFILE echo+
dmkeypar bgevt2_c${ccd_id}_newgainfilt.fits GAINFILE echo+

# Add the PNT header keywords
punlearn dmmakepar
dmmakepar evt2_c${ccd_id}.fits event_header.par

grep _pnt event_header.par > event_pnt.par
cat event_pnt.par
chmod +w bgevt2_c${ccd_id}_newgainfilt.fits
punlearn dmreadpar
dmreadpar event_pnt.par "bgevt2_c${ccd_id}_newgainfilt.fits[events]" clobber+

rm -f event_pnt.par
rm -r event_header.par

# Reproject the background

#aspect_file="@"`ls acisf*asol1.lis`
aspect_file='/home/muzili/Documents/2020_Spring/summary/A2029/04977/primary/pcadf189953929N005_asol1.fits'

punlearn reproject_events
reproject_events infile=bgevt2_c${ccd_id}_newgainfilt.fits outfile=bgevt2_c${ccd_id}_reproj.fits aspect=${aspect_file} match=evt2_c${ccd_id}.fits random=0
 
# Normalize background
# Check there are no sources
punlearn dmcopy
dmcopy "${evt2name}[energy=9500:12000,ccd_id=${ccd_id}]" highE.fits

# Temporary work around
punlearn dmcopy
dmcopy "highE.fits[sky=region(chips.reg[ccd_id=${ccd_id}])]" tempfile.fits

punlearn wavdetect
wavdetect infile=tempfile.fits outfile=evt2_highEsources_out_c${ccd_id}.fits scellfile=evt2_highEsources_scell_c${ccd_id}.fits imagefile=evt2_highEsources_image_c${ccd_id}.fits defnbkgfile=evt2_highEsources_defnbkg_c${ccd_id}.fits regfile=sources_highE_c${ccd_id}.reg psffile="" scales="2.0 4.0" ellsigma=5 clobber=yes

rm -f tempfile.fits

echo -n "Create sources_highE.reg"
# emacs sources_highE_c${ccd_id}.reg
ds9 highE.fits -region sources_highE_c${ccd_id}.reg

file_size=$(du sources_highE_c${ccd_id}.reg | awk '{print $1}')
if [ $file_size == 0 ]; then
    rm -f sources_highE_c${ccd_id}.reg
fi

# exclude sources, create light curve
if [ -f sources_highE_c${ccd_id}.reg ] ; then
    punlearn dmcopy
    dmcopy "${evt2name}[exclude sky=region(sources_highE_c${ccd_id}.reg)]" evt2_exhigh_c${ccd_id}.fits
    evt2high=evt2_exhigh_c${ccd_id}.fits
else
    evt2high=${evt2name}
fi

# Link to JSS code to modify exposure time
~/Documents/2020_Spring/summary/Scripts/Pre_Extract/fix_bg_exposures.py ${evt2high} bgevt2_c${ccd_id}_reproj.fits ${ccd_id}

echo "bgevt2_c${ccd_id}_reproj.fits can now be used to estimate the background."

# REMOVE FILES

rm -f highE.fits
rm -f bgevt2_c${ccd_id}.fits
rm -f bgevt2_c${ccd_id}_filt.fits
rm -f bgevt2_c${ccd_id}_newgainfilt.fits
rm -f wd*
rm -f evt2_highEsources_*_c${ccd_id}.fits

