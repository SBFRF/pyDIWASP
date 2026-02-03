import warnings
import numpy as np
from numpy.linalg import inv

def EMLM(xps, trm, kx, Ss, pidirs, miter, displ):
    """
    Extended Maximum Likelihood Method (EMLM) for directional wave spectrum estimation.
    
    This method uses the inverse of the cross-power spectral matrix to estimate
    the directional spectrum.
    
    Parameters:
    -----------
    xps : ndarray
        Cross-power spectra (szd x szd x ffreqs)
    trm : ndarray
        Transfer functions (szd x ffreqs x ddirs)
    kx : ndarray
        Wavenumber array (szd x szd x ffreqs x ddirs)
    Ss : ndarray
        Auto-spectra (szd x ffreqs)
    pidirs : ndarray
        Direction array
    miter : int
        Number of iterations (not used in EMLM)
    displ : int
        Display level (0=none, 1=progress, 2=verbose)
        
    Returns:
    --------
    S : ndarray
        Directional spectrum (ffreqs x ddirs)
    """
    
    szd = xps.shape[0]
    ffreqs = xps.shape[2]
    ddirs = trm.shape[2]
    
    ddir = 8 * np.arctan(1.0) / ddirs
    
    if displ < 2:
        warnings.simplefilter('ignore')
    
    S = np.zeros((ffreqs, ddirs), dtype='complex128')
    
    for ff in range(ffreqs):
        if displ >= 1:
            print('calculating for frequency {} of {}'.format(ff + 1, ffreqs))
        
        invcps = inv(xps[:, :, ff])
        Sftmp = np.zeros(ddirs, dtype='complex128')
        
        for m in range(szd):
            for n in range(szd):
                H = trm[n, ff, :]
                Hs = np.conj(trm[m, ff, :])
                expx = np.exp(1j * kx[m, n, ff, :])
                xtemp = invcps[m, n] * H * Hs * expx
                Sftmp += xtemp
        
        E = 1.0 / Sftmp
        E = E / (ddir * np.sum(E))
        S[ff, :] = Ss[0, ff] * E
    
    warnings.simplefilter('default')
    
    return S
