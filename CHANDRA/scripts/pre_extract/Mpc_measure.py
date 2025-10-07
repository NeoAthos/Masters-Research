#!/usr/bin/env python

import math
import os
import sys
import glob
import subprocess
from astropy.cosmology import FlatLambdaCDM as LCDM
from astropy import constants as const
import astropy.units as u
import numpy as np

cosmo = LCDM(70, 0.3)

d_A = 16.7			#cosmo.angular_diameter_distance(z=0.004283)
print(d_A)
theta = 58 #arcsec

theta_radian = theta * np.pi/180/3600
distance_Mpc = d_A * theta_radian
distance_kpc = distance_Mpc * 1000
print(distance_kpc)

#M87 bullshit
r_error = 8/149
m_error = 3E10/3.9116E11
print(r_error)
timescale = 232403207*3.154E7 #232403207 237573207 616323783 100736025  (616323783+100736025)/2
print(timescale, "s")
timescale = ((237572548+100000000+155268298+199233855+222399516+366179679+487414063+524499749+634669651)/9)*3.154E7
#timescale = 3.4584564E14
print(timescale, "s")
sigma = 149 * 100000 #cm/s
sigma_error = r_error*sigma
#M = 4.8E10*1.989E33
M = 1.36E10*1.989E33
M_error = M*m_error
print(M)
Tot_percent_error = 2*r_error+m_error
print(Tot_percent_error*100)

E_turb = (3/2)*(M)*(sigma)**2
E_error = E_turb*Tot_percent_error
P_turb = E_turb/timescale
P_error = P_turb*Tot_percent_error
print(E_turb)
print(E_error)
print(P_turb)
print(P_error)

#average 2.2905357255775444e+43 4.216361104572499e+42
#half 3.456726304157216e+43 6.363055670885108e+42
#full 1.3324579976494066e+43 2.4527554894822417e+42

