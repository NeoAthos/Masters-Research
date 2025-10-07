#!/usr/bin/env python

import math
import os
import sys
import glob
import subprocess
from ciao_contrib.runtool import dmstat
from astropy.cosmology import FlatLambdaCDM as LCDM
import astropy.units as u
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy
from astropy.io import fits


import matplotlib.pyplot as plt
import matplotlib.cm as cm
from astropy.io import fits
import pyregion

grplist = ["XRISM_region1_3200_grp100.pi","XRISM_region1_16142_grp100.pi","XRISM_region1_16143_grp100.pi","XRISM_region1_16464_grp100.pi","XRISM_region1_16626_grp100.pi","XRISM_region1_16627_grp100.pi","XRISM_region1_16633_grp100.pi","XRISM_region1_16634_grp100.pi","XRISM_region1_16635_grp100.pi","XRISM_region1_16645_grp100.pi"]

combine_name = 'XRISM_region1_sum'
print("combine_spectra src_spectra=%s outroot=%s " % (grplist,combine_name))
os.system("combine_spectra src_spectra=%s outroot=%s " % (grplist,combine_name))



