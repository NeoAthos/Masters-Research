from astropy.io import fits
import numpy as np
import astropy
import matplotlib.pyplot as plt
from astropy import wcs
from astropy.convolution import convolve, Gaussian2DKernel, Tophat2DKernel
from astropy.modeling.models import Gaussian2D



#image_file = astropy.io.fits.open('HydraA_GV_v300_100ks.fits', format='fits')
#image_list = ['HydraA_GV_v300_100ks.fits', 'HydraA_GV_v600_100ks.fits']
#print(image_list)
hdu = fits.open('HydraA_GV_v300_100ks_slice.fits')

gauss_kernel = Gaussian2DKernel(12)
hdu.verify('fix')
data = hdu[0].data
print(hdu.info())
#print(data[503,491])
#print(data[503,492])
#print(data[503,493])
#print(data[503,494])
print(data.max())
print(data[511,514])
print(data[511,515])
print(data[511,516])
smoothed_data_gauss = convolve(data, gauss_kernel)
outfile = 'HydraA_GV_v300_100ks_smoothed.fits'
hdu[0].data = smoothed_data_gauss
hdu.writeto(outfile, overwrite=True)
#test = fits.open('HydraA_GV_v300_100ks.fits')
#test2 = fits.open('HydraA_GV_v600_100ks.fits')
#head = test[1].header
#print(test.shape)
#head2 = test2[1].header
#total_exp_time = head['TSTOP'] + head2['TSTOP']
#head['TSTOP'] = total_exp_time
#total_exp_time = head['EXPOSURE'] + head2['EXPOSURE']
#head['EXPOSURE'] = total_exp_time
#head['TLMIN'] = head['TLMIN4']
#head['TLMAX'] = head['TLMAX4']+1
#print(head['TSTOP'])
#print(head)
#w = wcs.WCS(test[0].header)


#print(w)
#print(w.wcs.name)
#w.wcs.print_contents()
