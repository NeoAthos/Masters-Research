#!/usr/bin/env bash
##############################################################################
# Version 1.0: Added choice of not applying CTI correction
#
##############################################################################
set -x
screen.log
ls

# Set file names
gzip -d ../primary/*.gz
gzip -d ../secondary/*.gz
evt1name=$(ls ../secondary/*_evt1.fits)

echo -n "If there is more than one pcad file need to supply list of pcad files."

# GET VERSION + OBS DETAILS
dmkeypar $evt1name READMODE echo+
datamode=$(dmkeypar ${evt1name} DATAMODE echo+)
dmkeypar $evt1name ASCDSVER echo+
version=$(dmkeypar ${evt1name} ASCDSVER echo+)
temp=$(dmkeypar ${evt1name} FP_TEMP echo+)
dmkeypar $evt1name DETNAM echo+

echo -n "FP_TEMP is given in Kelvin ~153K (-120C)"
echo -n "If not Timed (V)Faint mode need different eventdef parameter!"

echo -n "Go ahead with reprocessing?"
read -e continue

if [[ $continue = "y" ]] ; then

    echo -n "The message 'WARNING: File /tmp/hotpixel_list.fits does not have any rows' just means no hot pixels were identified in the observation"

    echo -n "The message: 'WARNING: Event island contains 1 or more bad pixels.' may be ignored"

    # Run reprocessing script, default is also to destreak
    
    if [[ $datamode = VFAINT ]] ; then
	chandra_repro ../ ./ verbose=2 check_vf_pha=yes
    else
	chandra_repro ../ ./ verbose=2 check_vf_pha=no
    fi

    # Change name of bpix file
    bpixname=$(ls *_repro_bpix1.fits)
    bpixnew=${bpixname/_repro_bpix1.fits/_new_bpix1.fits}
    mv $bpixname $bpixnew

    # SET bad pixel file here.
    punlearn ardlib
    pset acis_set_ardlib absolutepath=yes
    acis_set_ardlib ${bpixnew}

    #  Note that repro script also filters out bad grades and applies gtis
    newevt2=$(ls *_evt2.fits)

    # LC_CLEAN FOR FLARES
    
    echo -n "Enter the ccd id: "
    read ccd_id

    # Check a ccd for flares
    echo -n "Use which ccd to check for flares?"
    read ccd_flare

    if [[ ${ccd_flare} = 7 ]] ; then
	interval=1037.12
	e_low=2500
	e_high=7000    
    elif [[ ${ccd_flare} = 5 ]] ; then
	interval=1037.12
	e_low=2500
	e_high=6000
    else
	interval=259.28
	e_low=300
	e_high=12000
    fi

    # cut for relevant energy range
    punlearn dmcopy
    dmcopy "${newevt2}[energy=${e_low}:${e_high},ccd_id=${ccd_flare}]" evt2_c${ccd_flare}.fits

    # Run a basic source detection => wavsources_flares.reg
    pcad=$(ls pcadf*.fits)
    punlearn skyfov
    skyfov ${newevt2} chips.reg aspect=${pcad}


    # Temporary work around
    punlearn dmcopy
    dmcopy "evt2_c${ccd_flare}.fits[sky=region(chips.reg[ccd_id=${ccd_flare}])]" tempfile.fits
 
    punlearn wtransform 
    pset wtransform clobber=yes
 
    punlearn wavdetect
    pset wavdetect infile=tempfile.fits
    pset wavdetect outfile=evt2_c${ccd_flare}_out.fits
    pset wavdetect scellfile=evt2_c${ccd_flare}_scell.fits
    pset wavdetect imagefile=evt2_c${ccd_flare}_image.fits
    pset wavdetect defnbkgfile=evt2_c${ccd_flare}_defnbkg.fits
    pset wavdetect regfile=evt2_c${ccd_flare}_out.reg
    pset wavdetect ellsigma=5
    pset wavdetect clobbe=yes
    wavdetect

    rm -f tempfile.fits

    # Locate any sources (above 20% of background)  
    echo -n "Look at sources detected + modify region file:"
    ds9 evt2_c${ccd_flare}.fits -region evt2_c${ccd_flare}_out.reg

    file_size=$(du evt2_c${ccd_flare}_out.reg | awk '{print $1}')
    if [ $file_size == 0 ]; then
	rm -f evt2_c${ccd_flare}_out.reg
    fi

    # exclude sources, create light curve
    if [ -f evt2_c${ccd_flare}_out.reg ] ; then
	punlearn dmcopy
	dmcopy "evt2_c${ccd_flare}.fits[exclude sky=region(evt2_c${ccd_flare}_out.reg)]" evt2_c${ccd_flare}_bg.fits
    else
	cp evt2_c${ccd_flare}.fits evt2_c${ccd_flare}_bg.fits
    fi

    punlearn dmextract
    dmextract "evt2_c${ccd_flare}_bg.fits[bin time=::${interval}]" evt2_c${ccd_flare}_bg.lc opt=ltc1

    # Flare Filtering

    # Create gti for event file
    mv evt2_c${ccd_flare}_bg.lc lcurve.lc
    sherpa /home/neolnx/Documents/XRISMprep/scripts/pre_extract/blanksky.chp
    mv lcurve.lc evt2_c${ccd_flare}_bg.lc
    mv lcurve.lc.ps lcurve.ps

    # Apply final gti to ccd of observation
    punlearn dmcopy
    outevt1gtiname=${newevt2/_repro_evt2.fits/_evt1gti.fits}
    dmcopy "${newevt2}[@evt2_bg.gti]" ${outevt1gtiname}
#    cp ${newevt2} ${outevt1gtiname}

    # Apply filtering from Cookbook
    outevt2name=${outevt1gtiname/_evt1gti.fits/_evt2.fits}
    if [[ $datamode = VFAINT ]] ; then
	punlearn fcopy
	fcopy "${outevt1gtiname}[events][status==bxxxxxxxx0xxxxxxxxxxxxxxxxxxxxxxx]" ${outevt2name}
    else
	cp ${outevt1gtiname} ${outevt2name}
    fi

    # REMOVE FILES
#    rm -f ${newevt2}
    rm -f evt2_c${ccd_flare}_scell.fits
    rm -f evt2_c${ccd_flare}_image.fits
    rm -f evt2_c${ccd_flare}_defnbkg.fits
#    rm -f ${outevt1gtiname}
    rm -f wd*
#    exit
fi

