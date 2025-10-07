#!/usr/bin/env python
from sgp4.api import accelerated
from sgp4.api import Satrec
import numpy as np
import astropy
#import pkg_resources
#pkg_resources.require("astropy==6.0")
from astropy.time import Time
from sgp4.api import jday
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy import units as u
from astropy.coordinates import ITRS, SkyCoord, EarthLocation


s='1 57800U 23137A   24221.54588967  .00010068  00000+0  74615-3 0  9999'
t='2 57800  31.0036  39.1663 0009965   7.6480 352.4307 15.01847293 50488'
satellite = Satrec.twoline2rv(s, t)
#jd, fr = jday(2024, 1, 9, 20, 42, 0)
time=Time('2024-06-02T20:01:04', format='isot', scale='utc')
#t = Time(time.jd, format='jd')
#time = Time(2458827.362605, format='jd')
error_code, teme_p, teme_v = satellite.sgp4(time.jd1, time.jd2)  # in km and km/s
if error_code != 0:
    raise RuntimeError(SGP4_ERRORS[error_code])
print(error_code,teme_p,teme_v)


teme_p = CartesianRepresentation(teme_p*u.km)
teme_v = CartesianDifferential(teme_v*u.km/u.s)
teme = TEME(teme_p.with_differentials(teme_v), obstime=time)
    
print(teme_p,teme_v)
teme.default_representation

    
itrs_geo = teme.transform_to(ITRS(obstime=time))
location = itrs_geo.earth_location
print(location.geodetic)

position = EarthLocation.from_geodetic(lat=location.lat, lon=location.lon, height=location.height)
sc = SkyCoord(ra=187.664867339318*u.deg, dec=12.3557507134426*u.deg)
heliocorr = sc.radial_velocity_correction('heliocentric', obstime=Time('2024-06-02T20:01:04', format='isot', scale='utc'), location=position)
print(heliocorr.to(u.km/u.s))

