import numpy as np

def accz(ffreqs, dirs, wns, z, depth):
    """
    Transfer function for vertical acceleration measurements.
    
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
    
    Kz = np.cosh(z * wns) / np.sinh(depth * wns)
    
    # Include a maximum cutoff for the acceleration response function
    Kz[Kz < 0.1] = 0.1
    
    trm = (ffreqs * ffreqs * Kz)[:, np.newaxis] * np.ones(np.shape(dirs))
    
    return trm


def accs(ffreqs, dirs, wns, z, depth):
    """
    Transfer function for surface acceleration measurements.
    
    This is equivalent to vertical acceleration at the surface (z=depth).
    
    Parameters:
    -----------
    ffreqs : ndarray
        Frequency array
    dirs : ndarray
        Direction array
    wns : ndarray
        Wavenumber array
    z : float
        Depth of measurement (overridden to depth for surface measurement)
    depth : float
        Total water depth
        
    Returns:
    --------
    trm : ndarray
        Transfer function matrix
    """
    
    return accz(ffreqs, dirs, wns, depth, depth)
