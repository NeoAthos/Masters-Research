#!/usr/bin/env python

#import syspython
from astropy.table import Table
import numpy as np
from astropy.units import *
from astropy import units as u
from matplotlib.pyplot import *
from astropy.cosmology import FlatLambdaCDM as LCDM
import matplotlib.backends.backend_pdf as many_pdf


def get_r(DA,asec_kpc,rin,rout):
    rin = (rin*0.492/asec_kpc)*kpc
    rout = (rout*0.492/asec_kpc)*kpc
    r = ((rin + rout)/2).value
    dr = rout.value - r
    return rin,rout,r, dr

def get_ne0(DA,z,n0,rin,rout,n_p0,n_n0):
    ne0 = (DA * (1 + z) * 10**7 * np.sqrt(n0 * 4 * np.pi * 1.2 / (4./3 * np.pi * ((rout)**3 - (rin)**3)))).cgs.value
    ne_p0 = 1./2 * (ne0 / n0) * (n_p0)
    ne_n0 = abs(1./2 * (ne0 / n0) * (n_n0))
    return ne0,ne_p0,ne_n0

def kt_units(kt0,kt_p0,kt_n0):
    
    kt_units0 = kt0*keV
    kt_p_units0 = kt_p0*keV
    kt_n_units0 = abs(kt_n0)*keV
    
    
    kt_cgs0 = kt_units0.cgs
    kt_cgs_p0 = kt_p_units0.cgs.value
    kt_cgs_n0 = kt_n_units0.cgs.value
    
    kt_value0 = kt_cgs0.value
    
    return kt_units0,kt_p_units0,kt_n_units0,kt_cgs0,kt_cgs_p0,kt_cgs_n0,kt_value0

def get_P(ne0,kt_value0,kt_cgs_p0,kt_cgs_n0):
    P0 = 2 * ne0 * kt_value0
    P_p0 = np.sqrt((2 *kt_value0 * ne_p0)**2 + (2 * ne0 * kt_cgs_p0)**2) #Propagate Error
    P_n0 = np.sqrt((2 *kt_value0 * ne_n0)**2 + (2 * ne0 * kt_cgs_n0)**2)
    return P0,P_p0,P_n0

def get_K(kt0,ne0,ne_p0,kt_p0,ne_n0,kt_n0):
    K0 = kt0 * ne0**(-2.0/3)
    K_p0 = np.sqrt((-2./3 * kt0 * ne0**(-5./3)*ne_p0)**2 + (ne0**(-2./3)*kt_p0)**2) #Propagation of Error
    K_n0 = np.sqrt((-2./3 * kt0 * ne0**(-5./3)*ne_n0)**2 + (ne0**(-2./3)*kt_n0)**2)
    return K0,K_p0,K_n0

def get_Mgas(rin,rout,dr,P0,kt_value0,P_p0,kt_cgs_p0,P_n0,kt_cgs_n0):
    
    mean_mol_m = 0.62 #4/(6*(0.75)+0.24+2)
    mp = (1.67e-27)*1000 #mass of proton in g
    m_solar = 1.989e+33 #Solar mass in cgs
    
    r_out = (rout.cgs).value
    r_in = (rin.cgs).value
    r_avg = (r_out + r_in) / 2.0
    dr_kpc = (dr*u.kpc)
    dr_cgs = ((dr_kpc).cgs).value
    M_g0 = P0  * mean_mol_m * mp *(4./3 * np.pi * (r_out**3 - r_in**3)) / (kt_value0)
    
    M_g_p0 = np.sqrt((mean_mol_m * mp * (4./3 * np.pi * (r_out**3 - r_in**3)) * P_p0/kt_value0)**2 + (-P0  * mean_mol_m * mp * (4./3 * np.pi * (r_out**3 - r_in**3)) * kt_cgs_p0/kt_value0**2)**2)
    M_g_n0 = np.sqrt((mean_mol_m * mp * (4./3 * np.pi * (r_out**3 - r_in**3)) * P_n0/kt_value0)**2 + (-P0  * mean_mol_m * mp * (4./3 * np.pi * (r_out**3 - r_in**3)) * kt_cgs_n0/kt_value0**2)**2)
    
    Mgas_cum0 = M_g0.cumsum()
    dM_g_p0 = M_g_p0.cumsum()
    dM_g_n0 = M_g_n0.cumsum()
    
    return mean_mol_m,mp,m_solar,r_out,r_in,r_avg,dr_kpc,dr_cgs,M_g0,M_g_p0,M_g_n0,Mgas_cum0,dM_g_p0,dM_g_n0

def get_flux_lum(cosmo,z,logflux0,logflux_p0,logflux_n0):
    d_l = cosmo.luminosity_distance(z)
    flux0 = 10**(logflux0)*(u.erg/(u.s * u.cm**2))
    flux_p0 = 10**(logflux0 + logflux_p0)*(u.erg/(u.s * u.cm**2))
    flux_n0 = 10**(logflux0 - logflux_n0)*(u.erg/(u.s * u.cm**2))
    Lx0 = flux0 * 4 * np.pi * (d_l**2).to(u.cm**2)
    Lx_p0 = flux_p0 * 4 * np.pi * (d_l**2).to(u.cm**2) - Lx0
    Lx_n0 = (flux_n0) * 4 * np.pi * (d_l**2).to(u.cm**2) - Lx0
    return d_l,flux0,flux_p0,flux_n0,Lx0,Lx_p0,Lx_n0

def get_tcool(r_in,r_out,P0,P_p0,P_n0,Lx0,Lx_p0,Lx_n0):
    
    r_out = r_out*u.cm
    r_in = r_in*u.cm
    
    P0  = P0*(u.erg/(u.cm**3))
    P_p0 = P_p0*(u.erg/u.cm**3)
    P_n0 = P_n0*(u.erg/u.cm**3)
    
    t_cool0 = (3 * P0 * 4./3 * np.pi * (r_out**3 - r_in**3).to(u.cm**3)) / (2 * Lx0)
    t_cool_p0  = np.sqrt((3 * 4./3 * np.pi * (r_out**3 - r_in**3) * P_p0 / (2*Lx0))**2 + (-3 * P0 * 4./3 * np.pi * (r_out ** 3 - r_in**3) * Lx_p0/(2 * Lx0**2))**2)
    t_cool_n0  = np.sqrt((3 * 4./3 * np.pi * (r_out**3 - r_in**3) * P_n0 / (2*Lx0))**2 + (-3 * P0 * 4./3 * np.pi * (r_out**3 - r_in**3) * Lx_n0/(2 * Lx0**2))**2)
    
    tcool0 = ((t_cool0).to(u.year)).value
    tcool_p0 = ((t_cool_p0).to(u.year)).value
    tcool_n0 = ((t_cool_n0).to(u.year)).value
    
    return r_out,r_in,P0,P_p0,P_n0,t_cool0,t_cool_p0,t_cool_n0,tcool0,tcool_p0,tcool_n0

def make_graph(pdf,title0,yaxis0,xdata,ydata,yerr0=None,log0=None):
    l1, l2, font, s1, s2, padding = 3.0, 10.0, 20.0, 25.0, 15.0, 10.0
    rcParams.update({'font.size': font})
    fig0 = figure('Histogram', figsize = (s1, s2))
    xlabel('Radius (kpc)',fontsize=30)
    title(r'{}'.format(title0))
    ylabel(r'{}'.format(yaxis0),fontsize=30)
    xscale('log')
    if log0 is not None:
        yscale('log')
    scatter(xdata,ydata,color='red')
    if yerr0 is not None:
        errorbar(xdata,ydata,yerr=yerr0,ecolor='red',color='none')
    pdf.savefig(fig0)
    close(fig0)
    return


path=sys.argv[1]

cluster_name=sys.argv[2]

z=sys.argv[3]

cosmo = LCDM(70,0.3)
z=float(z)
#fout=open(cluster_name+"/"+cluster_name+"_projected_properties.csv",'w')
fout=open(path+cluster_name+"_project_properties.csv",'w')
pdf0=many_pdf.PdfPages(path+cluster_name+'_plot_projected_properties.pdf')
#rin,rout,nh0,nh_p0,nh_n0,kt0,kt_p0,kt_n0,Z0,Z_p0,Z_n0,n0,n_p0,n_n0,stats0,logflux0,logflux_p0,logflux_n0,chi,dof,rechi = np.genfromtxt(cluster_name+"/spct/specfits.csv",unpack = True)
rin,rout,nh0,nh_p0,nh_n0,kt0,kt_p0,kt_n0,Z0,Z_p0,Z_n0,n0,n_p0,n_n0,stats0,logflux0,logflux_p0,logflux_n0,chi,dof,rechi,unknown = np.genfromtxt(path+"specfits.csv",unpack = True)

DA = cosmo.angular_diameter_distance(z)

print('DA:',DA)
asec_kpc = float(cosmo.arcsec_per_kpc_proper(z).value)

rin,rout,r,dr=get_r(DA,asec_kpc,rin,rout)

ne0,ne_p0,ne_n0=get_ne0(DA,z,n0,rin,rout,n_p0,n_n0)

kt_units0,kt_p_units0,kt_n_units0,kt_cgs0,kt_cgs_p0,kt_cgs_n0,kt_value0=kt_units(kt0,kt_p0,kt_n0)

P0,P_p0,P_n0=get_P(ne0,kt_value0,kt_cgs_p0,kt_cgs_n0)

K0,K_p0,K_n0=get_K(kt0,ne0,ne_p0,kt_p0,ne_n0,kt_n0)

mean_mol_m,mp,m_solar,r_out,r_in,r_avg,dr_kpc,dr_cgs,M_g0,M_g_p0,M_g_n0,Mgas_cum0,dM_g_p0,dM_g_n0=get_Mgas(rin,rout,dr,P0,kt_value0,P_p0,kt_cgs_p0,P_n0,kt_cgs_n0)

d_l,flux0,flux_p0,flux_n0,Lx0,Lx_p0,Lx_n0=get_flux_lum(cosmo,z,logflux0,logflux_p0,logflux_n0)

r_out,r_in,P0,P_p0,P_n0,t_cool0,t_cool_p0,t_cool_n0,tcool0,tcool_p0,tcool_n0=get_tcool(r_in,r_out,P0,P_p0,P_n0,Lx0,Lx_p0,Lx_n0)

fout.write("#r_avg,dr,kT,kT_p,kT_m,Z,Z_p,Z_m,norm,norm_p,norm_m,log10flux,log10flux_p,log10flux_m,reduced_chisquare,ne,ne_p,ne_m,P,P_p,P_m,K,K_p,K_m,Mgas,Mgas_p,Mgas_m,Lx,Lx_p,Lx_n,tcool,tcool_p,tcool_m\n")

'''print(len(r))
print(len(dr))
print(len(kt0))
print(len(kt_p0))
print(len(kt_n0))
print(len(Z0))
print(len(Z_p0))
print(len(Z_n0))
print(len(ne0))
print(len(P0))
print(len(P_p0))
print(len(P_n0))
print(len(K0))
print(len(K_p0))
print(len(K_n0))
print(len(Mgas_cum0))
print(len(dM_g_p0))
print(len(dM_g_n0))
print(len(Lx0))
print(len(Lx_p0))
print(len(Lx_n0))
print(len(tcool0))
print(len(tcool_p0))
print(len(tcool_n0))'''

for j in range (len(tcool0)):
    fout.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(r[j], dr[j], kt0[j],kt_p0[j], abs(kt_n0[j]), Z0[j], Z_p0[j], abs(Z_n0[j]),n0[j],n_p0[j],abs(n_n0[j]),logflux0[j],logflux_p0[j],abs(logflux_n0[j]),rechi[j], ne0[j], ne_p0[j], abs(ne_n0[j]),P0[j].value, P_p0[j].value, abs(P_n0[j].value), K0[j],  K_p0[j], abs(K_n0[j]), Mgas_cum0[j],dM_g_p0[j],  abs(dM_g_n0[j]),Lx0[j].value, Lx_p0[j].value, abs(Lx_n0[j].value),tcool0[j], tcool_p0[j], abs(tcool_n0[j])))

fout.close()

print('plot')

make_graph(pdf0,'Temperature','kT (keV)',r,kt0,yerr0=[abs(kt_n0),kt_p0],log0=True)
print(1)
make_graph(pdf0,'Metallicity','Z',r,Z0,yerr0=[abs(Z_n0),Z_p0],log0=True)
print(2)
make_graph(pdf0,'Flux (erg/cm$^2$/s)','log10(Flux)',r,logflux0,yerr0=[abs(logflux_n0),logflux_p0])
print(3)
make_graph(pdf0,'Normalization','Norm',r,n0,yerr0=[abs(n_n0),n_p0],log0=True)
make_graph(pdf0,'n$_e$','n$_e$',r,ne0,yerr0=[abs(ne_n0),ne_p0],log0=True)
make_graph(pdf0,'Pressure','P (erg/cm$^3$)',r,P0.value,yerr0=[abs(P_n0.value),P_p0.value],log0=True)
make_graph(pdf0,'Entropy','K (keV cm$^2$)',r,K0,yerr0=[abs(K_n0),K_p0],log0=True)
make_graph(pdf0,'Hot gas mass','M$_{gas}$ (solarmass)',r,Mgas_cum0,yerr0=[abs(dM_g_n0),dM_g_p0],log0=True)
make_graph(pdf0,'Luminosity','Lx (erg/s)',r,Lx0.value,yerr0=[abs(Lx_n0.value),Lx_p0.value],log0=True)
make_graph(pdf0,'t$_{cool}$','t$_{cool}$ (yr)',r,tcool0,yerr0=[abs(tcool_n0),tcool_p0],log0=True)

pdf0.close()






