#!/usr/bin/env bash

#for reg in xaf_*.reg; do
#for reg in center.reg; do
for reg in region*.reg; do

    # make .dat file for header modification
    outerrad=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f4 |cut -d')' -f1 )
    outerrad=$(cut -f2 ${reg}|cut -d'-' -f1 |cut -d',' -f4 |cut -d')' -f1 )
    echo "$outerrad"
    # r1=$(echo ${outerrad}*0.0082 |bc -l)       # 0.0082 = 0.492/60 = deproj1 in arcmin
    r1=$(echo ${outerrad}*0.492 |bc -l)       # 0.492 = deproj2 in arcsec
    echo "$r1"
    r2=${r1}
    orientation="0.0"
    #angle1=$(cut -f2 ${reg}|cut -d'-' -f1 |cut -d',' -f5|cut -d')' -f1)
    #angle1=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f5 |cut -d')' -f1 )
    #angle2=$(cut -f2 ${reg}|cut -d'-' -f1 |cut -d',' -f6 |cut -d')' -f1)
    #angle1=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f5)
    angle2=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f6 |cut -d')' -f1)
    if [ -z $angle2 ]
    then   
        angle2="360.0"
    fi
     # 2 regions per region file
#    outerrad=$(cut -d$'\n' -f3 ${reg} |cut -d',' -f4 |cut -d')' -f1 ) 
#    radius=$(echo ${outerrad}*0.0082 |bc -l)

    ######## ellipse
    #major=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f3 )
    #echo "$major"
    #minor=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f4 )
    #orientation=$(cut -d$'\n' -f2 ${reg} |cut -d',' -f5 |cut -d')' -f1 )
    #r1=$(echo ${major}*0.0082 |bc -l)
    #r2=$(echo ${minor}*0.0082 |bc -l)

#change 'add' to 'delete' to erase values

    echo "#add
XFLT0001=${r1}
XFLT0002=${r2}
XFLT0004=${angle1}
XFLT0005=${angle2}
XFLT0003=${orientation}" >> ${reg/.reg/.dat}

#XFLT0004=${angle1}
#XFLT0005=${angle2}

    punlearn dmhedit
    spec="${reg/.reg}_*_grp100.pi"
    # spec="${reg/.reg}_*_grp100.pi"
    # spec="${reg/.reg}_*_grp30.pi"
    # spec="${reg/.reg}_*_grp10.pi"
    spec1="${reg/.reg}_*_spec.pi"

    for x in $spec; do
	dmhedit ${x} ${reg/.reg/.dat}
	done

    for x in $spec1; do
    dmhedit ${x} ${reg/.reg/.dat}
    done

    #dmhedit ${reg/.reg/_sum_spec.pi} ${reg/.reg/.dat}
#    dmhedit ${reg/.reg/_*_grp20.pi} ${reg/.reg/.dat}
done 
