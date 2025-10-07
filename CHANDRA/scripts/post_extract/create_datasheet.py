#!/usr/bin/env python
import matplotlib.pyplot as plt
import csv
import pandas as pd
from fpdf import FPDF
import cv2

i=0 
pdf = FPDF()
#imagelist = ["XRISM_region1.png","XRISM_region1_table.png","XRISMspecfits1_proj.png","XRISMspecfits1_model.png","Metallicity.png","Temperature.png","Tcool.png","XRISM_region.png","XRISM_region_table.png","XRISMspecfits_proj.png","XRISMspecfits1_model.png","Metallicity.png","Temperature.png","Tcool.png"]
# imagelist is the list with all image filenames
imagelist = ["XRISM_region1.png","XRISM_region1_table.png","Centaurus_Updated_Fit.jpg","XRISMspecfits1_model.png","Metallicity.png","Temperature.png","Tcool.png","XRISM_region.png","XRISM_region_table.png","Centaurus_Updated_Fit.jpg","XRISMspecfits1_model.png","Metallicity.png","Temperature.png","Tcool.png"]
# imagelist is the list with all image filenames
while i <= len(imagelist)-1:
	i+=1
	print(i)							#Format for image placement (x,y,w,h)
	if i%7 == 0:
		pdf.add_page()
		pdf.set_font('Times','',20)
		pdf.cell(200,10,txt="Galaxy Cluster: Centaurus",align="C")		#Setting up the title on the first page
		pdf.image(imagelist[i-7],0,20,140,110)					#Image of the cluster
		pdf.image(imagelist[i-6],75,27,220,50)					#table of data values, adjustable in length 
		pdf.image(imagelist[i-5],0,135,220,160)				#The Spectra plotted out
		pdf.add_page()								#An additional page is added
		pdf.image(imagelist[i-4],15,15,190,110)					#The uncovoluted model of the spectra
		pdf.image(imagelist[i-3],-5,130,117,80)					#Profiles of cluster
		pdf.image(imagelist[i-2],102,130,117,80)
		pdf.image(imagelist[i-1],-5,210,117,80)
		

pdf.output("Centaurus_Datasheet_new.pdf", "F")				#Change the name, this can probably be automated!!!



#For Iron K flux, get the flux per pixel, and for calibration just use the Iron photon energy. Also just post Counts/s
#Find the number of pixels in a region and just multiply the flux
