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
set z  0.0852
set n_h 0.0248

# Phoenix
# set z  0.596
# set n_h 0.015

# Abell 2052
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

# Zw 7160
# set z 0.258
# set n_h 0.0318

# AS1101
# set z 0.058
# set n_h 0.039

# ZwCl 3146
# set z 0.291
# set n_h 0.0246

# Abell 2199
# set z 0.0302
# set n_h 0.039

# MACS1423+24
# set z 0.543
# set n_h 0.022

# Zw2701
# set z 0.215
# set n_h 0.00751

# RXCJ 1539
# set z 0.07576
# set n_h 0.0769


set sum 0

# Load file list
set file [open "region_list_deproj.txt" r]
set data [read $file]
close $file
set data [split $data]

cpd specfits_deproj.ps/ps
#cpd new/specfits_new.ps/ps

# set bases [lsearch -all -inline -not -regexp $data "grp100.pi"]
# set bases [lsearch -all -inline -not -regexp $data "grp30.pi"]
set bases [lsearch -all -inline -not -regexp $data "deproj.pi"]
set bases [lreplace $bases end end]
#set bases [lsearch -all -inline -not -regexp $data "spec.pi"]


foreach base $bases {

    if {$sum==0} {
        # set speclist [glob "${base}_*_grp100.pi"]
    	# set spec_sum [lsearch $speclist "${base}_sum_grp100.pi"]
    	# set speclist [lreplace $speclist $spec_sum $spec_sum]
        # set speclist [glob "${base}_*_grp100.pi"]
        # set speclist [glob "${base}_*_grp30.pi"]
        set speclist [glob "${base}_*_deproj.pi"]
        # set speclist [glob "${base}_*_spec.pi"]
        # set spec_sum [lsearch $speclist "${base}_sum_grp100.pi"]
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
        set filenames [glob "${base}_deproj.pi"]
    }

    for {set i 0 } { $i < [llength $filenames] } { incr i } {
    	set j [expr $i+1]
    	data $j [lindex $filenames $i]
    }

    chatter ,0

    ignore bad
    # ignore *:**-0.3
    ignore *:**-0.5
    ignore *:7.0-**
    # ignore **:**-0.5,7.0 ;
    abund angr
    # abund lodd
    cosmo ,,0.7
    statistic chi
    # statistic cstat

    query yes
    
    model phabs(apec) & /*

    newpar 1 $n_h
    freeze 1 
    newpar 2 3.5
    newpar 3 0.5
    thaw 3
    newpar 4 $z
    freeze 4
    newpar 5 1.0E-6
    
    setpl e
    setpl ylog on
    setpl xlog on

    renorm
    fit 1000
    # @~/scripts/fit_10.tcl
    
    plot data resid

    chatter ,10
    # error 2.706 1 2 3 4 5 ;# Calculates the 2.706-sigma confidence or the 90% confidence range
    error 1. 2 3 5 ; # Calculates the 1-sigma confidence range or the 68.3% confidence range

    # error maximum 1.2 3 5

    show param
    show fit

    # Print out results
    set outfile [open "${base}_fit_out_deproj.txt" w]
    # set outfile [open "new/${base}_fit_out.txt" w]

    tclout param 1
    scan $xspec_tclout "%f" nHval
    tclout error 1
    scan $xspec_tclout "%f %f" nHval_low nHval_upp
    puts $outfile "nH $nHval"
    puts $outfile "nH_uerr [expr $nHval_upp - $nHval]"
    puts $outfile "nH_lerr [expr $nHval_low - $nHval]"

    tclout param 2
    scan $xspec_tclout "%f" temp
    tclout error 2
    scan $xspec_tclout "%f %f" temp_low temp_upp
    puts $outfile "kT $temp"
    puts $outfile "kT_uerr [expr $temp_upp - $temp]"
    puts $outfile "kT_lerr [expr $temp_low - $temp]"

    tclout param 3
    scan $xspec_tclout "%f" abund
    tclout error 3
    scan $xspec_tclout "%f %f" abund_low abund_upp
    puts $outfile "Z $abund"
    puts $outfile "Z_uerr [expr $abund_upp - $abund]"
    puts $outfile "Z_lerr [expr $abund_low - $abund]"
    # puts $outfile "Z_uerr [expr 0.]"
    # puts $outfile "Z_lerr [expr 0.]"

    tclout param 5
    scan $xspec_tclout "%f" norm
    tclout error 5
    scan $xspec_tclout "%f %f" norm_low norm_upp
    puts $outfile "Norm $norm"
    puts $outfile "Norm_uerr [expr $norm_upp - $norm]"
    puts $outfile "Norm_lerr [expr $norm_low - $norm]"



    # Output statistic value (chi^2 or cstat)
    tclout stat
    scan $xspec_tclout "%f" chi2
    puts $outfile "Stat $chi2"
    editmod phabs*cflux(apec) & /*
    newpar 2 0.1
    newpar 3 100.0
    newpar 4 -12.0
    # newpar 4 -13.0
    freeze 8
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
    scan $xspec_tclout "%f" chi
    puts $outfile "Chi $chi"

    tclout dof
    scan $xspec_tclout "%f" dof
    puts $outfile "dof $dof"
    puts $outfile "red_chi2 [expr $chi/$dof]"

    close $outfile

    chatter ,0

    model none
    data none

}

exit
/*
