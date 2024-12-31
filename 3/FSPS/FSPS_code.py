import numpy as np
import matplotlib.pyplot as plt
import fsps

plt.style.use('pablet')

sp= fsps.StellarPopulation(compute_vega_mags=False, zcontinuous=1, logzsol=0.0, sfh=5, imf_type=0, dust_type=2)
print('SSP calculated')

wave, spec= sp.get_spectrum(tage=1.56, peraa=True)
plt.plot(wave, spec)
plt.xlabel('log(Wavelength [$\AA$])')
plt.ylabel('log(Flux [erg/s/cm$^{2}$/ $\AA$])')
plt.title('Spectrum of SSP')
plt.loglog()
plt.show()
