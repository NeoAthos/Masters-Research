from xspec import *
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import FuncFormatter
import lineid_plot
import numpy as np
import re
from scipy import integrate

rc('text', usetex=True)

z = 0.063001



# PyXspec operations loading data
# -------------------------------

specfile = 'image_nh0p041_v500_exp500_Z0p5_cenPix.pi'
exptime = int(re.search(r"exp(\d+)_", specfile).group(1))*1000 # seconds
vel = int(re.search(r"v(\d+)_", specfile).group(1)) # km/s

s = Spectrum(specfile)
s.response = '~/soft/heasoft-6.31.1/xrism/heasimfiles/xrism/resolve/response/resolve_h5ev_2019a.rmf'
s.response.arf = '~/soft/heasoft-6.31.1/xrism/heasimfiles/xrism/resolve/response/resolve_bet_spec_noGV_20190611.arf'
s.ignore("**-0.3 10.-**")
s.ignore("bad")


# Set XSPEC commands
# -------------------

Xset.abund = "angr"
Xset.cosmo = "70 .0 0.7"
Xset.xsect = "bcmc"

# Fit a model
# --------------------------------------
nH = 0.041   # /cm^2
kT = 4       # keV
Z = 0.5      # solar metallicity
norm = 0.3   # normalization

m1 = Model("phabs*bapec", setPars={1:nH, 2:kT, 3:Z, 4:z, 5:vel, 6:norm})
# m1 = Model("bapec", setPars={1:kT, 2:Z, 3:z, 4:vel, 5:norm})
# m1 = Model("phabs*(bapec+mkcflow)", setPars={1:kT, 2:Z, 3:z, 4:vel, 5:norm})

Fit.renorm('auto')
Fit.perform()
# Fit.nIterations = 1000
# Fit.statMethod = "cstat"

Plot.device = '/null'
Plot('model')
# modVals = Plot.model()
modVals = np.array(m1.folded(1))
modVals = modVals*exptime**0.5     




# Plot data in xspec and get x and y point values and errors
# ----------------------------------------------------------

Plot.xAxis = 'keV'
Plot("data")
xVals = np.array(Plot.x())
yVals = np.array(Plot.y())
xErrs = np.array(Plot.xErr())
yErrs = np.array(Plot.yErr())


# stack the arrays horizontally
data = np.hstack((xVals.reshape(-1,1),
				  xErrs.reshape(-1,1),
				  yVals.reshape(-1,1),
				  yErrs.reshape(-1,1)))

# save the arrays to a csv file
np.savetxt(specfile[:-3]+'.csv', data, delimiter=',')


# # Calculate counts in various lines
# # ---------------------------------

# AllModels.calcFlux("0.608 0.622")
# print("\nCounts OVIII:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("0.952 0.971")
# print("\nCounts Ne X:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("0.987 1.001")
# print("\nCounts Fe XXII + Fe XXIII:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.012 1.029")
# print("\nCounts Fe XXIV:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.029 1.0518")
# print("\nCounts Some Fe:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.0518 1.070")
# print("\nCounts Fe XXIII + Fe XXIV:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.087 1.111")
# print("\nCounts Fe XXIV:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.377 1.395")
# print("\nCounts Mg XII:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.3972 1.413")
# print("\nCounts Fe XXIII + Fe XXIV:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("1.876 1.900")
# print("\nCounts Si XIV:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("2.457 2.479")
# print("\nCounts S XVI:", s.flux[3]*exptime, "\n")

# AllModels.calcFlux("6.214 6.328")
# print("\nCounts Fe K:", s.flux[3]*exptime, "\n")



# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# print("             using numerical integration              ")
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# def NumInt(xmin, xmax, xarr, yarr):
# 	# Integrate the spectrum numerically
# 	valid = (xarr >= xmin)&(xarr <= xmax)
# 	return integrate.simpson(yarr[valid], xarr[valid])

# print("\nCounts OVIII:", NumInt(0.608, 0.622, xVals, yVals)*exptime, "\n")

# print("\nCounts Ne X:", NumInt(0.952, 0.971, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe XXII + Fe XXIII:", NumInt(0.987, 1.001, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe XXIV:", NumInt(1.012, 1.029, xVals, yVals)*exptime, "\n")

# print("\nCounts Some Fe:", NumInt(1.029, 1.0518, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe XXIII + Fe XXIV:", NumInt(1.0518, 1.070, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe XXIV:", NumInt(1.087, 1.111, xVals, yVals)*exptime, "\n")

# print("\nCounts Mg XII:", NumInt(1.377, 1.395, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe XXIII + Fe XXIV:", NumInt(1.3972, 1.413, xVals, yVals)*exptime, "\n")

# print("\nCounts Si XIV:", NumInt(1.876, 1.900, xVals, yVals)*exptime, "\n")

# print("\nCounts S XVI:", NumInt(2.457, 2.479, xVals, yVals)*exptime, "\n")

# print("\nCounts Fe K:", NumInt(6.214, 6.328, xVals, yVals)*exptime, "\n")





# Plot data
# ---------

line_keV = np.array([0.367, 0.5, 0.561, 0.654, 0.773, 0.919, 0.965, 1.010,
					 1.021, 1.055, 1.083 , 1.121, 1.127, 1.166, 1.240  ,
					 1.313, 1.350, 1.383, 1.407 , 1.473 , 1.493  ,
					 1.659, 1.840, 1.865, 2.006, 2.461, 2.622, 6.676])/(1+z) # keV
line_flux = np.interp(line_keV, xVals, yVals)
arrow_tips = [30]*len(line_flux)
line_label = ['C VI', 'N VII', 'O VII', 'O VIII', 'O VIII + Fe XIX',
			  'Fe XIX', 'Fe XX', 'Fe XXI', 'Ne X', 'Fe XXII + Fe XXIII',
			  'Fe XXIV', 'Fe XXIV', 'Fe XXIII + Fe XXIV', 'Fe XXIV',
			  'Fe XX', 'Fe XXI', 'Mg XI', 'Fe XXII', 'Fe XXIII',
			  'Mg XII', 'Fe XXIII + Fe XXIV', 'Fe XXIV', 'Si XIII',
			  'Si XIII', 'Si XIV', 'S XV', 'S XVI', 'Fe K']
box_loc = [100]*len(line_label)

fig, ax = plt.subplots(1,1, figsize=(16,10))
lineid_plot.plot_line_ids(xVals, yVals, line_keV, line_label, ls='', ax=ax,
	box_loc=box_loc, arrow_tip=arrow_tips)
ax.errorbar(xVals, yVals, xerr=xErrs, yerr=yErrs, ls='', marker="+", c='k')
ax.plot(xVals, modVals, ls='-', c='r')
ax.set_xlabel('Energy (keV)')
ax.set_ylabel(r'counts s$^{-1}$ keV$^{-1}$')
ax.loglog()


def scientific(x, pos):
    # x:  tick value - ie. what you currently see in xticks
    # pos: a position - ie. the index of the tick
    return str(float(x))


scientific_formatter = FuncFormatter(scientific)
ax.xaxis.set_major_formatter(scientific_formatter)
ax.yaxis.set_major_formatter(scientific_formatter)

plt.title(specfile[:-3], y=1.3, pad=14)
plt.savefig(specfile[:-2]+'png')
plt.show()
plt.close()