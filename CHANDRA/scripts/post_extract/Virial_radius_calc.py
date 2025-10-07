#!/usr/bin/env python
import matplotlib.pyplot as plt
import csv
import pandas as pd
from fpdf import FPDF
import cv2
import sys
import math
import numpy as np

#using Lambda CDM model

cluster_name = sys.argv[1] #Name of the cluster
#File = "%_project_properties.csv"%
z = float(sys.argv[2]) #Redshift
file_name = cluster_name+"_project_properties.csv"

df = pd.read_csv(file_name)

mass = df['Mgas']
r = df['#r_avg']
#print(r)

Omega_lam = 0.7
Omega_m = 0.3

Hubble_const = 70
G = 6.674e-11
i = 0
H = Hubble_const*3.24e-20*np.sqrt(((Omega_m*(1+z)**3 + Omega_lam)))
M = 0.94E15 * 1.989E30
#print(((Omega_m*(1+z)**3 + Omega_lam)))

#TOP = (200*(3*H**2)/(8*math.pi*G))**(-1)
#print(TOP)
#BOTTOM = (3*(1.989e30*0.94e15)/(4*math.pi))
#print(BOTTOM)
TOP = (200*(3*H**2)/(8*math.pi*G))
print(TOP)
BOTTOM = (3*(M)/(4*math.pi))
test1 = (TOP/BOTTOM)**(-1/3)
test_radius = (200*(H**2/(2*G*M)))**(-1/3)


#test_radius = ((TOP/BOTTOM)**(-1))**(1/3)
print("test")
print(test1)
print(test_radius)

while i <= len(r)-1:
	mass_kg = mass[i]*1.989e30
	r_m = r[i]*3.086e19
	r200 = r_m/(1970*3.086e19)
	print(r200)
	if i > 0:
		print("Slope:", (mass[i] - mass[i-1])/(r[i] - r[i-1]))
	virial_density = ((3*H**2)/(8*math.pi*G)) #
	System_density = 3*mass_kg/(4*math.pi*r_m**3)

	#print(virial_density)
	print(System_density/virial_density)
	print(r[i],"kpc")
	i+=1
#For Iron K flux, get the flux per pixel, and for calibration just use the Iron photon energy. Also just post Counts/s
#Find the number of pixels in a region and just multiply the flux
