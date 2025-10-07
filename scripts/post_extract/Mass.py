#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

df = pd.read_csv('Star_formation.csv')
cluster_loc = [2,16,29,44,61,78,91,102,107,121,133,142,156]
#A478
norm = mpl.colors.Normalize(vmin=0, vmax=5)
cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.jet)
cmap.set_array([])
i = 0
while i <= len(cluster_loc)-1:
	cluster = cluster_loc[i]-2
	if i != len(cluster_loc)-1:
		next_cluster = cluster_loc[i+1]-2
	else:
		next_cluster = 170 - 2
	cluster_name = df.loc[cluster,'Cluster']
	radius = np.array(df.loc[cluster+1:next_cluster-1,'R/R2500'].tolist())
	Z = np.array(df.loc[cluster+1:next_cluster-1,'Z'].tolist())
	Mass = df.loc[cluster,'Mass']
	plt.plot(radius,Z,c=cmap.to_rgba(Mass))
	print(Mass)
	print(cluster_name)
	print(radius)
	i+=1
#print(df)


cbar = plt.colorbar(cmap)
cbar.set_label("$M_{2500} (x10^{14} M_{sun})$")
plt.title("Cluster Metallicities")
plt.xlabel("$Radius (R/R_{2500})$")
plt.ylabel("$Metallicity (Z/Z_{solar})$")
plt.ylim(0,1.8)
plt.xscale('log')
plt.show()




#define x as 200 equally spaced values between the min and max of original x 
#xnew = np.linspace(radius.min(), radius.max(), 500) 

#define spline
#spl = make_interp_spline(radius, Z, k=3)
#y_smooth = spl(xnew)

#create smooth line chart 
#plt.plot(xnew, y_smooth)
#plt.xscale('log')
#plt.show()

