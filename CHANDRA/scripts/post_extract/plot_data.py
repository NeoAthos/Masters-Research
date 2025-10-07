#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

df = pd.read_csv('massdata.csv')
print(df)
radius = df['x']
cooling_time = df['y']
fig, ax = plt.subplots()
ax.plot(radius, cooling_time, linestyle='-',marker='o', markeredgecolor='black', color = 'grey', markerfacecolor = 'red')
#ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
#plt.title("Cluster Metallicities")
ax.axvline(x = 7.04, color = 'grey', linestyle=':')
ax.set_xlabel("Radius (kpc)")
ax.set_ylabel("Gravitating Mass $(M_{\odot})$")
plt.tick_params(which="major", direction="in", width=1.25, length =8)
plt.tick_params(which="minor", direction="in", width=1.25, length =4)
#plt.ylim(0,1.8)
plt.xscale('log')
plt.yscale('log')
ax.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f'))
#plt.show()
fig.savefig('mass.pdf')
plt.close(fig)



#define x as 200 equally spaced values between the min and max of original x 
#xnew = np.linspace(radius.min(), radius.max(), 500) 

#define spline
#spl = make_interp_spline(radius, Z, k=3)
#y_smooth = spl(xnew)

#create smooth line chart 
#plt.plot(xnew, y_smooth)
#plt.xscale('log')
#plt.show()

