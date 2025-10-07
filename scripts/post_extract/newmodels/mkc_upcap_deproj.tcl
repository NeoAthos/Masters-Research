# Fit each of the regions produced by contour binning

# Abell 2029
# set z  0.0773
# set n_h 0.033

# Abell 1835
# set z  0.2532
# set n_h 0.020

# Abell 1664
# set z  0.128
# set n_h 0.0886

# Abell 2597
# set z  0.0852
# set n_h 0.0248

# Phoenix
# set z  0.596
# set n_h 0.015

# # Abell 2052
# set z 0.0355
# set n_h 0.0270

# PKS0745
# set z 0.1028
# set n_h 0.4180

# MACS1347-11
# set z 0.451
# set n_h 0.0460

# Abell 85
# set z 0.0551
# set n_h 0.0278

# MS0735+7421
# set z 0.216
# set n_h 0.0328

# Abell 1795
# set z 0.063001
# set n_h 0.041

# Hydra-A
# set z 0.055
# set n_h 0.043

# RXCJ1504
# set z 0.215
# set n_h 0.0597

# Abell 133
set z 0.0566
set n_h 0.0153

# IC1262
# set z 0.0331
# set n_h 0.0178

# Abell 262
# set z 0.017
# set n_h 0.1250

# Abell 2626
# set z 0.0553
# set n_h 0.0383

# NGC 5044
# set z 0.009
# set n_h 0.0487

# Zw 7160
# set z 0.258
# set n_h 0.0318

set sum 0

# Load file list
set file [open "region_list_deproj.txt" r]
set data [read $file]
close $file
set data [split $data]

cpd specfits_deproj_mkc_upcap.ps/ps
#cpd new/specfits_new.ps/ps

set bases [lsearch -all -inline -not -regexp $data "grp30.pi"]
set bases [lreplace $bases end end]
#set bases [lsearch -all -inline -not -regexp $data "spec.pi"]

foreach base $bases {
    if {$sum==0} {
     #    set speclist [glob "${base}_*_grp100.pi"]
    	# set spec_sum [lsearch $speclist "${base}_sum_grp100.pi"]
    	# set speclist [lreplace $speclist $spec_sum $spec_sum]
        set speclist [glob "${base}_*_grp30.pi"]
        set spec_sum [lsearch $speclist "${base}_sum_grp30.pi"]
        set speclist [lreplace $speclist $spec_sum $spec_sum]
        set k 1
    	foreach x $speclist {
    	    data 1:${k} ${x}
    	    set k [expr $k+1]
            }
        set filenames $speclist
    }

    if {$sum==1} {
        set filenames [glob "${base}_sum_grp30.pi"]
        # set filenames [glob "${base}_deproj.pi"]
    }

    for {set i 0 } { $i < [llength $filenames] } { incr i } {
    	set j [expr $i+1]
    	data $j [lindex $filenames $i]
    }

    chatter ,0

    ignore bad
    ignore *:**-0.5
    ignore *:7.0-**
#ignore **:**-0.5,7.0 ;
    abund angr
    #abund lodd
    cosmo ,,0.7
    #statistic chi
    statistic cstat

    query yes
    
    model phabs(mkcflow + apec) & /*

    # phabs
    newpar 1 $n_h
    freeze 1 
    # mkcflow
    newpar 2 0.1
    thaw 2
    newpar 3 = 8
    newpar 4 0.5
    thaw 4
    newpar 5 $z
    freeze 5
    newpar 6 2
    newpar 7 30
    # apec
    newpar 8 5.0
    newpar 9 0.5
    thaw 9
    newpar 10 $z
    freeze 10
    newpar 11 5.0E-1
    
    setpl e
    setpl ylog on
    setpl xlog on

    renorm
    fit 1000
   # @~/scripts/fit_10.tcl
    
    plot data resid

    chatter ,10
    # error 2.706 1 2 3 4 5 ;# Calculates the 2.706-sigma confidence or the 90% confidence range
    error 1. 2 4 7 8 9 11 ;#Calculates the 1-sigma confidence range or the 68.3% confidence range

    # error maximum 1.2 3 5

    show param
    show fit

    # Print out results
    set outfile [open "${base}_mkc_upcap_deproj_fit_out.txt" w]
#set outfile [open "new/${base}_fit_out.txt" w]

    tclout param 1
    scan $xspec_tclout "%f" nHval
    tclout error 1
    scan $xspec_tclout "%f %f" nHval_low nHval_upp
    puts $outfile "nH $nHval"
    puts $outfile "nH_uerr [expr $nHval_upp - $nHval]"
    puts $outfile "nH_lerr [expr $nHval_low - $nHval]"

    tclout param 2
    scan $xspec_tclout "%f" tempL
    tclout error 2
    scan $xspec_tclout "%f %f" tempL_low tempL_upp
    puts $outfile "kT_low $tempL"
    puts $outfile "kT_low_uerr [expr $tempL_upp - $tempL]"
    puts $outfile "kT_low_lerr [expr $tempL_low - $tempL]"

    # tclout param 3
    # scan $xspec_tclout "%f" tempU
    # tclout error 3
    # scan $xspec_tclout "%f %f" tempU_low tempU_upp
    # puts $outfile "kT_up $tempU"
    # puts $outfile "kt_up_uerr [expr $tempU_upp - $tempU]"
    # puts $outfile "kt_up_lerr [expr $tempU_low - $tempU]"
#    puts $outfile "Z_uerr [expr 0.]"
#    puts $outfile "Z_lerr [expr 0.]"

    tclout param 4
    scan $xspec_tclout "%f" abund1
    tclout error 4
    scan $xspec_tclout "%f %f" abund1_low abund1_upp
    puts $outfile "Z1 $abund1"
    puts $outfile "Z1_uerr [expr $abund1_upp - $abund1]"
    puts $outfile "Z1_lerr [expr $abund1_low - $abund1]"

    tclout param 7
    scan $xspec_tclout "%f" norm1
    tclout error 7
    scan $xspec_tclout "%f %f" norm1_low norm1_upp
    puts $outfile "Mdot $norm1"
    puts $outfile "Mdot_uerr [expr $norm1_upp - $norm1]"
    puts $outfile "Mdot_lerr [expr $norm1_low - $norm1]"

    tclout param 8
    scan $xspec_tclout "%f" temp
    tclout error 8
    scan $xspec_tclout "%f %f" temp_low temp_upp
    puts $outfile "kT $temp"
    puts $outfile "kT_uerr [expr $temp_upp - $temp]"
    puts $outfile "kT_lerr [expr $temp_low - $temp]"

    tclout param 9
    scan $xspec_tclout "%f" abund2
    tclout error 9
    scan $xspec_tclout "%f %f" abund2_low abund2_upp
    puts $outfile "Z2 $abund2"
    puts $outfile "Z2_uerr [expr $abund2_upp - $abund2]"
    puts $outfile "Z2_lerr [expr $abund2_low - $abund2]"
    # puts $outfile "Z_uerr [expr 0.]"
    # puts $outfile "Z_lerr [expr 0.]"

    tclout param 11
    scan $xspec_tclout "%f" norm2
    tclout error 11
    scan $xspec_tclout "%f %f" norm2_low norm2_upp
    puts $outfile "Norm $norm2"
    puts $outfile "Norm_uerr [expr $norm2_upp - $norm2]"
    puts $outfile "Norm_lerr [expr $norm2_low - $norm2]"


    # Output statistic value (chi^2 or cstat)
    tclout stat
    scan $xspec_tclout "%f" chi2
    puts $outfile "Stat $chi2"

    tclout dof
    scan $xspec_tclout "%f" dof
    puts $outfile "dof $dof"

    puts $outfile "red_chi2 [expr $chi2/$dof]"




    editmod phabs*cflux(mkcflow + apec) & /*
    newpar 2 0.1
    newpar 3 100.0
    newpar 4 -12.0
#newpar 4 -13.0
    # freeze 2
    query yes 
    fit 100
    error 4

    tclout param 4
    scan $xspec_tclout "%f" log10Flux
    tclout error 4
    scan $xspec_tclout "%f %f" log10Flux_low log10Flux_upp
    puts $outfile "log10Flux $log10Flux"
    puts $outfile "log10Flux_uerr [expr $log10Flux_upp - $log10Flux]"
    puts $outfile "log10Flux_lerr [expr $log10Flux_low - $log10Flux]"

    tclout stat test
    scan $xspec_tclout "%f" chi2
    puts $outfile "Chi2 $chi2"

    tclout dof
    scan $xspec_tclout "%f" dof
    puts $outfile "dof $dof"
    puts $outfile "red_chi2 [expr $chi2/$dof]"

    close $outfile

    chatter ,0

    model none
    data none

}

exit
/*
