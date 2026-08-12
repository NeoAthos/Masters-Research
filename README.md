# UWaterloo MSc Research
**Observations of X-Ray telescopes (CHANDRA and XRISM)**
## Introduction
This is the cumalitive work that was completed during my MSc at the University of Waterloo, this work required knowledge in the fields of astrophysics, data science and data analysis. The code primarily was done through Python (Juptyer and IDEs), yet it also extended to Tcl and Bash scripting. Several tools produced by HEASARC, SRON, and NASA were also utilized, with key tools being SPEX and Xspec. 
My research is subdivided into 3 projects:

## **CHANDRA Datasheets & Dashboards** 
CHANDRA is an older X-ray telescope (deployed 1999) with a high imaging resolution (0.5 arcsec) and a low spectral resolution (95 eV). I extracted the X-ray spectra radially to observe radial relationships with plasma temperature and metallicity between 16 commonly observed clusters. Below is an example of the perseus cluster with equally weighted spectral rings. Each ring has has a unique spectrum, upon using linear regression algorthims extracting key features per ring (metallicity, temperature & cooling time) to produce unique graphs per cluster. You can inspect the logic inside the [Annulus generation](./CHANDRA/new_scripts/pre_extract/annulus.py) and [Spectrum extraction](./CHANDRA/new_scripts/pre_extract/specextractmaster_sum.py) scripts.
<p align="center">
   <img width="720" height="650" alt="Screenshot from 2025-01-05 14-16-44" src="https://github.com/user-attachments/assets/ce7b33ab-b612-419e-a932-831d1813d948" />  
</p>
This data is then collected into a dashboard to be compared to with other clusters, allowing for a deeper scientific analysis between cluster types (cool core and non-cool core). By observing and comparing multiple clusters together there were two clusters that are unique and do not follow expected results, this could only be accomplished through observing these dashboards/datasheets!  
 
<p align="center">
   <img width="956" height="647" alt="Screenshot 2026-08-11 142054" src="https://github.com/user-attachments/assets/8acc5e86-4944-4554-920f-824026e8ff0c" />
</p>

These dashboards are created through the combination of [extracting properties](./CHANDRA/scripts/post_extract/multifit_apec.tcl) from the spectra, [plotting the properties](./CHANDRA/new_scripts/pre_extract/plot_proj.py) with the radius of the cluster and aligning them into a legible [dashboard](./CHANDRA/new_scripts/pre_extract/create_datasheet.py). You may notice in the dashboard that each contains an image of the cluster with a green square, this is the footprint of XRISM (an at the time upcoming telescope), and all of the data extracted in the chart next to the image is related to this footprint to simplify simulations. The folder containing all 16 dashboards can be found [here](./CHANDRA/Datasheets/).
   
## **Simulating XRISM** 
While working on this project XRISM was slated to launch near the end of my MSc, XRISM is a high spectral resolution (5eV) low spatial resolution (30 arcsec^2) X-Ray space telescope. This telescope is used to measure the abundances of metals in galaxy clusters at a higher precision due to its groundbreaking spectral resolution. The goal with XRISM data is to get the metallicity ratios and the turbelent gas speeds of different elements in galaxy clusters, this can only be achieved with an instrument with an extremely high spectral resolution. To attempt to obtain observation time with the new telescope one must contest other observation proposals from other research teams, as new telescope observation time is a competitive field. Therefore I had to attempt to simulate the effect of XRISM on previous CHANDRA data, essentially upscaling CHANDRA data. This was achieved through utilizing simulation software from xspec and heasoft, [simulating photon raytracing](./XRISM/heasimscripts/run_sim_xrism.sh) through a telescope with the anticipated spectral resolution of XRISM. 
<p align="center">
   <img width="970" height="488" alt="Screenshot 2026-08-12 143325" src="https://github.com/user-attachments/assets/db86d4bd-4c45-4ad3-93a7-7d9b96136700" />
</p>
Each simulation has a set of variables that can be manuipulated, these are: observation time, turblent velocity and gate valve position. The gate valve is a glass lens cap ontop of the instrument, X-Ray imaging can be accomplished with this on but it filters the lowest energy photons removing a lot of useful data. Unfortunately the team was notified that the gate valve had mechanical issues and was stuck covering the instrument, luckily we have simulated both gate valve on and off prior to the first observation cycle. Below in black is an example of the same simulated cluster without the gate valve, while in red is the data with the gate valve covering the instrument.
<p align="center">
   <img width="914" height="696" alt="Screenshot 2026-08-12 155947" src="https://github.com/user-attachments/assets/1a42fc3a-300f-490a-afe1-0d3f18f7c917" />
</p>

In both cases the Iron-K complex (large emission line around 7keV) appears to be strong with and without the gate valve, therefore we can use that complex to observe gas velocity (as higher turbelent velocities broaden these lines) and treat the Fe-K continuum as the baseline for observations. These simulations can have injected velocity speeds as a true value, then we can test if our linear regression algorithms can accurately extract the same value. Since the Iron-K complex is a set of multiple Fe lines the brightest (Fe-K w-line) is defined as the limiter, any observation that can be done within 200 ks and contains at least 150 Fe-K w-line photons will be deemed a possible subject for observation proposals. Through this there are 4 clusters that produce enough photons and have previously defined lower turbulent velocities which allows us to accurately extract their turbulent speeds through a XRISM observation. The Fe-K complex fit shown below was done through this [non-linear optimization and curve fitting script](./XRISM/heasimscripts/Fit_lines_new.py). 

<p align="center">
   <img width="1163" height="679" alt="Screenshot 2026-08-12 164313" src="https://github.com/user-attachments/assets/26e15824-516b-4aba-9ddc-173ff3337dbd" />
</p>

## **XRISM's First Light (M87)** 
