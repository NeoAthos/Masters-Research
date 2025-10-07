#!/usr/bin/env python3
from __future__ import print_function
import sys
import os
import numpy
import glob
from array import *
from natsort import natsorted
import re

#fout = open("mekal/specfits_mekal.csv", "w")
#fout0 = open("mekal/specfits_mekal_read.csv", "w")

def write(argv):
    print(argv)
    fout = open("specfits_%s_new.csv"%argv, "w")
    fout0 = open("specfits_read_%s_new.csv"%argv, "w")
    if argv == "proj" or argv == "deproj":
        fout.write("#rin rout n_h + - kT + - Z + - n + - stats log10flux + - chi dof reduced_chi-square\n")
        fout0.write("#rin,rout,n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square\n")
    elif argv == "mkcfixedproj" or "mkcfixeddeproj":
        fout.write("#n_h + - Z1 + - Mdot + - kT + - Z + - n + - stats reduced_chi-square\n")
        fout0.write("#n_h,+,-,Z1,+,-,Mdot,+,-,kT,+,-,Z,+,-,n,+,-,stats,reduced_chi-square\n")
    else:
        fout.write("#rin rout n_h + - kT + - Z + - n + - stats log10flux + - chi dof reduced_chi-square volume\n")
        fout0.write("#rin,rout,n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square,volume\n")
    if argv == 'proj':
        reg = natsorted(glob.glob("region*sum_grp100.pi"))
        print(len(reg))
        if len(reg) == 0:
            reg = natsorted(glob.glob("region*sum_grp30.pi"))
            print(len(reg))
            if len(reg)==0:
                reg = open('region_list.txt', 'r').readlines()
                print(len(reg))
    elif argv == 'deproj':
        reg = natsorted(glob.glob("region*_deproj.pi"))
    elif argv == 'mkcfixedproj':
        reg = natsorted(glob.glob("region*_mkc_fixed_proj*.txt"))
    elif argv == 'mkcfixeddeproj':
        reg = natsorted(glob.glob("region*_mkc_fixed_deproj*.txt"))
    else:
        # reg = glob.glob(argv+"*sum_grp100.pi")
        reg = natsorted(glob.glob(argv+"*_fit_out_new.txt"))

    # print(reg)

    #To write both the radius profile and the spectral fit properties into one file.
    for i in range (0,len(reg)):
        #infile1 = open( "region"+str(i)+"_projctfit.txt", 'r' ) 
        region = [int(s) for s in re.findall(r'\b\d+\b', reg[i])]
        print('REGION: ', region)
        if i == region:
            if argv == 'proj':
                infile1 = open( "region"+str(i)+"_fit_out_new.txt", 'r' )
            if argv == 'deproj':
                infile1 = open( "region"+str(i)+"_fit_out_deproj_new.txt", 'r' )
        if argv == 'mkcfixedproj':
            infile1 = open( reg[i], 'r' )
        if argv == 'mkcfixeddeproj':
            infile1 = open( reg[i], 'r' )

        # else:
        #     # if len(glob.glob(argv+"*_fit_out_new.txt")) == 1:
        #     #     infile1 = open( argv+"_fit_out_new.txt", 'r' )
        #     # else:
        #     infile1 = open(argv+str(i)+"_fit_out_new.txt", 'r')

        infile2 = open("profile_radii.txt",'r') #Can comment out the lines of code that pertain to writing radius if you want this separate from fitting results.
        liners = []

        if argv in ['proj', 'deproj']:
            count = 0
            for lines in infile2:

                if count == i:
                    spl2 = lines.split()
                    r_in = float(spl2[0])
                    r_out = float(spl2[1])

                count += 1
        elif argv in ['mkcfixedproj', 'mkcfixeddeproj']:
            # count = 0
            liners = []
            lines = infile2[region]
            spl2 = lines.split()
            r_in = float(spl2[0])
            r_out = float(spl2[1])

        for line in infile1:

            spl = line.split()
            number = float(spl[1])
            liners.append(number)
     
        if argv in ['proj','deproj','mkcfixedproj','mkcfixeddeproj']:
            fout.write('{} {}'.format (str(r_in),str(r_out)))
            fout0.write('{},{}'.format (str(r_in),str(r_out)))
        for a in range(len(liners)):
            if argv in ['proj','deproj','mkcfixedproj','mkcfixeddeproj']:
                fout.write(" "+(str(liners[a])))
            else:
                fout.write((str(liners[a]))+" ")

        for a in range(len(liners)):
            if argv in ['proj','deproj','mkcfixedproj','mkcfixeddeproj']:
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
        print("Use: python {} {}".format(sys.argv[0], 'proj/deproj/mkcfixedproj/mkcfixeddeproj/custom'))

    write(sys.argv[1])

