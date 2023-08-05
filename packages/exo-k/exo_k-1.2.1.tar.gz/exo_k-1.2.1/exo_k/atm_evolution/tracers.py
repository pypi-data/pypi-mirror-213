# -*- coding: utf-8 -*-
"""
@author: jeremy leconte
"""
import numpy as np
import numba
from .convection import dry_convective_adjustment_numba, turbulent_diffusion_numba
from exo_k.util.molar_mass import Molar_mass
from exo_k.util.cst import PI, N_A
from exo_k.aerosol.util_aerosol import mmr_to_number_density_ratio

class Tracers(object):

    def __init__(self, settings, tracers=None, tracer_values=None, Kzz=0., Dmol=0.,
            bg_vmr=None, M_bg=None, Nlay=None, **kwargs):
        """Class that deals with tracers. 

        Fills out the tracers.qarray and creates tracer_names, a table of correspondence
        between tracer names and indices in tracers.qarray.
        """
        self.settings=settings
        if tracers is None:
            self.Ntrac=1
            tracers = {'inactive_tracer':{}}
        else:
            self.Ntrac = len(tracers)
        if tracer_values is None:
            tracer_values = {}
        if Nlay is not None:
            self.Nlay = Nlay
        else:
            raise RuntimeError("We need to know Nlay to initialize Tracers")
        self.bg_vmr = bg_vmr.copy()
        self.gas_vmr = bg_vmr.copy()
        self.var_gas_idx = list()
        self.aerosols_idx = list()
        self.var_gas_names = list()
        self.aerosols_names = list()
        self.gas_molar_masses = list()
        self.aerosols_bulk_density = list()
        self.aerosols_r_eff = list()
        self.some_var_gases = False
        self.some_active_aerosol = False
        self.dico=tracers
        self.namelist = list(tracers.keys())
        self.idx = dict()
        self.qarray = np.empty((self.Ntrac, self.Nlay))
        self.qsurf = np.zeros(self.Ntrac)
        self.qdeep = - np.ones(self.Ntrac)
        for ii, name in enumerate(self.namelist):
            self.idx[name]=ii
            if name in tracer_values.keys():
                self.qarray[ii]=np.copy(tracer_values[name])
            elif 'init_value' in self.dico[name].keys():
                self.qarray[ii]=np.ones(self.Nlay)*self.dico[name]['init_value']
            else:
                self.qarray[ii]=np.zeros(self.Nlay)
            if 'type' in self.dico[name]:
                if self.dico[name]['type'] in ('gas', 'vapor'):
                    self.some_var_gases = True
                    self.var_gas_idx.append(ii)
                    self.var_gas_names.append(name)
                    self.gas_molar_masses.append(Molar_mass().fetch(name))
                if self.dico[name]['type'] in ('aerosol'):
                    self.some_active_aerosol = True
                    self.aerosols_idx.append(ii)
                    self.aerosols_names.append(name)
                    self.aerosols_bulk_density.append(self.dico[name]['bulk_density'])
                    self.aerosols_r_eff.append(self.dico[name]['r_eff'])
                if 'q_deep' in self.dico[name]:
                    self.qdeep[ii] = np.copy(self.dico[name]['q_deep'])
            if 'surface_reservoir' in self.dico[name]: # should be reserved to condensates
                self.qsurf[ii] = np.copy(self.dico[name]['surface_reservoir'])
                self.settings.set_parameters(surface_reservoir = True)
        self.var_gas_idx = np.array(self.var_gas_idx)
        self.var_gas_names = np.array(self.var_gas_names)
        self.gas_molar_masses = np.array(self.gas_molar_masses)
        self.aerosols_idx = np.array(self.aerosols_idx)
        self.aerosols_names = np.array(self.aerosols_names)
        self.aerosols_bulk_density = np.array(self.aerosols_bulk_density)
        self.aerosols_r_eff = np.array(self.aerosols_r_eff)
        self.M_bg = M_bg
        self.update_gas_composition()
        self.Kzz = np.ones(self.Nlay)*Kzz
        self.Dmol = Dmol

    def update_gas_composition(self, update_vmr=True):
        """Performs mass to volume mixing ratio conversion,
        computes the new molar mass of the total gas
        and transmits new composition to the radiative model. 

        !!!Small discrepancies with case without tracers!!!
        Maybe a problem with the background gas. JL22 => is this still true ? 

        Parameters
        ----------
            atm: exo_k.Atm object
                If atm is provided, its composition will be
                updated with the new composition.
        """
        qvar = np.zeros(self.Nlay)
        ovMvar = np.zeros(self.Nlay)
        for ii, idx in enumerate(self.var_gas_idx):
            qvar += self.qarray[idx]
            ovMvar += self.qarray[idx]/self.gas_molar_masses[ii]
        ovMbg=1./self.M_bg
        self.Mgas = 1./((1.-qvar)*ovMbg + ovMvar)
        if update_vmr:
            var_vmr_tot = 0.
            for ii, idx in enumerate(self.var_gas_idx):
                vmr_tmp = np.core.umath.maximum(
                    self.Mgas * self.qarray[idx] / self.gas_molar_masses[ii], 0.)
                    #conversion to vmr
                self.gas_vmr[self.var_gas_names[ii]] = vmr_tmp
                var_vmr_tot += vmr_tmp
                #print(vmr_tmp, var_vmr_tot, isinstance(vmr_tmp, (np.ndarray)))
            var_vmr_tot = 1. - var_vmr_tot    
            #print(var_vmr_tot)
            for mol, vmr in self.bg_vmr.items():
                #print(mol, vmr, var_vmr_tot, isinstance(var_vmr_tot, (np.ndarray)))
                self.gas_vmr[mol] = vmr * var_vmr_tot

    def update_aerosol_properties(self, atm):
        if self.some_active_aerosol:
            aer_reffs_densities = {}
            #atm.compute_mass_density()
            for ii, idx in enumerate(self.aerosols_idx):
                mmr_rad = np.sqrt(self.qarray[idx,1:] * self.qarray[idx,:-1])
                aer_reffs_densities[self.aerosols_names[ii]] = [self.aerosols_r_eff[ii], 
                    mmr_to_number_density_ratio(mmr_rad, atm.Mgas_rad, self.aerosols_r_eff[ii], self.aerosols_bulk_density[ii])]
        else:
            aer_reffs_densities = None
        return aer_reffs_densities

    def turbulent_diffusion(self, timestep, Htot, atm, cp):
        """Mixes tracers following a diffusion equation
        with a constant Kzz parameter (self.Kzz in m^2/s).

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
                (needs to be converted before it is sent to `turbulent diffusion`)
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed
            atm: :class:`Atm` object
                The Atm object used in the radiative transfer which
                contains many state variables. 
        """
        new_t = atm.tlay + timestep * Htot
        if self.settings['moist_inhibition']:
            Mgas_tmp = self.Mgas
        else:
            Mgas_tmp = np.mean(self.Mgas)
            Mgas_tmp = np.full_like(self.Mgas, Mgas_tmp)
        qarray = turbulent_diffusion_numba(timestep*cp, self.Nlay,
                    atm.play, atm.plev,
                    atm.dmass, new_t/Mgas_tmp,
                    atm.grav, self.Kzz, self.qarray)
        #self.dm_trac = (qarray - self.qarray) * atm.dmass / (timestep*cp)
        self.qarray = qarray


    def dry_convective_adjustment(self, timestep, Htot, atm, verbose=False):
        """Computes convective adjustement. 

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
                (needs to be converted before it is sent to `turbulent diffusion)
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed
            atm: :class:`Atm` object
                The Atm object used in the radiative transfer which
                contains many state variables. 
        """
        new_t = atm.tlay + timestep * Htot
        if self.settings['moist_inhibition']:
            Mgas_tmp = self.Mgas
        else:
            Mgas_tmp = np.mean(self.Mgas)
            Mgas_tmp = np.full_like(self.Mgas, Mgas_tmp)
        H_conv, q_array = dry_convective_adjustment_numba(timestep, self.Nlay, new_t,
                    atm.exner, atm.dmass, self.qarray, Mgas_tmp, verbose=verbose)
        if self.settings['convective_transport']:
            self.qarray=q_array
        return H_conv

    def update_surface_reservoir(self, condensing_pairs_idx = False,
            surf_layer_mass = 0.):
        """Update surface reservoirs of tracers.

        E.g. deals with removing excess condensates from the first layer or
        putting more when everything as been evaporated. 
        """
        if condensing_pairs_idx: # an empty list is False
            qcond_surf_layer = self.settings['qcond_surf_layer']
            for idx_vap, idx_cond in condensing_pairs_idx:
                dm_surf_layer = (qcond_surf_layer - self.qarray[idx_cond, -1]) * surf_layer_mass
                if dm_surf_layer > self.qsurf[idx_cond]: #empties surface reservoir
                    self.qarray[idx_cond, -1] += self.qsurf[idx_cond] / surf_layer_mass
                    self.qsurf[idx_cond] = 0.
                else:  # general case
                    self.qarray[idx_cond, -1] = qcond_surf_layer
                    self.qsurf[idx_cond] -= dm_surf_layer

    def __getitem__(self, key):
        return self.qarray[self.idx[key]]
