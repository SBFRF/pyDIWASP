import warnings
import numpy as np

def DFTM(xps, trm, kx, Ss, pidirs, miter, displ):
    """
    Direct Fourier Transform Method (DFTM) for directional wave spectrum estimation.
    
    This is the simplest estimation method that directly computes the Fourier 
    coefficients from the cross-power spectra.
    
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
        Number of iterations (not used in DFTM)
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
        
        nxps = xps[:, :, ff]
        Sftmp = np.zeros(ddirs, dtype='complex128')
        
        for m in range(szd):
            for n in range(szd):
                H = trm[n, ff, :]
                Hs = np.conj(trm[m, ff, :])
                expx = np.exp(1j * kx[m, n, ff, :])
                xtemp = nxps[m, n] * H * Hs * expx
                Sftmp += xtemp
        
        E = Sftmp
        E = E / (ddir * np.sum(E))
        S[ff, :] = Ss[0, ff] * E
    
    warnings.simplefilter('default')
    
    return S
