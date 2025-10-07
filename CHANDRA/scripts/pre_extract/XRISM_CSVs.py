#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np
import os
import subprocess
from numpy import genfromtxt
import pandas
import matplotlib.pyplot as plt

with open ("Datasheet_regions.txt", 'rt') as myfile:		#Datasheet_regions file is self made, contains XRISMregion & XRISMregion1
    	regionlist = []
    	for myline in myfile:                
        	regionlist.append(myline.strip('.reg\n'))
print(regionlist)
i = 0

while i < len(regionlist):
	df = pd.DataFrame()
	mylines = []                             
	regiondata =  '%s_fit_out.txt'%(regionlist[i])		#Pulling data from "header" files 	
	with open (regiondata, 'rt') as myfile:
    		for myline in myfile:                # For each line, stored as myline,
        		mylines.append(myline)           # add its contents to mylines.

	nH = round(float(mylines[0][3:-1]),4)
	kT = round(float(mylines[3][3:-1]),4)
	Z = round(float(mylines[6][3:-1]),4)
	Flux = "{:.4E}".format((10**(float(mylines[13][10:-1]))))	#Reformatting Flux, too many sig figs
	
	regionfile = '%s.reg'%(regionlist[i])
	print(regionfile)
	
	#Pulling total counts from summed data (if evt2_bgsub doesn't exist replace with evt_summed)
	os.system('punlearn dmextract')
	#os.system('touch XRISMRegion_stack.fits')
	os.system('dmextract infile="evt2_summed_500_7000.fits[bin sky=region(%s)]" outfile=XRISMRegion_stack.fits opt=generic clobber=yes'%(regionfile))
	os.system('punlearn dmlist')
	os.system('dmlist "XRISMRegion_stack.fits[cols counts]" data outfile=data.txt')

	mylines = []    
	with open ('data.txt', 'rt') as myfile:			#Split out the data output from counts into lines
    		for myline in myfile:              
        		mylines.append(myline)          

	Counts = round(float(mylines[-1][10:-1]))		#Removing excess characters and spaces to convert to numerical value
	
	#Get total exposure time of all Chandra images
	os.system('punlearn dmlist')
	exposure = int(round(float(subprocess.check_output("dmkeypar evt2_summed_500_7000.fits LIVETIME echo+", shell=True)[:-2]),0))
	
	
	df["Stats"]=["Counts","Flux(erg/cm2/s)","Exposure(s)","nH(10^22)","kT","Metallicity(/Solar)"]
	df[1]=[Counts,Flux,exposure,nH,kT,Z]
	df.set_index('Stats', inplace=True)
	df.to_csv('%s.csv'%(regionlist[i]))			#Set this data into a table to be converted into a png
	i+=1
	
print(df)
print("Certain data will require manual input, do this before running XRISM_Table.py") 
