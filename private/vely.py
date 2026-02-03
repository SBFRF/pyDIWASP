import numpy as np

def vely(ffreqs, dirs, wns, z, depth):
    Kz = np.cosh(z * wns) / np.sinh(depth * wns)
    #include a maximum cuttoff for the velocity response function
    Kz[np.isnan(Kz)] = 1
    Kz[Kz < 0.1] = 0.1
    trm = np.transpose((ffreqs * Kz, )) * np.sin(dirs)

    return trm