# -*- coding: utf-8 -*-
"""
@author: jeremy leconte
"""
import numpy as np
import numba
from exo_k.util.cst import PI, N_A

#@numba.jit(nopython=True, fastmath=True, cache=True)
def mmr_to_number_density(mmr, gas_density, r_eff, aerosols_bulk_density):
    """Converts a mass mixing ratio (mmr or q) in a number density of particles
    (in number per unit volume)

    Parameters
    ----------
        mmr: float or array
            Mass mixing ratio (in kg per kg of air)
        gas_density: float or array
            Density of the gas (in kg/m^3)
        r_eff: float or array
            Effective radius of the particles (m)
        aerosols_bulk_density: float or array
            Density of the constituent of the condensed particles (in kg/m^3)
    """
    particle_mass = 4. * PI * r_eff**3 * aerosols_bulk_density / 3.
    #print(particle_mass.shape, mmr.shape, gas_density.shape)
    return mmr * gas_density / particle_mass

#@numba.jit(nopython=True, fastmath=True, cache=True)
def mmr_to_number_density_ratio(mmr, Mgas, r_eff, aerosols_bulk_density):
    """Converts a mass mixing ratio (mmr or q) in a ratio between particles density
    and molecules density

    Parameters
    ----------
        mmr: float or array
            Mass mixing ratio (in kg per kg of air)
        Mgas: float or array
            gas molar mass (in kg/mol)
        r_eff: float or array
            Effective radius of the particles (m)
        aerosols_bulk_density: float or array
            Density of the constituent of the condensed particles (in kg/m^3)
    """
    particle_mass = 4. * PI * r_eff**3 * aerosols_bulk_density / 3.
    #print(particle_mass.shape, mmr.shape, gas_density.shape)
    return mmr * Mgas / (particle_mass * N_A)
