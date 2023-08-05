"""
@author: jeremy leconte

A class with some basic functions for all objects with a spectral dimension
"""
import numpy as np
from .cst import PI
from .radiation import Bnu_integral_num, Bnu

class Spectral_object(object):
    """A class with some basic functions for all objects with a spectral dimension
    """

    def __init__(self):
        """Initializes some atributes to None
        """
        self.wns = None
        self.wnedges = None
        self.Nw = None
        self.wn_unit='cm^-1'

    @property
    def wls(self):
        """Returns the wavelength array for the bin centers (in micron)
        """
        if self.wns is not None:
            return 10000./self.wns
        else:
            raise RuntimeError('self.wns should not be None when requesting wls')

    @property
    def wledges(self):
        """Returns the wavelength array for the bin edges (in micron)
        """
        if self.wnedges is not None:
            return 10000./self.wnedges
        else:
            raise RuntimeError('self.wnedges should not be None when requesting wledges')

    @property
    def wnrange(self):
        """Returns the limits of the wavenumber range.

        First tries with wnedges (for Ktables) and then wns (Xtables).
        """
        if self.wnedges is not None:
            return self.wnedges[[0,-1]]
        elif self.wns is not None:
            return self.wns[[0,-1]]
        else:
            raise RuntimeError('self.wns or wnedges should not be None when requesting wnrange')

    @property
    def wlrange(self):
        """Returns the limits of the wavelength range
        """
        if (self.wnedges is None) and (self.wns is None):
            raise RuntimeError('self.wns or wnedges should not be None when requesting wlrange')
        else:
            return np.sort(10000./self.wnrange)

    def _compute_spectral_range(self, wn_range=None, wl_range=None):
        """Converts an unordered spectral range in either wavenumber or wavelength
        in an ordered wavenumber range.

        Parameters
        ----------
            wn_range: list or array of size 2
                Minimum and maximum wavenumber (in cm^-1).
            wl_range: list or array of size 2
                Minimum and maximum wavelength (in micron)
        """
        if wl_range is not None:
            if wn_range is not None:
                print('Cannot specify both wl and wn range!')
                raise RuntimeError()
            else:
                _wn_range=np.sort(10000./np.array(wl_range))
        else:
            if wn_range is not None:
                _wn_range=np.sort(np.array(wn_range))
            else:
                _wn_range=self._wn_range
        return _wn_range

    def select_spectral_range(self, wn_range=None, wl_range=None):
        """Select spectral range, without restricting the data
        (but the spectral axes are modified in place).
        Should use either wn_range OR wl_range, not both.
        
        To be selected, the whole bin must be inside the range.

        Parameters
        ----------
            wn_range: array, np.ndarray
                Wavenumber range in cm^-1.
            wl_range: array, np.ndarray
                Wavelength range in micron.

        Returns
        -------
            tuple:
                iw_min, iw_max the boundary indices of the spectral range
        """
        if (wn_range is None) and (wl_range is None): return None, None
        if wl_range is not None:
            if wn_range is not None:
                raise RuntimeError('Should provide either wn_range or wl_range, not both!')
            _wn_range=np.sort(10000./np.array(wl_range))
        else:
            _wn_range=np.sort(np.array(wn_range))
        iw_min=np.searchsorted(self.wnedges, _wn_range[0], side='left')
        iw_max=np.searchsorted(self.wnedges, _wn_range[1], side='right')
        iw_max-=1
        if iw_max <= iw_min:
            raise RuntimeError(f"Spectral range {wn_range} does not contain any point.")
        self.wnedges=self.wnedges[iw_min:iw_max+1]
        self.wns=self.wns[iw_min:iw_max]
        self.Nw=self.wns.size
        return iw_min, iw_max

    def blackbody(self, Temperature, integral=True):
        """Computes the surface black body flux (in W/m^2/cm^-1) at Temperature.

        Parameters
        ----------
            Temperature; float
                Blackbody temperature
            integral: boolean, optional
                * If true, the black body is integrated within each wavenumber bin.
                * If not, only the central value is used.
                  False is faster and should be ok for small bins,
                  but True is the correct version.
        Returns
        -------
            Spectrum object
                Spectral flux in W/m^2/cm^-1
        """
        if integral:
            try:
                piB = PI*Bnu_integral_num(self.wnedges, Temperature)/np.diff(self.wnedges)
            except:
                raise RuntimeError('You should use integral=False as this spectral object does not have a wnedges atribute.')
        else:
            try:
                piB = PI*Bnu(self.wns[:], Temperature)
            except:
                raise RuntimeError('You should instenciate wns for this spectral object before calling blackbody.')
        return piB
