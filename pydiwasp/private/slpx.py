import numpy as np

def slpx(ffreqs, dirs, wns, z, depth):
    """
    Transfer function for x-direction surface slope measurements.
    
    Parameters:
    -----------
    ffreqs : ndarray
        Frequency array
    dirs : ndarray
        Direction array
    wns : ndarray
        Wavenumber array
    z : float
        Depth of measurement (not used for surface slope)
    depth : float
        Total water depth (not used for surface slope)
        
    Returns:
    --------
    trm : ndarray
        Transfer function matrix
    """
    
    trm = (1j * wns)[:, np.newaxis] * np.cos(dirs)
    
    return trm
