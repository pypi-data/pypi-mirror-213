# -*- coding: utf-8 -*-
"""
@author: jeremy leconte

This module contain classes to fit a spectrum
"""
import copy
import time
import numpy as np
import scipy.optimize as sciopt
from .atm import Atm
from .util.cst import G


class Fit(object):
    """Class to fit spectra
    """

    def __init__(self, spectrum_to_fit=None, uncertainties=None, fitting_parameters=None, **kwargs):
        """Initialization method. 
        """
        self.cost_function = None
        self.atm = None
        self.N_iter = 0
        self.spectrum_to_fit = None
        self.set_spectrum_to_fit(spectrum_to_fit=spectrum_to_fit, uncertainties=uncertainties)
        
        if fitting_parameters is not None:
            self.set_fitting_parameters(fitting_parameters=fitting_parameters)


    def init_atmosphere(self, composition=None, Mp=None, **kwargs):
        """initializes atmospheric model
 
        Parameters
        ----------
            Mp: float
                Mass of the planet in Kg.
        """
        if composition is None:
            raise RuntimeError('composition should not be None')
        self.atm = Atm(composition=composition, **kwargs)
        self.composition = copy.deepcopy(composition)
        self.Mp = Mp

    def set_fitting_parameters(self, fitting_parameters=None):
        """
        Parameters
        ----------
            fitting_paramaters: list of str
                The parameters to fit.
                Must be in T, Rp, logx_MOL
        """
        if fitting_parameters is None:
            raise RuntimeError('fitting_parameters should not be None.')
        self.fitting_parameters = fitting_parameters
        self.Nparam = len(self.fitting_parameters)

    def set_spectrum_to_fit(self, spectrum_to_fit=None, uncertainties=None):
        """
        Parameters
        ----------
            spectrum_to_fit: :class:`Spectrum` object
                The spectrum to fit
            uncertainties: float or array
                The uncertainty on each spectral point. 
        """
        if spectrum_to_fit is None:
            raise RuntimeError('spectrum_to_fit should not be None.')
        self.spectrum_to_fit = spectrum_to_fit
        if uncertainties is None:
            raise RuntimeError('uncertainties should not be None.')
        self.uncertainties = uncertainties
        self.Nw = self.spectrum_to_fit.value.size
    
    def plot_spectrum_to_fit(self, ax, capsize=0, fmt='k.', ecolor='.7',
            ylabel='Depth', xlabel='Wavelength', **kwargs):
        """Plots the spectrum that is fitted with uncertainties
        """
        ax.errorbar(self.spectrum_to_fit.wls, self.spectrum_to_fit.value, yerr=self.uncertainties,
                capsize=capsize, fmt=fmt, ecolor=ecolor)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        

    def transmission_spectrum(self, parameters, rebin_spectrum=False, **kwargs):
        """Method to compute the spectrum with a new set of parameters
        """
        var_species = 0
        var_comp = self.composition
        for ii, param in enumerate(self.fitting_parameters):
            if param == 'T':
                tlay = np.ones(self.atm.Nlay) * parameters[ii]
                self.atm.set_T_profile(tlay)
            if param.startswith('logx_'):
                mol = param[5:]
                var_comp[mol] = np.power(10., parameters[ii])
                var_species += 1
            if param == 'Rp':
                self.atm.set_Rp(parameters[ii])
                if self.Mp is not None:
                    grav = G * self.Mp / parameters[ii]**2
                    self.atm.set_grav(grav=grav)
        if var_species > 0:
            self.atm.set_gas(var_comp)
        spectrum = self.atm.transmission_spectrum(**kwargs)
        if rebin_spectrum: spectrum.bin_down(self.spectrum_to_fit.wnedges)
        return spectrum

    def set_cost_function(self):
        """
        Defines the cost (or merit) function to minimize. 
        """
        if self.spectrum_to_fit is None:
            raise RuntimeError('Use set_spectrum_to_fit before setting cost function.')
        if self.atm is None:
            raise RuntimeError('Use init_atmosphere before setting cost function.')
        if self.atm.k_database is None:
            raise RuntimeError('A k_database should be provided to init_atmosphere.')
        self.rebin_spectrum = np.any(self.atm.k_database.wnedges != self.spectrum_to_fit.wnedges)
        def distance(parameters):
            self.last_spec = self.transmission_spectrum(parameters, rebin_spectrum=self.rebin_spectrum)
            return np.sum(((self.last_spec.value - self.spectrum_to_fit.value)/self.uncertainties)**2)/self.Nw
        self.cost_function = distance

    def set_progress_report(self, Nprint=None):
        if Nprint is not None:
            self.Nprint = Nprint
            self.N_iter = 0
            def callback(parameters):
                if self.N_iter % self.Nprint == 0:
                    res=dict()
                    for ii, param in enumerate(self.fitting_parameters):
                        res[param] = parameters[ii]
                    print('Niter=',self.N_iter, res)
                self.N_iter += 1
            self.callback = callback
        else:
            self.callback = None
        return None
    
    def minimize(self, initial_guess=None, bounds=None, method='Nelder-Mead',
            verbose=False, tol=.1e0, Nprint=None, **kwargs):
        """
        Minimizes the cost function over the fitting parameters. 

        Parameters
        ----------
            initial_guess: list
                Initial value for the fitting parameters.
                Must be in the order declared in fitting_parameters.
            bounds: list or 2-value arrays
                Lower and upper values for the parameters.
                Must be in the order declared in fitting_parameters.
            method: str
                Method used for minimization. 
                For now, only 'Nelder-Mead' seems to handle bounds and yield relatively
                good results.
            tol: float
                tolerance transmitted to sciopt.minimize
        """        
        self.set_bounds(bounds=bounds)
        if initial_guess is None:
            initial_guess = np.zeros(self.Nparam)
            for ii in range(self.Nparam):
                initial_guess[ii] = 0.5 * (self.bounds[ii][0] + self.bounds[ii][1])
        self.set_cost_function()
        start = time.time()
        if verbose:
            print(self.cost_function, initial_guess,
            method, bounds,
            tol)
        self.set_progress_report(Nprint)
        self.full_minimize_output = sciopt.minimize(self.cost_function, initial_guess,
            method=method, bounds=self.bounds,
            tol=tol, callback=self.callback, **kwargs)
        self.best_fit_parameters = self.full_minimize_output.x
        if verbose:
            print('computation time: ', time.time()-start,'s')
            print(self.best_fit())
            print(self.full_minimize_output)
        return self.best_fit()

    def best_fit(self):
        """Output last fit results in a dictionary
        """
        res = dict()
        for ii, param in enumerate(self.fitting_parameters):
            res[param] = self.best_fit_parameters[ii]
        return res

    def best_fit_spectrum(self, rebin_spectrum=False):
        """Returns the spectrum computed with the best fit parameters
        """
        spectrum = self.transmission_spectrum(self.best_fit_parameters, rebin_spectrum=rebin_spectrum)
        return spectrum

    def contributions(self, rebin_spectrum=False):
        """Computes a spectrum with each molecule contribution
        """
        molecules = set(self.atm.gas_mix.composition.keys())
        molecules = molecules.intersection(self.atm.gas_mix.k_database.molecules) 
        spectra = dict()
        for mol in molecules:
            inactive_mols = list(self.atm.gas_mix.composition.keys()-{mol})
            spectra[mol] = self.transmission_spectrum(self.best_fit_parameters, rebin_spectrum=rebin_spectrum,
                    inactive_molecules=inactive_mols)
        return spectra

    def set_log_likelihood(self):
        """
        Defines the log likelihood. 
        """
        if self.spectrum_to_fit is None:
            raise RuntimeError('Use set_spectrum_to_fit before setting cost function.')
        if self.atm is None:
            raise RuntimeError('Use init_atmosphere before setting cost function.')
        if self.atm.k_database is None:
            raise RuntimeError('A k_database should be provided to init_atmosphere.')
        self.rebin_spectrum = np.any(self.atm.k_database.wnedges != self.spectrum_to_fit.wnedges)
        def loglike(parameters):
            self.last_spec = self.transmission_spectrum(parameters, rebin_spectrum=self.rebin_spectrum)
            return -0.5 * np.sum(((self.last_spec.value - self.spectrum_to_fit.value)/self.uncertainties)**2)
        self.loglike = loglike
    
    def set_bounds(self, bounds=None):
        if bounds is None:
            print("""You should provide bounds in the form of a dictionary
where keys are the fitting parameters and values are
2 value arrays with the lower and upper bounds.""")
            raise RuntimeError('bounds should not be None.')
        self.upper_bounds = np.ones(self.Nparam)
        self.lower_bounds = np.zeros(self.Nparam)
        self.bounds = list()
        for ii, param in enumerate(self.fitting_parameters):
            try:
                self.upper_bounds[ii] = bounds[param][1]
                self.lower_bounds[ii] = bounds[param][0]
                self.bounds.append([bounds[param][0], bounds[param][1]])
            except:
                self.upper_bounds[ii] = bounds['logx'][1]
                self.lower_bounds[ii] = bounds['logx'][0]
                self.bounds.append([bounds['logx'][0], bounds['logx'][1]])

    def set_prior_transform(self, bounds=None):
        """
        Defines the piors. 
        """
        self.set_bounds(bounds=bounds)
        self.delta_bounds = self.upper_bounds-self.lower_bounds

        def prior_transform(x):
            return self.delta_bounds * x + self.lower_bounds
        self.prior_transform = prior_transform

    def sample(self, bounds=None, method='single',
            npoints=10, maxcall=None,
            verbose=False, **kwargs):
        """
        Minimizes the cost function over the fitting parameters. 

        Parameters
        ----------
            initial_guess: list
                Initial value for the fitting parameters.
                Must be in the order declared in fitting_parameters.
            bounds: list or 2-value arrays
                Lower and upper values for the parameters.
                Must be in the order declared in fitting_parameters.
            method: str
                Method used for minimization. 
                For now, only 'Nelder-Mead' seems to handle bounds and yield relatively
                good results.
            tol: float
                tolerance transmitted to sciopt.minimize
        """        
        import nestle
        self.set_log_likelihood()
        self.set_prior_transform(bounds=bounds)
        start = time.time()
        self.full_sample_output = nestle.sample(self.loglike, self.prior_transform,
                self.Nparam, method=method, npoints=npoints, maxcall=maxcall, **kwargs)

        # weighted average and covariance:
        self.best_fit_parameters, self.covariance = nestle.mean_and_cov( \
                    self.full_sample_output.samples, self.full_sample_output.weights)

        if verbose:
            print('computation time: ', time.time()-start,'s')
            #print(self.full_sample_output.summary)
            for ii, param in enumerate(self.fitting_parameters):
                print(param+" = {0:5.2f} +/- {1:5.2f}".format( \
                    self.best_fit_parameters[ii], np.sqrt(self.covariance[ii, ii])))

        return self.best_fit()
