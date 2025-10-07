#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np
import os
from numpy import genfromtxt
import pandas
import matplotlib.pyplot as plt

with open ("Datasheet_regions.txt", 'rt') as myfile:
    	regionlist = []
    	for myline in myfile:                
        	regionlist.append(myline.strip('.reg\n'))
print(regionlist)
i = 0

while i < len(regionlist):
	df = pandas.read_csv('%s.csv'%(regionlist[i]), delimiter=',') #Pulls from the XRISM_CSVs csvs, you can manually edit it between these two steps
	df.set_index('Stats', inplace=True)
	
	fig, ax = plt.subplots(figsize=(12, 2.5)) # set size frame
	ax.xaxis.set_visible(False)  # hide the x axis
	ax.yaxis.set_visible(False)  # hide the y axis
	ax.set_frame_on(False)  # no visible frame
	tabla = table(ax, df, loc='upper center', colWidths=[0.17]*len(df.columns))
	tabla.auto_set_font_size(False) #True = set fontsize manually
	tabla.set_fontsize(11) # if ++fontsize is necessary ++colWidths
	tabla.scale(1.1, 1.1) # change size table
	plt.savefig('%s_table.png'%(regionlist[i]), transparent=True)
	print('%s_table.png'%(regionlist[i]))
	print(df)
	i+=1
