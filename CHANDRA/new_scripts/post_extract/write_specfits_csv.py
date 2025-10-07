#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import numpy
import glob
from array import *

#fout = open("mekal/specfits_mekal.csv", "w")
#fout0 = open("mekal/specfits_mekal_read.csv", "w")
fout = open("specfits.csv", "w")
fout0 = open("specfits_read.csv", "w")
fout.write("#rin,rout,n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square\n")
fout0.write("#rin,rout,n_h,+,-,kT,+,-,Z,+,-,n,+,-,stats,log10flux,+,-,chi,dof,reduced_chi-square\n")

#reg = glob.glob("region*sum_grp100.pi")
reg = glob.glob("region*.reg")


#To write both the radius profile and the spectral fit properties into one file.
for i in range (0,len(reg)):
    #infile1 = open( "region"+str(i)+"_projctfit.txt", 'r' ) 
    infile1 = open( "region"+str(i)+"_fit_out.txt", 'r' )
    #infile1 = open( "region"+str(i)+"_fit_out_new.txt", 'r' )
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
 

    fout.write('{} {}'.format (str(r_in),str(r_out)))
    fout0.write('{},{}'.format (str(r_in),str(r_out)))
    for a in range(len(liners)):
        fout.write(" "+(str(liners[a])))
    for a in range(len(liners)):
        fout0.write(","+(str(liners[a])))
    fout.write(" "+str(liners[a-1]/liners[a]))
    fout0.write(","+str(liners[a-1]/liners[a]))
    fout.write("\n")
    fout0.write("\n")
fout.close()
fout0.close()
