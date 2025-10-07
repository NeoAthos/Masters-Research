#! /bin/sh

# THIS SCRIPT RUNS THE SKY BACKGROUND TOOL.

############# ASSIGNMENT BLOCK ##############
# Create a definition block here, so we can preserve the useful comments for each parameter

outfileroot="cxb_sxi" # Output file name base
exposure=10000     # exposure time in sec
ra=151.8606        # central RA in decimal degrees
dec=16.1085        # central Dec in decimal degrees
radius=50.0        # radius of FOV in arcmin
emin=0.1           # energy grid minimum in keV
emax=16.0          # energy grid maximum in keV
de=0.005           # energy grid spacing in keV
flaglogns=yes      # include emission from logN-logS ?
flaggal=yes        # include soft Xray Galactic and LHB emission ?
flagswcx=no        # include SWCX emission ?
slopebright1=1.7   # logN-logS slope 1, bright end
slopefaint1=0.9    # logN-logS slope 1, faint end
fluxbreak=2.5e-14  # logN-logS flux at power-law break
norm1=8.0e3        # logN-logS normalization in sources/sq.degree for slope 1
fluxsens=1.0e-14   # logN-logS flux sensitivity limit
fluxmin=1.0e-16    # lower flux limit of logN
fluxmax=5.0e-13    # upper flux limit of logNS in erg/cm^2/sec, both components
bandpasslo=0.5 # lower limit in keV for bandpass over which logN-logS is defined
bandpasshi=2.0 # upper limit in keV for bandpass over which logN-logS is defined
spectype1=1    # spectral type for slope-1 source: 0=single_spectrum, 1=multi, 2=torus
fabs0=0.22     # fraction of slope-1 sources, NH < 1e21 cm^-2
fabs1=0.22     # fraction of slope-1 sources, NH=1e21 - 1e22 cm^-2
fabs2=0.22     # fraction of slope-1 sources, NH=1e22 - 1e23 cm^-2
fabs3=0.22     # fraction of slope-1 sources, NH=1e23 - 1e24 cm^-2
fabs4=0.06     # fraction of slope-1 sources, NH=1e24 - 1e25 cm^-2
fabs5=0.06     # fraction of slope-1 sources, NH > 1e25 cm^-2
fpar0=0.2      # fraction index=1.5-1.7 if spectype1=1, opening angle < 30 if spectype1=2
fpar1=0.2      # fraction index=1.7-1.9 if spectype1=1, opening angle 30-45 if spectype1=2
fpar2=0.2      # fraction index=1.9-2.1 if spectype1=1, opening angle 45-60 if spectype1=2
fpar3=0.2      # fraction index=2.1-2.3 if spectype1=1, opening angle 60-75 if spectype1=2
fpar4=0.2      # fraction index=2.3-2.5 if spectype1=1, opening angle 75-90 if spectype1=2
seed=1234567890

######### EXECUTION BLOCK ###################

punlearn skyback

skyback \
    outfileroot=$outfileroot \
    ra=$ra \
    dec=$dec \
    radius=$radius \
    emin=$emin \
    emax=$emax \
    de=$de \
    flaglogns=$flaglogns \
    flaggal=$flaggal \
    flagswcx=$flagswcx \
    slopebright1=$slopebright1 \
    slopefaint1=$slopefaint1 \
    fluxbreak=$fluxbreak \
    norm1=$norm1 \
    fluxsens=$fluxsens \
    fluxmin=$fluxmin \
    fluxmax=$fluxmax \
    bandpasslo=$bandpasslo \
    bandpasshi=$bandpasshi \
    spectype1=$spectype1 \
    fabs0=$fabs0 \
    fabs1=$fabs1 \
    fabs2=$fabs2 \
    fabs3=$fabs3 \
    fabs4=$fabs4 \
    fabs5=$fabs5 \
    fpar0=$fpar0 \
    fpar1=$fpar1 \
    fpar2=$fpar2 \
    fpar3=$fpar3 \
    fpar4=$fpar4 \
    seed=$seed

############# ASSIGNMENT BLOCK ##############
# Create a definition block here, so we can preserve the useful comments for each parameter

outfileroot="cxb_hxi" # Output file name base
exposure=10000     # exposure time in sec
ra=151.8606        # central RA in decimal degrees
dec=16.1085        # central Dec in decimal degrees
radius=20.0        # radius of FOV in arcmin
emin=0.1           # energy grid minimum in keV
emax=120.0         # energy grid maximum in keV
de=0.025           # energy grid spacing in keV
flaglogns=yes      # include emission from logN-logS ?
flaggal=yes        # include soft Xray Galactic and LHB emission ?
flagswcx=no        # include SWCX emission ?
slopebright1=1.7   # logN-logS slope 1, bright end
slopefaint1=0.9    # logN-logS slope 1, faint end
fluxbreak=3.5e-14  # logN-logS flux at power-law break
norm1=1.9e4        # logN-logS normalization in sources/sq.degree for slope 1
fluxsens=1.0e-14   # logN-logS flux sensitivity limit
fluxmin=1.0e-16    # lower flux limit of logN
fluxmax=7.0e-13    # upper flux limit of logNS in erg/cm^2/sec, both components
bandpasslo=2.0     # lower limit in keV for bandpass over which logN-logS is defined
bandpasshi=10.0    # upper limit in keV for bandpass over which logN-logS is defined
spectype1=2  # spectral type for slope-1 source: 0=single_spectrum, 1=multi, 2=torus
fabs0=0.2    # fraction of slope-1 sources, NH < 1e21 cm^-2
fabs1=0.2    # fraction of slope-1 sources, NH=1e21 - 1e22 cm^-2
fabs2=0.2    # fraction of slope-1 sources, NH=1e22 - 1e23 cm^-2
fabs3=0.2    # fraction of slope-1 sources, NH=1e23 - 1e24 cm^-2
fabs4=0.1    # fraction of slope-1 sources, NH=1e24 - 1e25 cm^-2
fabs5=0.1    # fraction of slope-1 sources, NH > 1e25 cm^-2
fpar0=0.2    # fraction index=1.5-1.7 if spectype1=1, opening angle < 30 if spectype1=2
fpar1=0.2    # fraction index=1.7-1.9 if spectype1=1, opening angle 30-45 if spectype1=2
fpar2=0.2    # fraction index=1.9-2.1 if spectype1=1, opening angle 45-60 if spectype1=2
fpar3=0.2    # fraction index=2.1-2.3 if spectype1=1, opening angle 60-75 if spectype1=2
fpar4=0.2    # fraction index=2.3-2.5 if spectype1=1, opening angle 75-90 if spectype1=2
seed=1234567890

######### EXECUTION BLOCK ###################

punlearn skyback

skyback \
    outfileroot=$outfileroot \
    ra=$ra \
    dec=$dec \
    radius=$radius \
    emin=$emin \
    emax=$emax \
    de=$de \
    flaglogns=$flaglogns \
    flaggal=$flaggal \
    flagswcx=$flagswcx \
    slopebright1=$slopebright1 \
    slopefaint1=$slopefaint1 \
    fluxbreak=$fluxbreak \
    norm1=$norm1 \
    fluxsens=$fluxsens \
    fluxmin=$fluxmin \
    fluxmax=$fluxmax \
    bandpasslo=$bandpasslo \
    bandpasshi=$bandpasshi \
    spectype1=$spectype1 \
    fabs0=$fabs0 \
    fabs1=$fabs1 \
    fabs2=$fabs2 \
    fabs3=$fabs3 \
    fabs4=$fabs4 \
    fabs5=$fabs5 \
    fpar0=$fpar0 \
    fpar1=$fpar1 \
    fpar2=$fpar2 \
    fpar3=$fpar3 \
    fpar4=$fpar4 \
    seed=$seed
