import numpy as np

def velz(ffreqs, dirs, wns, z, depth):
    """
    Transfer function for vertical velocity measurements.
    
    Parameters:
    -----------
    ffreqs : ndarray
        Frequency array
    dirs : ndarray
        Direction array
    wns : ndarray
        Wavenumber array
    z : float
        Depth of measurement (negative downward from surface)
    depth : float
        Total water depth
        
    Returns:
    --------
    trm : ndarray
        Transfer function matrix
    """
    
    Kz = np.sinh(z * wns) / np.sinh(depth * wns)
    
    # Include a maximum cutoff for the velocity response function
    Kz[np.isnan(Kz)] = 1
    Kz[Kz < 0.1] = 0.1
    
    trm = -1j * (ffreqs * Kz)[:, np.newaxis] * np.ones(np.shape(dirs))
    
    return trm
