import numpy as np

def velx(ffreqs, dirs, wns, z, depth):
    
    Kz = np.cosh(z * wns) / np.sinh(depth * wns)
    #include a maximum cuttoff for the velocity response function
    Kz[Kz < 0.1] = 0.1
    trm = (ffreqs * Kz)[:, np.newaxis] * np.cos(dirs)

    return trm