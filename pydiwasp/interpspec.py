import numpy as np
from warnings import warn
from scipy.interpolate import griddata
from .private.hsig import hsig
from .private.spectobasis import spectobasis

def interpspec(SMin, SMout, method='linear'):
    """
    Interpolate directional spectrum onto a different frequency/direction grid.
    
    This function resamples a directional spectrum from one frequency-direction
    grid to another. It uses 2D interpolation in frequency-direction space and
    preserves the total wave energy (significant wave height) to within 2%.
    
    Parameters
    ----------
    SMin : dict
        Input spectral matrix containing the original spectrum. Required fields:
        
        * 'freqs' : ndarray
            Frequency values (Hz or rad/s).
        * 'dirs' : ndarray
            Direction values (radians or degrees).
        * 'S' : ndarray, shape (nfreqs, ndirs)
            Spectral density values to be interpolated.
            
    SMout : dict
        Output spectral matrix defining the target grid. Required fields:
        
        * 'freqs' : ndarray
            Target frequency values (Hz or rad/s).
        * 'dirs' : ndarray
            Target direction values (radians or degrees).
            
        Note: The 'S' field in SMout is ignored if present; it will be
        filled with interpolated values.
        
    method : str, optional
        Interpolation method passed to scipy.interpolate.griddata.
        Options are:
        
        * 'linear' : Linear interpolation (default, recommended)
        * 'nearest' : Nearest-neighbor interpolation
        * 'cubic' : Cubic interpolation (smoother but slower)
        
    Returns
    -------
    SMout : dict
        Output spectral matrix with interpolated spectrum. Contains all input
        SMout fields with 'S' field filled with interpolated spectral density.
    
    Examples
    --------
    Interpolate spectrum to a coarser grid:
    
    >>> from pydiwasp import dirspec, interpspec
    >>> import numpy as np
    >>> 
    >>> # Compute high-resolution spectrum
    >>> SM_hires = {
    ...     'freqs': np.linspace(0.05, 0.5, 100),
    ...     'dirs': np.linspace(-180, 180, 72)
    ... }
    >>> SMout_hires, EPout = dirspec(ID, SM_hires, EP)
    >>> 
    >>> # Define coarser output grid
    >>> SM_coarse = {
    ...     'freqs': np.linspace(0.05, 0.5, 25),
    ...     'dirs': np.linspace(-180, 180, 36)
    ... }
    >>> 
    >>> # Interpolate to coarse grid
    >>> SMout_coarse = interpspec(SMout_hires, SM_coarse, method='linear')
    
    Interpolate to different frequency range:
    
    >>> # Zoom in on specific frequency range
    >>> SM_zoom = {
    ...     'freqs': np.linspace(0.1, 0.2, 50),  # Focus on 0.1-0.2 Hz
    ...     'dirs': np.linspace(-180, 180, 36)
    ... }
    >>> SMout_zoom = interpspec(SMout_hires, SM_zoom)
    
    Notes
    -----
    The interpolation is performed in a transformed coordinate system where
    each point is represented by (f*sin(θ), f*cos(θ)) to properly handle
    the periodic nature of directions and the coupling between frequency
    and direction in wave spectra.
    
    The function automatically checks that the interpolated spectrum preserves
    the significant wave height to within 2%. If the error is larger, a
    warning is issued suggesting that the output grid may be too coarse.
    
    NaN values in the interpolated result (typically at edges) are set to zero.
    
    If the input and output grids are identical, no interpolation is performed
    and a warning is issued.
    
    Warnings
    --------
    If the significant wave height changes by more than 2% during interpolation,
    the function warns that the output grid may be too coarse. Consider using
    a finer frequency or direction resolution in SMout.
    
    See Also
    --------
    dirspec : Compute directional spectrum
    
    References
    ----------
    Original MATLAB version: Copyright (C) 2002 Coastal Oceanography Group,
    CWR, UWA, Perth
    """
    Hs1 = hsig(SMin)

    SMin, facin = spectobasis(SMin)
    SMtmp, facout = spectobasis(SMout)

    s1 = SMin['freqs'][:, np.newaxis] * np.sin(SMin['dirs'])
    c1 = SMin['freqs'][:, np.newaxis] * np.cos(SMin['dirs'])
    s2 = SMtmp['freqs'][:, np.newaxis] * np.sin(SMtmp['dirs'])
    c2 = SMtmp['freqs'][:, np.newaxis] * np.cos(SMtmp['dirs'])

    if np.array_equal(s1, s2) and np.array_equal(c1, c2):
        warn('No interpolation required, skipping')
        Stmp = SMin['S']
    else:
        Stmp = griddata((s1.flatten(), c1.flatten()), SMin['S'].flatten(),
            (s2.flatten(), c2.flatten()), method=method).reshape(s2.shape)

    Stmp[np.isnan(Stmp)] = 0
    SMout['S'] = Stmp / facout

    # check Hsig of mapped spectrum and check sufficiently close to original
    Hs2 = hsig(SMout)
    if (Hs2 - Hs1) / Hs1 > 0.02:
        warn('User defined grid may be too coarse; try increasing' +
            ' resolution of ''SM[\'freqs\']'' or ''SM[\'dirs\']''')

    return SMout