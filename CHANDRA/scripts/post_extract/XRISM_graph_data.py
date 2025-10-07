#!/usr/bin/env python
import matplotlib.pyplot as plt
import csv
import pandas as pd

df = pd.read_csv('HydraA_project_properties.csv')	#Change the name per cluster, this is just taking data from the standard csvs
#df.head()			#and plotting it out into concise pngs, remember that point source changes will not really effect this
print(df)
rerr = df['dr']
terr = [df['kT_p'],df['kT_m']]
zerr = [df['Z_p'],df['Z_m']]
tcoolerr = [df['tcool_p'],df['tcool_m']]
r = df['#r_avg']
t = df['kT']
z = df['Z']
cool = df['tcool']

plt.figure(figsize=(8,5))
plt.scatter(r,t, s=10)
plt.errorbar(r,t,xerr=rerr,yerr=terr,color='k',ls = "None",alpha=0.7)
plt.xscale("log")
plt.xlabel("Radius (kpc)")
plt.ylabel("kT")
plt.title("Radial Temperature")
current_values = plt.gca().get_xticks()
plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in current_values])
plt.savefig("Temperature.png")
plt.clf()

plt.figure(figsize=(8,5))
plt.scatter(r,z, s=10)
plt.errorbar(r,z,xerr=rerr,yerr=zerr,color='k',ls = "None",alpha=0.7)
plt.xscale("log")
plt.xlabel("Radius (kpc)")
plt.ylabel("Z/Zsun")
plt.title("Radial Metallicity")
current_values = plt.gca().get_xticks()
plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in current_values])
plt.savefig("Metallicity.png")

plt.figure(figsize=(8,5))
plt.scatter(r,cool, s=10)
plt.errorbar(r,cool,xerr=rerr,yerr=tcoolerr,color='k',ls = "None",alpha=0.7)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Radius (kpc)")
plt.ylabel("tcool(yr)")
plt.title("Radial Cooling Time")
current_values = plt.gca().get_xticks()
plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in current_values])
plt.savefig("Tcool.png")

