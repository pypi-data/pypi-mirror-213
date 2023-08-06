import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import numpy as np
import pandas as pd
import scipy as sci
import os

import seaborn as sns
sns.set_theme(font_scale=1.5);

from scipy.optimize import curve_fit
from scipy.optimize import minimize

from utils import FileReader, EnergyDistributions

# Globals
Earray  = np.round(np.logspace(np.log10(0.250), np.log10(10000), 100), 2)

h       = np.arange(0, 500);

runList = np.array([10, 14, 20, 32, 50, 71, 100, 141, 200, 316, 500, 
                    707, 1000, 1414, 2000, 3162, 5000, 7071, 10000])

PAlist  = np.arange(0, 70+5, 5);


class api(FileReader):
    def __init__(self):

        # Altitude array abscissa
        self.h = h 
        
        # Energy array abscissa
        self.Earray = Earray 
        
        # Delta E
        self.dE = np.hstack([np.diff(self.Earray), np.diff(self.Earray)[-1]])

        self.EbinCenters = self.Earray + self.dE

        self.runList        = runList
        self.PAlist         = PAlist


        super().__init__(self.Earray, self.runList, self.PAlist)

        self.X_energy, self.Y_altitude = np.meshgrid(self.Earray, self.h)

        # Check if look up table downloaded
        if self._check_if_data_present() is False:

            print("Lookup table data missing, downloading now...")
            
            # If not, download from Zenodo
            self._download_data()
        

    def _check_if_data_present(self):
        """
        Internal function to check if look up table is present
        """
        dirname = os.path.dirname(__file__)

        total_path = dirname + '/data/G4data_mono_discretePAD_0degLat.pkl'

        return os.path.isfile(total_path)

    def _download_data(self):
        """
        Internal function to download 
        """
        import wget
        
        url = "https://zenodo.org/record/8034275/files/G4data_mono_discretePAD_0degLat.pkl?download=1"

        try:
            wget.download(url, out='./data')
            print("Data downloaded!")
        except:
            print("Couldn't download data :( contact Grant.Berland@colorado.edu and I'll email it to you")

    def plot_spectral_profile(self, energyDistribution, 
                                    pitchAngleDistribution, 
                                    flux, 
                                    particle=None):

        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        particle)

        result /= self.EbinCenters[np.newaxis,:]

        result[result < 1e-10] = 0
    
        plt.pcolormesh(self.X_energy, self.Y_altitude, norm * result, norm=LogNorm())
        plt.xscale('log')
        plt.ylim(0, 300)
        plt.xlim(1e0, 1e4)
        plt.ylabel('Altitude [km]')
        plt.xlabel('Energy [keV]')
        plt.colorbar(label='Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$]')


        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return result 


    def get_spectral_profile(self, energyDistribution, 
                                    pitchAngleDistribution, 
                                    flux, 
                                    particle=None):

        result_el, norm_el = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        'electron')

        result_el /= self.EbinCenters[np.newaxis,:]

    
        result_ph, norm_ph = self._formGreensFunctionSpectrum(energyDistribution, 
                                                pitchAngleDistribution, 
                                                flux,
                                                'spectra',
                                                'photon')

        result_ph /= self.EbinCenters[np.newaxis,:]

        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return norm_el * result_el, norm_ph * result_ph 
    
    def plot_ionization_profile(self, energyDistribution, 
                                      pitchAngleDistribution,
                                      flux,
                                      **plotParams):


        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'ioni')

        # Normalize to unity
        result /= np.trapz(result, x=1e5 * self.h)
        
        # Make it integrate to what it should be
        result *= (norm/35)
       
        # Plot on current figure
        plt.semilogx(result, self.h, **plotParams)
    
        plt.xlabel("Ionization Rate [cm$^{-3}$ s$^{-1}$]");
        plt.ylabel("Altitude [km]");

        plt.ylim(0, 300);
        plt.grid(True, which='both')
       
        return result

    # Getter methods
    def get_all_ionization_profiles(self):
        return self._get_ionization_table()

    def get_all_data(self):
        return self._get_all_data()

    def get_altitude_array(self):
        return self.h

    def get_spectral_abscissa(self):
        return self.X_energy, self.Y_altitude

    def get_energy_array(self):
        return self.Earray

    def get_bin_width(self):
        return self.binWidth

    def get_run_list(self):
        return self.runList

    def get_PA_list(self):
        return self.PAlist


class XrayAnalysis(FileReader):
    def __init__(self):
        
        # Import globals
        self.Earray         = Earray
        self.runList        = runList
        self.PAlist         = PAlist 

        self.dE = np.hstack([np.diff(Earray), np.diff(Earray)[-1]])
        self.EbinCenters = self.Earray + self.dE

        # Send them up
        super().__init__(self.Earray, self.runList, self.PAlist)


    def getSpectrumAtAltitude(self, energyDistribution, pitchAngleDistribution, flux, altitudeRange):

        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        'photon')

        spectrum = norm * np.mean(result[altitudeRange[0]:altitudeRange[1],:], axis=0)

        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return spectrum / self.EbinCenters

    



class RadiationAnalysis:
    def __init__(self, material):
        
        if material is "human":
            
            filepath_pre  = "../data/radiationData/"
            filepath_post = "_human_dose_conversion.csv"

            # Read in data
            # [energy in keV, conversion factor in Sv-cm^2]
            self.el_conv = pd.read_csv(filepath_pre + "electron" + filepath_post, names=['E', 'C']) 
            self.ph_conv = pd.read_csv(filepath_pre + "photon"   + filepath_post, names=['E', 'C'])

    def calculate_radiation_dose(self, el_spectra, ph_spectra):
    
        dosage_alt_array = np.zeros([len(h)]);
   
        for i in range(0, len(h)):
            dosage_alt_array[i] = 2 * np.pi * np.sum(el_spectra[i,:] * self.el_conv.C + \
                                         ph_spectra[i,:] * self.ph_conv.C)

        return dosage_alt_array;

    def _calculate_differential_radiation_dose(self, el_spectra, ph_spectra):
    
        dosage_alt_array = np.zeros([len(h), 100]);
    
        for i in range(0, len(h)):
            dosage_alt_array[i,:] = el_spectra[i,:] * self.el_conv.C + \
                                    ph_spectra[i,:] * self.ph_conv.C

        return dosage_alt_array;



'''
TODO: loop in Jovian EPP model
class JUNO(DataHandler):
    def __init__(self):
        pass
'''
