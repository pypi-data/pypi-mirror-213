# -*- coding: utf-8 -*-
"""
@author: jeremy leconte
"""
import numpy as np
from .util.spectral_object import Spectral_object

class Aerosols(Spectral_object):
    """Dict-like class to handle aerosol composition, reff, and density, and link this to the optical propoerties.
    """

    def __init__(self, aer_reffs_densities=None, a_database=None):
        """__init__ Instantiates an aerosols object.
        """
        super().__init__()
        self.set_a_database(a_database=a_database)
        self.set_aer_reffs_densities(aer_reffs_densities=aer_reffs_densities)
        self._wn_range=None

    def set_aer_reffs_densities(self, aer_reffs_densities=None):
        """Set the dictionary with the arrays of the effective radii and number densities for the aerosols.

        .. warning::
            The unit and physical meaning of the result may change depending on the
            quantity provided in aer_reffs_densities (number density or ratio of particle to gas number density).
            See :func:`exo_k.atable.Atable.absorption_coefficient` for further details.

            For use in the amtospheric model, one should provide the particle to gas number density ratio.

        Parameters
        ----------
            aer_reffs_densities: dict
                A dictionary with aerosol names as keys and lists containing 2
                floats (or arrays) as values. The values are the particle effective radii
                and number densities (or ratio of aerosol to gas number density).
        """
        if aer_reffs_densities is None:
            self.aer_reffs_densities = {}
        else:
            self.aer_reffs_densities = aer_reffs_densities

    def set_a_database(self, a_database=None):
        """Change the radiative database attached to the current instance of aerosols

        Parameters
        ----------
            a_database: :class:`~exo_k.kdatabase.Kdatabase` object
                New Adatabase to use.
        """
        self.adatabase = a_database
        if self.adatabase is not None:
            if self.adatabase.r_eff_unit != 'm' :
                print("""
                You're being Bad!!! You are trying *NOT* to use MKS units
                for the effective radii in the aerosol database!!!""")
                raise RuntimeError("Bad units in the Adatabase used with aerosols.")

    def optical_properties(self, aer_reffs_densities=None, wl_range=None, wn_range=None,
            log_interp=True, compute_all_opt_prop=True, **kwargs):
        """Compute the optical properties for the mix.

        Parameters
        ----------
            aer_reffs_densities: dict
                A dictionary with aerosol names as keys and lists containing 2
                floats (or arrays) as values. The values are the particle effective radii
                and number densities (or ratio of aerosol to gas number density).
                See :func:`exo_k.atable.Atable.absorption_coefficient` for further details.

        Other Parameters
        ----------------
            wl_range, wn_range: two-value list
                Wavelength or wavenumber range to consider
            log_interp: bool, optional
                Whether the interpolation is linear in kdata or in log(kdata).
            compute_all_opt_prop: bool, optional
                Whether to compute all the optical properties or just the extinction.
        """
        if self.adatabase is None: raise RuntimeError("""
            a_database not provided. 
            Use the a_database keyword during initialization or use the set_a_database method.""")
        if self.adatabase.wns is None: raise RuntimeError("""
            All tables in the Adatabase should have the same wavenumber grid to proceed.
            You should probably use sample().""")
        if aer_reffs_densities is not None:
            self.set_aer_reffs_densities(aer_reffs_densities=aer_reffs_densities)

        local_wn_range=self._compute_spectral_range(wl_range=wl_range, wn_range=wn_range)

        [k, k_scat, g] = self.adatabase.optical_properties(self.aer_reffs_densities,
            wngrid_limit=local_wn_range, log_interp=log_interp,
            compute_all_opt_prop=compute_all_opt_prop)
        return [k, k_scat, g]
    
    def absorption_coefficient(self, aer_reffs_densities=None, wl_range=None, wn_range=None,
            log_interp=True, **kwargs):
        """Compute the aerosol opacity for the mix.

        Parameters
        ----------
            aer_reffs_densities: dict
                A dictionary with aerosol names as keys and lists containing 2
                floats (or arrays) as values. The values are the particle effective radii
                and number densities (or ratio of aerosol to gas number density).
                See :func:`exo_k.atable.Atable.absorption_coefficient` for further details.

        Other Parameters
        ----------------
            wl_range, wn_range: two-value list
                Wavelength or wavenumber range to consider
            log_interp: bool, optional
                Whether the interpolation is linear in kdata or in log(kdata).
        """
        if self.adatabase is None: raise RuntimeError("""
            a_database not provided. 
            Use the a_database keyword during initialization or use the set_a_database method.""")
        if self.adatabase.wns is None: raise RuntimeError("""
            All tables in the Adatabase should have the same wavenumber grid to proceed.
            You should probably use sample().""")
        if aer_reffs_densities is not None:
            self.set_aer_reffs_densities(aer_reffs_densities=aer_reffs_densities)

        local_wn_range=self._compute_spectral_range(wl_range=wl_range, wn_range=wn_range)

        return self.adatabase.absorption_coefficient(self.aer_reffs_densities,
            wngrid_limit=local_wn_range, log_interp=log_interp)

