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

# Abell 2052
# set z 0.0355
# # set n_h 0.0270
# set n_h 0.0285

# PKS0745
# set z 0.1028
# set n_h 0.4180

# MACS1347-11
# set z 0.451
# set n_h 0.0460

# Abell 85
set z 0.0551
set n_h 0.0278

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
# set z 0.0566
# set n_h 0.0153

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

# Cygnus A
# set z 0.056075
# set n_h 0.2720


set sum 1

# Load file list
set file [open "region_list.txt" r]
set data [read $file]
close $file
set data [split $data]

cpd specfits_model4_proj.ps/ps
#cpd new/specfits_new.ps/ps

set bases [lsearch -all -inline -not -regexp $data "grp100.pi"]
set bases [lreplace $bases end end]
#set bases [lsearch -all -inline -not -regexp $data "spec.pi"]

foreach base $bases {
    if {$sum==0} {
     #    set speclist [glob "${base}_*_grp100.pi"]
    	# set spec_sum [lsearch $speclist "${base}_sum_grp100.pi"]
    	# set speclist [lreplace $speclist $spec_sum $spec_sum]
        set speclist [glob "${base}_*_grp100.pi"]
        set spec_sum [lsearch $speclist "${base}_sum_grp100.pi"]
        set speclist [lreplace $speclist $spec_sum $spec_sum]
        set k 1
    	foreach x $speclist {
    	    data 1:${k} ${x}
    	    set k [expr $k+1]
            }
        set filenames $speclist
    }

    if {$sum==1} {
        set filenames [glob "${base}_sum_grp100.pi"]
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
    # ignore *:1.8-2.1 ;
    abund angr
    #abund lodd
    cosmo ,,0.7
    # statistic chi
    statistic cstat

    query yes
    
    model mekal & /*

    # mekal
    newpar 1 2.72
    newpar 2 $n_h
    freeze 2
    newpar 3 0.53
    thaw 3
    newpar 4 $z
    freeze 4
    newpar 5 2
    newpar 6 5.0E-1
    
    setpl e
    setpl ylog on
    setpl xlog on

    renorm
    fit 10000
   # @~/scripts/fit_10.tcl
    
    plot data resid

    chatter ,10
    # error 2.706 1 2 3 4 5 ;# Calculates the 2.706-sigma confidence or the 90% confidence range
    # error 1. 1 2 3 4 5 ;#Calculates the 1-sigma confidence range or the 68.3% confidence range
    error 1. 1 3 5 6 ;#Calculates the 1-sigma confidence range or the 68.3% confidence range

    # error maximum 1.2 3 5

    show param
    show fit

    # Print out results
    set outfile [open "${base}_model4_fit_out.txt" w]
#set outfile [open "new/${base}_fit_out.txt" w]

    tclout param 1
    scan $xspec_tclout "%f" kT
    tclout error 1
    scan $xspec_tclout "%f %f" kT_low kT_upp
    puts $outfile "kT $kT"
    puts $outfile "kT_uerr [expr $kT_upp - $kT]"
    puts $outfile "kT_lerr [expr $kT_low - $kT]"

    tclout param 2
    scan $xspec_tclout "%f" nH
    # tclout error 2
    # scan $xspec_tclout "%f %f" tempL_low tempL_upp
    # puts $outfile "kT_low $tempL"
    # puts $outfile "kT_low_uerr [expr $tempL_upp - $tempL]"
    # puts $outfile "kT_low_lerr [expr $tempL_low - $tempL]"

    tclout param 3
    scan $xspec_tclout "%f" abund
    tclout error 3
    scan $xspec_tclout "%f %f" abund_low abund_upp
    puts $outfile "Z $abund"
    puts $outfile "Z_uerr [expr $abund_upp - $abund]"
    puts $outfile "Z_lerr [expr $abund_low - $abund]"

    tclout param 6
    scan $xspec_tclout "%f" norm
    tclout error 6
    scan $xspec_tclout "%f %f" norm_low norm_upp
    puts $outfile "Mdot $norm"
    puts $outfile "Mdot_uerr [expr $norm_upp - $norm]"
    puts $outfile "Mdot_lerr [expr $norm_low - $norm]"

    
    # Output statistic value (chi^2 or cstat)
    tclout stat
    scan $xspec_tclout "%f" chi2
    puts $outfile "Stat $chi2"

    tclout dof
    scan $xspec_tclout "%f" dof
    puts $outfile "dof $dof"
    puts $outfile "red_chi2 [expr $chi2/$dof]"

    editmod cflux(mekal) & /*
    newpar 1 0.1
    newpar 2 100.0
    newpar 3 -12.0
#newpar 4 -13.0
    freeze 8
    query yes 
    fit 10000
    error 4

    tclout param 3
    scan $xspec_tclout "%f" log10Flux
    tclout error 3
    scan $xspec_tclout "%f %f" log10Flux_low log10Flux_upp
    puts $outfile "log10Flux $log10Flux"
    puts $outfile "log10Flux_uerr [expr $log10Flux_upp - $log10Flux]"
    puts $outfile "log10Flux_lerr [expr $log10Flux_low - $log10Flux]"

    tclout stat test
    scan $xspec_tclout "%f" chi2
    puts $outfile "Chi $chi2"

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
