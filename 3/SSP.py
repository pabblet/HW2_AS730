import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hoki import load
import fsps

plt.style.use('pablet')

#BPASS
data= pd.read_csv('sfh.dat', sep=' ', header=None, names=['time', 'sfr'])
time= np.asarray(data['time'])*1e6
sfr= data['sfr']

plt.step(time*1e-9, sfr, where='mid')
plt.title('Star Formation History')
plt.ylabel(r'SFR (M$_\odot$/yr)')
plt.xlabel(r'Time (Gyr)')
plt.show()

spectra= load.model_output('spectra/spectra-sin-imf135_300.a+00.z020.dat')
wl= spectra.WL

SED= np.zeros(len(wl))
ages= np.arange(6.0, 11.0, 0.1)
now= 13.8e9

for i in np.arange(len(time)-1):
    t=now-time[i]
    index= np.abs(t-10**ages).argmin()
    spectrum= spectra.iloc[:,index]
    mass= sfr[i]*(time[i+1]-time[i])
    SED+= spectrum*mass/1e6 #normalization

att_SED= np.zeros(len(wl))
Av= 1
Rv= 4.05
E= Av/Rv
wl_um= wl*1e-4

for i in range(len(wl)):
    if wl_um[i]<0.63:
        att= 2.659*(-2.156+1.509/wl_um[i]-0.198/wl_um[i]**2+0.011/wl_um[i]**3)+Rv
    elif wl_um[i]>=0.63:
        att= 2.659*(-1.857+1.040/wl_um[i])+Rv

    att_SED[i]= SED[i]*10**(-0.4*att*E)

plt.plot(wl, SED, label='BPASS', alpha=0.5)
plt.plot(wl, att_SED, label='BPASS Calzetti')

#FSPS
sfh= pd.read_csv('sfh.dat', names=['age', 'sfr'], sep=' ', engine='python')
age= np.asarray(sfh.age)/1e3
sfr= np.asarray(sfh.sfr)

sp= fsps.StellarPopulation(compute_vega_mags=False, zcontinuous=1, logzsol=0.0, sfh=3, imf_type=2, imf1=1.30, imf2=2.35, imf3=2.35,
                           imf_lower_limit=0.1, imf_upper_limit=300)
sp.set_tabular_sfh(age, sfr)
print('CSP calculated without dust')
wave, spec= sp.get_spectrum(tage=13.8, peraa=True)

sp2= fsps.StellarPopulation(compute_vega_mags=False, zcontinuous=1, logzsol=0.0, sfh=3, imf_type=2, imf1=1.30, imf2=2.35, imf3=2.35,
                           imf_lower_limit=0.1, imf_upper_limit=300, dust_type=2, dust2=1)
sp2.set_tabular_sfh(age, sfr)
print('CSP calculated with dust')
wave2, spec2= sp2.get_spectrum(tage=13.8, peraa=True)

plt.plot(wave, spec, label='FSPS', alpha=0.5)
plt.plot(wave2, spec2, label='FSPS Calzetti')
plt.title('Spectra of CSP using BPASS and FSPS')
plt.xlim(30,1e5)
plt.ylim(1e-1,1e5)
plt.loglog()
plt.ylabel(r'Flux (L$_\odot$/$\AA$)')
plt.xlabel(r'Wavelength ($\AA$)')
plt.legend()
plt.show()