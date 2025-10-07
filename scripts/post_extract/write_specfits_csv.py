#!/usr/bin/env python3
from __future__ import print_function
import sys
import os
import numpy
import glob
from array import *

#fout = open("mekal/specfits_mekal.csv", "w")
#fout0 = open("mekal/specfits_mekal_read.csv", "w")

def write(argv):
    fout = open("specfits_%s.csv"%argv, "w")
    fout0 = open("specfits_read_%s.csv"%argv, "w")
    if argv == "proj" or argv == "deproj":
        fout.write("#rin rout n_h + - kT + - Z + - n + - stats log10flux + - chi dof reduced_chi-square\n")
        fout0.write("#rin,rout,n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square\n")
    else:
        fout.write("#n_h + - kT + - Z + - n + - stats log10flux + - chi dof reduced_chi-square volume\n")
        fout0.write("#n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square,volume\n")
    if argv == 'proj':
        reg = glob.glob("region*sum_grp100.pi")
        print(len(reg))
        if len(reg) == 0:
            reg = glob.glob("region*sum_grp30.pi")
    elif argv == 'deproj':
        reg= glob.glob("region*_deproj.pi")
    else:
        # reg = glob.glob(argv+"*sum_grp100.pi")
        reg = glob.glob(argv+"*_fit_out.txt")


    #To write both the radius profile and the spectral fit properties into one file.
    for i in range (0,len(reg)):
        #infile1 = open( "region"+str(i)+"_projctfit.txt", 'r' ) 
        if argv == 'proj':
            infile1 = open( "region"+str(i)+"_fit_out.txt", 'r' )
        if argv == 'deproj':
            infile1 = open( "region"+str(i)+"_fit_out_deproj.txt", 'r' )

        else:
            # if len(glob.glob(argv+"*_fit_out.txt")) == 1:
            #     infile1 = open( argv+"_fit_out.txt", 'r' )
            # else:
            infile1 = open(argv+str(i)+"_fit_out.txt", 'r')

        infile2 = open("profile_radii.txt",'r') #Can comment out the lines of code that pertain to writing radius if you want this separate from fitting results.

        count = 0
        liners = []
        for lines in infile2:

            if count == i:
                spl2 = lines.split()
                r_in = float(spl2[0])
                r_out = float(spl2[1])

            count += 1

        for line in infile1:

            spl = line.split()
            number = float(spl[1])
            liners.append(number)
     
        if argv == 'proj' or argv == 'deproj':
            fout.write('{} {}'.format (str(r_in),str(r_out)))
            fout0.write('{},{}'.format (str(r_in),str(r_out)))
        for a in range(len(liners)):
            if argv == 'proj' or argv == 'deproj':
                fout.write(" "+(str(liners[a])))
            else:
                fout.write((str(liners[a]))+" ")

        for a in range(len(liners)):
            if argv == 'proj' or argv == 'deproj':
                fout0.write(","+(str(liners[a])))
            else:
                fout0.write((str(liners[a]))+",")
        
        # fout.write(" "+str(liners[a-1]/liners[a]))
        # fout0.write(","+str(liners[a-1]/liners[a]))
        fout.write("\n")
        fout0.write("\n")
    fout.close()
    fout0.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python {} {}".format(sys.argv[0], 'proj/deproj/custom'))

    write(sys.argv[1])
