# UWaterloo MSc Research
**Observations of X-Ray telescopes (CHANDRA and XRISM)**
## Introduction
This is the cumalitive work that was completed during my MSc at the University of Waterloo, this work required knowledge in the fields of astrophysics, data science and data analysis. The code primarily was done through Python (Juptyer and IDEs), yet it also extended to Tcl and Bash scripting. Several tools produced by HEASARC, SRON, and NASA were also utilized, with key tools being SPEX and Xspec. 
My research is subdivided into 3 projects:

## **CHANDRA Datasheets & Dasboards** 
CHANDRA is an older X-ray telescope (deployed 1999) with a high imaging resolution (0.5 arcsec) and a low spectral resolution (95 eV). I extracted the X-ray spectra radially to observe radial relationships with plasma temperature and metallicity between 16 commonly observed clusters. Below is an example of the perseus cluster with equally weighted spectral rings. Each ring has has a unique spectrum, upon using linear regression algorthims extracting key features per ring (metallicity, temperature & cooling time) to produce unique graphs per cluster. You can inspect the logic inside the [Annulus generation](./CHANDRA/new_scripts/pre_extract/annulus.py) and [Spectrum extraction](./CHANDRA/new_scripts/pre_extract/specextractmaster_sum.py) scripts.
<p align="center">
   <img width="720" height="650" alt="Screenshot from 2025-01-05 14-16-44" src="https://github.com/user-attachments/assets/ce7b33ab-b612-419e-a932-831d1813d948" />  
</p>
This data is then collected into a dashboard to be compared to with other clusters, allowing for a deeper scientific analysis between cluster types (cool core and non-cool core). By observing and comparing multiple clusters together there were two clusters that are unique and do not follow expected results, this could only be accomplished through observing these dashboards/datasheets!  
 
<p align="center">
   <img width="956" height="647" alt="Screenshot 2026-08-11 142054" src="https://github.com/user-attachments/assets/8acc5e86-4944-4554-920f-824026e8ff0c" />
</p>
These datasheets are created through 
   
2.
3. 
