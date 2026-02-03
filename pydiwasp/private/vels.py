from .velz import velz

def vels(ffreqs, dirs, wns, z, depth):
    """
    Transfer function for surface velocity measurements.
    
    This is equivalent to vertical velocity at the surface (z=depth).
    
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
    
    return velz(ffreqs, dirs, wns, depth, depth)
