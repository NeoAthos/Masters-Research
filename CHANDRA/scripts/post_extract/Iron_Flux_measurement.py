#!/usr/bin/env python
from fpdf import FPDF #fpdf2
import math


#format (keV before Iron K line, after Fe K line, flux before line, flux after, total flux of Fe-K region)
#A3667
#vals = [6.1,6.8,6.4725e-16,5.5585e-16,6.9167e-13]  #A3667 Region Values (ergs/cm^2/s)

#MS07
#vals = [5.3,5.9,3.7953e-16,2.7283e-16,3.0814e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals = [5.3,5.9,4.1124e-16,2.9909e-16,3.6242e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals = [5.3,5.9,4.4698e-08,2.8864e-08,3.4564e-05]  #MS07 Region Values (photon/cm^2/s)
#vals = [5.3,5.9,4.8433e-08,3.1642e-08,4.0697e-05]  #MS07 Region1 Values (photon/cm^2/s)


#A2142
#vals = [5.9,6.5,3.0588e-15,2.6751e-15,2.6473e-12]  #A2142 Region Values (ergs/cm^2/s)
#vals = [5.9,6.5,3.0588e-15,2.6751e-15,2.6473e-12]  #A2142 Region1 Values (ergs/cm^2/s)	#Should be the same but always test
#vals = [5.9,6.5,3.2361e-07,2.5689e-07,0.00026658]  #A2142 Region Values (photons/cm^2/s)
#vals = [5.9,6.5,3.2361e-07,2.5689e-07,0.00026658]  #A2142 Region1 Values (photons/cm^2/s)

#A2029
#vals = [6.0,6.6,4.27e-15,3.7347e-15,4.7681e-12]  #A2029 Region Values (ergs/cm^2/s)
#vals = [6.0,6.6,4.2784e-15,3.742e-15,4.7767e-12]  #A2029 Region1 Values (ergs/cm^2/s)	
#vals = [6.0,6.6,4.4422e-07,3.5321e-07,0.00047371]  #A2029 Region Values (photons/cm^2/s)
#vals = [6.0,6.6,4.451e-07,3.539e-07,0.00047456]  #A2029 Region1 Values (photons/cm^2/s)

#A426
#vals = [6.3,6.8,9.5048e-15,7.9885e-15,1.2777e-11]  #A426 Region Values (ergs/cm^2/s)
#vals = [6.3,6.8,9.7747e-15,8.2476e-15,1.3284e-11]  #A426 Region1 Values (ergs/cm^2/s)	
#vals = [6.3,6.8,9.4172e-07,7.3329e-07,0.0012176]  #A426 Region Values (photons/cm^2/s)
#vals = [6.3,6.8,9.6846e-07,7.5707e-07,0.0012658]  #A426 Region1 Values (photons/cm^2/s)

#A478
#vals = [5.9,6.5,4.2834e-15,3.6637e-15,4.4073e-12]  #A478 Region Values (ergs/cm^2/s)
#vals = [5.9,6.5,4.2941e-15,3.674e-15,4.4133e-12]  #A478 Region1 Values (ergs/cm^2/s)	
#vals = [5.9,6.5,4.5317e-07,3.5183e-07,0.00044488]  #A478 Region Values (photons/cm^2/s)
#vals = [5.9,6.5,4.543e-07,3.5281e-07,0.00044547]  #A478 Region1 Values (photons/cm^2/s)

#A2319
#vals = [6.1,6.9,2.5877e-15,1.8225e-15,2.0804e-12]  #A2319 Region Values (ergs/cm^2/s)
#vals = [6.1,6.9,2.5899e-15,1.824e-15,2.0812e-12]  #A2319 Region1 Values (ergs/cm^2/s)	
#vals = [6.1,6.9,2.648e-07,1.6729e-07,0.00020189]  #A2319 Region Values (photons/cm^2/s)
#vals = [6.1,6.9,2.6501e-07,1.6743e-07,0.00020197]  #A2319 Region1 Values (photons/cm^2/s)

#A3571
#vals = [6.2,6.9,2.6762e-15,1.8824e-15,2.5084e-12]  #A3571 Region Values (ergs/cm^2/s)
#vals = [6.2,6.9,2.7028e-15,1.8989e-15,2.5264e-12]  #A3571 Region1 Values (ergs/cm^2/s)	
#vals = [6.2,6.9,2.6943e-07,1.7028e-07,0.00023971]  #A3571 Region Values (photons/cm^2/s)
#vals = [6.2,6.9,2.7211e-07,1.7178e-07,0.00024145]  #A3571 Region1 Values (photons/cm^2/s)

#AWM7
#vals = [6.3,7.0,6.3617e-16,4.882e-16,1.2463e-12]  #AWM7 Region Values (ergs/cm^2/s)
#vals = [6.3,7.0,6.4482e-16,4.9498e-16,1.26e-12]  #AWM7 Region1 Values (ergs/cm^2/s)	
#vals = [6.3,7.0,6.3031e-08,4.3533e-08,0.00011805]  #AWM7 Region Values (photons/cm^2/s)
#vals = [6.3,7.0,6.3888e-08,4.4138e-08,0.00011935]  #AWM7 Region1 Values (photons/cm^2/s)

#Centaurus 
#vals = [6.3,6.9,3.8273e-16,2.7826e-16,6.6063e-13]  #Centaurus Region1 Values (ergs/cm^2/s)	
#vals = [6.3,6.9,3.8563e-16,2.8039e-16,6.6583e-13]  #Centaurus Region Values (ergs/cm^2/s)
#vals = [6.3,6.9,3.792e-08,2.5172e-08,6.2655e-05]  #Centaurus Region1 Values (photons/cm^2/s)
#vals = [6.3,6.9,3.8208e-08,2.5365e-08,6.3148e-05]  #Centaurus Region Values (photons/cm^2/s)

#Coma 
#vals = [6.3,7.0,1.0717e-15,7.5358e-16,7.8115e-13]  #Coma Region Values (ergs/cm^2/s)
#vals = [6.3,7.0,1.0717e-15,7.5358e-16,7.8115e-13]  #Coma Region1 Values (ergs/cm^2/s)	
#vals = [6.3,7.0,1.0618e-07,6.7196e-08,7.3473e-05]  #Coma Region Values (photons/cm^2/s)
#vals = [6.3,7.0,1.0618e-07,6.7196e-08,7.3473e-05]  #Coma Region1 Values (photons/cm^2/s)

#Ophiuchus
#vals = [6.2,6.9,5.9912e-15,5.1686e-15,6.7641e-12]  #Ophiuchus Region Values (ergs/cm^2/s)
#vals = [6.2,6.9,5.9922e-15,5.1691e-15,6.7677e-12]  #Ophiuchus Region1 Values (ergs/cm^2/s)	
#vals = [6.2,6.9,6.0318e-07,4.6756e-07,0.00064429]  #Ophiuchus Region Values (photons/cm^2/s)
#vals = [6.2,6.9,6.0327e-07,4.6761e-07,0.00064464]  #Ophiuchus Region1 Values (photons/cm^2/s)

#A754
#vals = [6.1,6.7,7.752e-16,6.77e-16,7.1397e-13]  #A754 Region Values (ergs/cm^2/s)	
#vals = [6.1,6.7,7.7514e-16,6.7696e-16,7.1387e-13]  #A754 Region1 Values (ergs/cm^2/s)
#vals = [6.1,6.7,7.9324e-08,6.3071e-08,6.9607e-05]  #A754 Region Values (photons/cm^2/s)
#vals = [6.1,6.7,7.9318e-08,6.3067e-08,6.9598e-05]  #A754 Region1 Values (photons/cm^2/s)

#A2199
#vals = [6.2,6.8,1.6306e-15,1.3078e-15,2.2821e-12]  #A2199 Region Values (ergs/cm^2/s)	
#vals = [6.2,6.8,1.6306e-15,1.3078e-15,2.2821e-12]  #A2199 Region1 Values (ergs/cm^2/s)
#vals = [6.2,6.8,1.6416e-07,1.2005e-07,0.00021952]  #A2199 Region Values (photons/cm^2/s)
#vals = [6.2,6.8,1.6416e-07,1.2005e-07,0.00021952]  #A2199 Region1 Values (photons/cm^2/s)

#A3667
#vals = [6.1,6.8,6.4725e-16,5.5585e-16,6.9167e-13]  #A3667 Region Values (ergs/cm^2/s)	
#vals = [6.1,6.8,6.504e-16,5.5857e-16,6.9504e-13]  #A3667 Region1 Values (ergs/cm^2/s)
#vals = [6.1,6.8,6.6231e-08,5.1023e-08,6.7193e-05]  #A3667 Region Values (photons/cm^2/s)
#vals = [6.1,6.8,6.6553e-08,5.1272e-08,6.752e-05]  #A3667 Region1 Values (photons/cm^2/s)

#CygnusA
#vals1 = [6.1,6.8,3.2173e-15,2.2651e-15,3.9651e-12]  #CygnusA Region Values (ergs/cm^2/s)	
#vals2 = [6.1,6.8,3.8047e-15,3.2279e-15,5.6042e-12]  #CygnusA Region1 Values (ergs/cm^2/s)
#vals3 = [6.1,6.8,3.2921e-07,2.0792e-07,0.00038679]  #CygnusA Region Values (photons/cm^2/s)
#vals4 = [6.1,6.8,3.8933e-07,2.963e-07,0.00054521]  #CygnusA Region1 Values (photons/cm^2/s)

#CygnusA Mg K line (possibly Iron L)
#vals1 = [1.0,1.3,5.6104e-15,8.2668e-15,2.1679e-12]  #CygnusA Region Values (ergs/cm^2/s)	
#vals2 = [1.0,1.3,5.9935e-15,8.8641e-15,2.3248e-12]  #CygnusA Region1 Values (ergs/cm^2/s)
#vals3 = [1.0,1.3,3.5034e-06,3.9705e-06,0.001183]  #CygnusA Region Values (photons/cm^2/s)
#vals4 = [1.0,1.3,3.7427e-06,4.2574e-06,0.0012682]  #CygnusA Region1 Values (photons/cm^2/s)

#CygnusA Si K line (possibly Mg K)
#vals1 = [1.25,1.65,6.7995e-15,7.757e-15,3.0248e-12]  #CygnusA Region Values (ergs/cm^2/s)	
#vals2 = [1.25,1.65,7.3595e-15,8.3689e-15,3.2448e-12]  #CygnusA Region1 Values (ergs/cm^2/s)
#vals3 = [1.25,1.65,3.3965e-06,2.9351e-06,0.0013063]  #CygnusA Region Values (photons/cm^2/s)
#vals4 = [1.25,1.65,3.6762e-06,3.1667e-06,0.0014014]  #CygnusA Region1 Values (photons/cm^2/s)

#CygnusA S K line (possibly Si K)
#vals1 = [2.3,2.6,3.2173e-15,2.2651e-15,3.9651e-12]  #CygnusA Region Values (ergs/cm^2/s)	
#vals2 = [2.3,2.6,7.7784e-15,7.0122e-15,2.2945e-12]  #CygnusA Region1 Values (ergs/cm^2/s)
#vals3 = [2.3,2.6,1.941e-06,1.5061e-06 ,0.00052389]  #CygnusA Region Values (photons/cm^2/s)
#vals4 = [2.3,2.6,2.1113e-06,1.6836e-06,0.00058543]  #CygnusA Region1 Values (photons/cm^2/s)

#CygnusA Ca K line (possibly S K)
#vals1 = [3.6,4.0,3.2173e-15,2.2651e-15,3.9651e-12]  #CygnusA Region Values (ergs/cm^2/s)	
#vals2 = [3.6,4.0,5.8239e-15,5.3346e-15,2.2873e-12]  #CygnusA Region1 Values (ergs/cm^2/s)
#vals3 = [3.6,4.0,8.5841e-07,7.0875e-07,0.00032256]  #CygnusA Region Values (photons/cm^2/s)
#vals4 = [3.6,4.0,1.0099e-06,8.3249e-07,0.00037626]  #CygnusA Region1 Values (photons/cm^2/s)

#HydraA Iron K
#vals1 = [6.1,6.6,1.2596e-15,1.128e-15,1.4223e-12]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [6.1,6.6,1.2892e-15,1.1535e-15,1.4783e-12]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [6.1,6.6,1.289e-07,1.0668e-07,0.00013994]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [6.1,6.6,1.3192e-07,1.0909e-07,0.00014545]  #HydraA Region1 Values (photons/cm^2/s)

#HydraA Mg K line (possibly Iron L)
#vals1 = [0.85,1.3,9.7131e-15,7.823e-15,4.5656e-12]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [0.85,1.3,9.6792e-15,8.0616e-15,4.6565e-12]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [0.85,1.3,7.1364e-06,3.7573e-06,0.0027094]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [0.85,1.3,7.1115e-06,3.872e-06,0.0027582]  #HydraA Region1 Values (photons/cm^2/s)

#HydraA Si K line (possibly Mg K)
#vals1 = [1.3,1.55,7.8938e-15,7.1647e-15,2.019e-12]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [1.3,1.55,8.0616e-15,7.3289e-15,2.0694e-12]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [1.3,1.55,3.7914e-06,2.886e-06,0.0008882]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [1.3,1.55,3.872e-06,2.9521e-06,0.00091035]  #HydraA Region1 Values (photons/cm^2/s)

#HydraA S K line (possibly Si K)
#vals1 = [2.15,2.6,5.4817e-15,4.5368e-15,2.3859e-12]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [2.15,2.6,5.6154e-15,4.6508e-15,2.4498e-12]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [2.15,2.6,1.5917e-06,1.0893e-06,0.00062977]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [2.15,2.6,1.6305e-06,1.1167e-06,0.00064659]  #HydraA Region1 Values (photons/cm^2/s)

#HydraA Ca K line (possibly S K)
#vals1 = [3.5,3.8,3.24e-15,2.875e-15,9.5116e-13]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [3.5,3.8,3.3323e-15,2.956e-15,9.7911e-13]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [3.5,3.8,5.7786e-07,4.7227e-07,0.0001628]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [3.5,3.8,5.9433e-07,4.8558e-07,0.00016758]  #HydraA Region1 Values (photons/cm^2/s)

#HerculesA Iron K
#vals1 = [5.5,6.0,2.782e-16,4.0186e-16,2.7748e-13]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [5.5,6.0,2.7813e-16,3.9542e-16,2.8499e-13]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [5.5,6.0,3.1574e-08,4.1807e-08,3.0039e-05]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [5.5,6.0,3.1566e-08,4.1136e-08,3.0852e-05]  #HydraA Region1 Values (photons/cm^2/s)

#HerculesA Iron L
#vals1 = [0.85,1.1,1.4706e-15,1.3552e-15,4.109e-13]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [0.85,1.1,1.5529e-15,1.4211e-15,4.3929e-13]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [0.85,1.1,1.0805e-06,7.6928e-07,0.00026486]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [0.85,1.1,1.1409e-06,8.067e-07,0.00028321]  #HydraA Region1 Values (photons/cm^2/s)

#HerculesA Mg K
#vals1 = [1.2,1.4,1.3096e-15, 1.2382e-15,2.6897e-13]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [1.2,1.4,1.3776e-15,1.2927e-15,2.8354e-13]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [1.2,1.4,6.8145e-07,5.5223e-07,0.00012948]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [1.2,1.4,7.1681e-07,5.7652e-07,0.00013651]  #HydraA Region1 Values (photons/cm^2/s)

#HerculesA Si K
#vals1 = [2.17,2.4,8.9908e-16,8.305e-16,2.1121e-13]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [2.17,2.4,9.3322e-16,8.5693e-16,2.2006e-13]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [2.17,2.4,2.5866e-07,2.1602e-07,5.7803e-05]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [2.17,2.4,2.6848e-07,2.229e-07,6.0229e-05]  #HydraA Region1 Values (photons/cm^2/s)

#HerculesA Ar K
#vals1 = [3.3,3.46,5.9693e-16,5.5944e-16,9.6654e-14]  #HydraA Region Values (ergs/cm^2/s)	
#vals2 = [3.3,3.46,6.0991e-16,5.7114e-16,9.9142e-14]  #HydraA Region1 Values (ergs/cm^2/s)
#vals3 = [3.3,3.46,1.1292e-07,1.0093e-07,1.7856e-05]  #HydraA Region Values (photons/cm^2/s)
#vals4 = [3.3,3.46,1.1537e-07,1.0304e-07,1.8316e-05]  #HydraA Region1 Values (photons/cm^2/s)

#MS07 Iron K
#vals1 = [5.3,5.9,3.7953e-16,2.7283e-16,3.0814e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [5.3,5.9,4.1124e-16,2.9909e-16,3.6242e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [5.3,5.9,4.4698e-08,2.8864e-08,3.4564e-05]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [5.3,5.9,4.8433e-08,3.1642e-08,4.0697e-05]  #MS07 Region1 Values (photon/cm^2/s)

#MS07 Iron L
#vals1 = [0.85,1.05,1.3499e-15,1.3035e-15,2.807e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [0.85,1.05,1.6381e-15,1.5755e-15,3.4814e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [0.85,1.05,9.9179e-07,7.7522e-07,0.0001855]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [0.85,1.05,1.2036e-06,9.3697e-07,0.00023019]  #MS07 Region1 Values (photon/cm^2/s)

#MS07 Mg K
#vals1 = [1.1,1.3,1.2417e-15,1.1561e-15,2.4486e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [1.1,1.3,1.4901e-15,1.3846e-15,2.9612e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [1.1,1.3,7.0489e-07,5.5528e-07,0.00012769]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [1.1,1.3,8.459e-07,6.6501e-07,0.00015439]  #MS07 Region1 Values (photon/cm^2/s)

#MS07 Si K
#vals1 = [2.25,2.6,8.1687e-16,7.2535e-16,2.7274e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [2.25,2.6,9.622e-16,8.4846e-16,3.1906e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [2.25,2.6,2.2665e-07,1.7416e-07,7.04e-05]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [2.25,2.6,2.6697e-07,2.0372e-07,8.2364e-05]  #MS07 Region1 Values (photon/cm^2/s)

#MS07 Ar K
#vals1 = [3.2,3.5,6.1799e-16,5.5172e-16,1.7639e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [3.2,3.5,7.2307e-16,6.2556e-16,2.0333e-13]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [3.2,3.5,1.2055e-07,9.84e-08,3.2912e-05]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [3.2,3.5,1.4105e-07,1.1157e-07,3.7946e-05]  #MS07 Region1 Values (photon/cm^2/s)

#M87 Iron K
#vals1 = [6.3,7.0,4.0748e-14,1.656e-14,1.2419e-11]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [6.3,7.0,7.1153e-16,4.7707e-16,1.3891e-12]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [6.3,7.0,4.4698e-08,2.8864e-08,3.4564e-05]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [6.3,7.0,7.0497e-08,4.2541e-08,0.00013082]  #MS07 Region1 Values (photon/cm^2/s)

#M87 Iron L
#vals1 = [1.0,1.25,4.0748e-14,1.656e-14,2.807e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [1.0,1.25,4.0748e-14,1.656e-14,1.2419e-11]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [1.0,1.25,9.9179e-07,7.7522e-07,0.0001855]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [1.0,1.25,2.5446e-05,8.2718e-06,0.0070686]  #MS07 Region1 Values (photon/cm^2/s)

#M87 Mg K
#vals1 = [1.3,1.6,1.2417e-15,1.1561e-15,2.4486e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [1.3,1.6,2.2478e-14,1.5042e-14,6.219e-12]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [1.3,1.6,7.0489e-07,5.5528e-07,0.00012769]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [1.3,1.6,1.0796e-05,5.8696e-06,0.0026901]  #MS07 Region1 Values (photon/cm^2/s)

#M87 Si K
#vals1 = [2.3,2.7,8.1687e-16,7.2535e-16,2.7274e-13]  #MS07 Region Values (ergs/cm^2/s)
#vals2 = [2.3,2.7,7.9307e-15,6.2004e-15,4.0814e-12]  #MS07 Region1 Values (ergs/cm^2/s)
#vals3 = [2.3,2.7,2.2665e-07,1.7416e-07,7.04e-05]  #MS07 Region Values (photon/cm^2/s)
#vals4 = [2.3,2.7,2.1526e-06,1.4336e-06,0.001023]  #MS07 Region1 Values (photon/cm^2/s)

#M87 Ar K
vals1 = [3.7,4.1,6.1799e-16,5.5172e-16,1.7639e-13]  #MS07 Region Values (ergs/cm^2/s)
vals2 = [3.7,4.1,3.3715e-15,2.6516e-15,1.3787e-12]  #MS07 Region1 Values (ergs/cm^2/s)
vals3 = [3.7,4.1,1.2055e-07,9.84e-08,3.2912e-05]  #MS07 Region Values (photon/cm^2/s)
vals4 = [3.7,4.1,5.6881e-07,4.0371e-07,0.00022129]  #MS07 Region1 Values (photon/cm^2/s)


def calc_counts(vals):
	slope = (vals[2]-vals[3])/(vals[0]-vals[1])
	b = vals[2] - slope*vals[0]
	#steps = (6.8-6.1)/0.01
	i = vals[0]
	total = 0
	print("Ping")
	while i <= vals[1]:
		total+=(slope*i+b)
		i+=0.001
	final = (vals[4] - total)*299
	return final

#Converting KeV to wavelength to find proper positioning
KeV = 5.5
Ev = KeV*1000
wav = 1.24E3/Ev
#Finding important lines mathematically 
z = 0.00428
Evs = [1253.6, 1740, 2306, 3690, 6395]
i = 0 
while i <= len(Evs)-1:
	Ev = Evs[i]
	wav = 1.24E3/Ev
	del_lam = z*wav
	obs_lam = del_lam + wav
	#print(obs_lam)
	print(1.24E3/obs_lam/1000)	
	i+=1

	
final1 = calc_counts(vals1)
final2 = calc_counts(vals2)
final3 = calc_counts(vals3)
final4 = calc_counts(vals4)

print(final1, "ergs/s without point sources")
print(final2, "ergs/s with point sources")
print(final3, "photons/s without point sources")
print(final4, "photons/s with point sources")

print(final1*3600, "ergs/h without point sources")
print(final2*3600, "ergs/h with point sources")
print(final3*3600, "photons/h without point sources")
print(final4*3600, "photons/h with point sources")

#diff = avg*steps


 
#print(total)


#dist = math.hypot(x2 - x1, y2 - y1)
#print(dist)

