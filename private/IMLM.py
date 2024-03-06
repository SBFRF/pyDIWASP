import warnings
import numpy as np
from numpy.linalg import inv

def IMLM(xps, trm, kx, Ss, pidirs, miter, displ):
    
    gamma = 0.1
    beta = 1.0
    alpha = 0.1

    szd = np.shape(xps)[0]
    ffreqs = np.shape(xps)[2]
    ddirs = np.shape(trm)[2]

    ddir = 8 * np.arctan(1) / ddirs

    if displ < 2:
        warnings.simplefilter('ignore')
    
    Htemp = np.empty((ddirs, szd, szd), dtype='complex128')
    iHtemp = np.empty((ddirs, szd, szd), dtype='complex128')
    ixps = np.empty((szd, szd), dtype='complex128')
    S = np.empty((ffreqs, ddirs), dtype='complex128')

    for ff in range(ffreqs):
        if displ >= 1:
            print('calculating for frequency {} of {}'.format(ff + 1, ffreqs))
        
        for m in range(szd):
            for n in range(szd):
                H = trm[n, ff, :]
                Hs = np.conj(trm[m, ff, :])
                expx = np.exp(1j * kx[m, n, ff, :])
                iexpx = np.exp(-1j * kx[m, n, ff, :])
                Htemp[:, m, n] = H * Hs * expx
                iHtemp[:, m, n] = H * Hs * iexpx

        invcps = inv(xps[:, :, ff])
        Sftmp = np.zeros(ddirs, dtype='complex128')
        for m in range(szd):
            for n in range(szd):
                xtemp = invcps[m, n] * Htemp[:, m, n]
                Sftmp += xtemp
        Eo = 1 / Sftmp
        kappa = 1 / (ddir * np.sum(Eo))
        Eo *= kappa
        E = Eo
        T = Eo

        for it in range(miter):
            for m in range(szd):
                for n in range(szd):
                    expG = iHtemp[:, m, n] * E
                    ixps[m, n] = np.sum(expG) * ddir
            invcps = inv(ixps)
            Sftmp = np.zeros(ddirs, dtype='complex128')
            for m in range(szd):
                for n in range(szd):
                    xtemp = invcps[m, n] * Htemp[:, m, n]
                    Sftmp = Sftmp + xtemp
            Told = T
            T = 1 / Sftmp
            
            kappa = 1 / (ddir * np.sum(T))
            T = T * kappa
            
            ei = gamma * ((Eo - T) + alpha * (T - Told))
            E = E + ei
            kappa = 1 / (ddir * np.sum(E))
            E = E * kappa

            
        
        S[ff, :] = Ss[0, ff] * E

        
    
    warnings.simplefilter('default')

    return S