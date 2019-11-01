import numpy as np

def pres(ffreqs, dirs, wns, z, depth):
    Kz = np.cosh(z * wns) / np.cosh(depth * wns)
    #include a maximum cuttoff for the pressure response function
    Kz[Kz < 0.1] = 0.1
    trm = Kz[:, np.newaxis] * np.ones(np.shape(dirs))

    return trm