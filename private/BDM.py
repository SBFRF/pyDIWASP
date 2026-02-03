import warnings
import numpy as np
from scipy.linalg import qr

def BDM(xps, trm, kx, Ss, pidirs, miter, displ):
    """
    Bayesian Directional Method (BDM) for directional wave spectrum estimation.
    
    This method uses a Bayesian approach with model selection via ABIC
    (Akaike's Bayesian Information Criterion) to estimate the directional spectrum.
    
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
        Maximum number of iterations
    displ : int
        Display level (0=none, 1=progress, 2=verbose)
        
    Returns:
    --------
    S : ndarray
        Directional spectrum (ffreqs x ddirs)
    """
    
    nmod = 6
    
    szd = xps.shape[0]
    freqs = xps.shape[2]
    ddirs = trm.shape[2]
    
    ddir = abs(pidirs[1] - pidirs[0])
    pi = 4.0 * np.arctan(1.0)
    
    if np.sum(kx) == 0:
        warnings.warn('BDM method may not work with three quantity measurements')
        print(' ')
    
    if displ < 2:
        warnings.simplefilter('ignore')
    
    Co = np.real(xps)
    Quad = -np.imag(xps)
    
    xpsx = np.zeros_like(Co)
    sigCo = np.zeros_like(Co)
    sigQuad = np.zeros_like(Quad)
    
    for ff in range(freqs):
        xpsx[:, :, ff] = np.outer(np.diag(xps[:, :, ff]), 
                                   np.diag(xps[:, :, ff]).conj())
        sigCo[:, :, ff] = np.sqrt(0.5 * (xpsx[:, :, ff] + Co[:, :, ff]**2 - Quad[:, :, ff]**2))
        sigQuad[:, :, ff] = np.sqrt(0.5 * (xpsx[:, :, ff] - Co[:, :, ff]**2 + Quad[:, :, ff]**2))
    
    phi = np.zeros((szd * szd * 2, freqs))
    H = np.zeros((ddirs, szd * szd * 2, freqs))
    
    for ff in range(freqs):
        index = 0
        for m in range(szd):
            for n in range(m, szd):
                expx = np.exp(-1j * kx[m, n, ff, :ddirs])
                Hh = trm[m, ff, :ddirs]
                Hhs = np.conj(trm[n, ff, :ddirs])
                Htemp = Hh * Hhs * expx
                
                if not np.allclose(Htemp[0], Htemp[1]):
                    phi[index, ff] = np.real(xps[m, n, ff]) / (sigCo[m, n, ff] * Ss[0, ff])
                    H[:ddirs, index, ff] = np.real(Htemp) / sigCo[m, n, ff]
                    index += 1
                    
                    if kx[m, n, 0, 0] + kx[m, n, 0, 1] != 0:
                        phi[index, ff] = np.imag(xps[m, n, ff]) / (sigQuad[m, n, ff] * Ss[0, ff])
                        H[:ddirs, index, ff] = np.imag(Htemp) / sigQuad[m, n, ff]
                        index += 1
    
    M = index
    k = ddirs
    
    # Create the finite difference matrix
    dd = np.diag(np.ones(k)) + np.diag(-2 * np.ones(k-1), -1) + np.diag(np.ones(k-2), -2)
    dd[0, k-2:k] = [1, -2]
    dd[1, k-1] = 1
    
    S = np.zeros((freqs, k))
    
    for ff in range(freqs):
        if displ > 0:
            print('calculating for frequency {} of {}'.format(ff + 1, freqs))
        
        a = H[:k, :M, ff] * ddir
        A = a.T
        B = phi[:M, ff]
        n = 0
        keepgoing = True
        ABIC = []
        xold = None
        
        while keepgoing:
            n += 1
            if displ > 0:
                print('model: {}'.format(n))
            
            if n <= nmod:
                u = 0.5**n
                x = np.log(1 / (2 * pi)) * np.ones(k)
                stddiff = 1
                rlx = 1.0
                count = 0
                TA = None  # Initialize TA
                
                while stddiff > 0.001:
                    count += 1
                    F = np.exp(x)
                    E = np.diag(F)
                    A2 = A @ E
                    B2 = B - A @ F + A @ E @ x
                    
                    Z = np.zeros((M + k, k + 1))
                    Z[:M, :k] = A2
                    Z[M:M+k, :k] = u * dd
                    Z[:M, k] = B2
                    Z[M:M+k, k] = 0
                    
                    # Check for non-finite values in Z
                    if not np.all(np.isfinite(Z)):
                        if rlx > 0.0625:
                            rlx *= 0.5
                            if displ == 2:
                                print('Non-finite values in Z, relaxing computation...factor: {:.4f}'.format(rlx))
                            x = np.log(1 / (2 * pi)) * np.ones(k)
                            count = 0
                            continue
                        else:
                            if displ == 2:
                                warnings.warn('computation fully relaxed with non-finite values..bailing out')
                            if n > 1:
                                keepgoing = False
                            break
                    
                    Q, U = qr(Z)
                    
                    UZ = U
                    TA = UZ[:k, :k]
                    Tb = UZ[:k, k]
                    
                    try:
                        x1 = np.linalg.solve(TA, Tb)
                    except np.linalg.LinAlgError:
                        # If solution fails, use least squares
                        x1, _, _, _ = np.linalg.lstsq(TA, Tb, rcond=None)
                    
                    # Check for non-finite values
                    if not np.all(np.isfinite(x1)):
                        x1 = np.log(1 / (2 * pi)) * np.ones(k)
                    stddiff = np.std(x - x1)
                    x = (1 - rlx) * x + rlx * x1
                    
                    if count > miter or np.sum(np.isfinite(x)) != k:
                        if rlx > 0.0625:
                            rlx *= 0.5
                            if displ == 2:
                                print('relaxing computation...factor: {:.4f}'.format(rlx))
                            if np.sum(np.isfinite(x)) != k:
                                x = np.log(1 / (2 * pi)) * np.ones(k)
                            count = 0
                        else:
                            if displ == 2:
                                warnings.warn('computation fully relaxed..bailing out')
                            if n > 1:
                                keepgoing = False
                            break
                
                # Only compute ABIC if TA was successfully computed
                if TA is not None:
                    sig2 = (np.linalg.norm(A2 @ x - B2)**2 + (u * np.linalg.norm(dd @ x))**2) / M
                    ABIC.append(M * (np.log(2 * pi * sig2) + 1) - k * np.log(u * u) + 
                               np.sum(np.log(np.diag(TA)**2)))
                    
                    if n > 1:
                        if ABIC[-1] > ABIC[-2]:
                            keepgoing = False
                            n -= 1
                    
                    if keepgoing:
                        xold = x.copy()
                    else:
                        if xold is not None:
                            x = xold
                else:
                    # If TA was not computed, we can't continue
                    keepgoing = False
                    if n > 1:
                        n -= 1
                        if xold is not None:
                            x = xold
            else:
                keepgoing = False
        
        if displ == 2:
            print('best: {}'.format(n))
        
        G = np.exp(x)
        SG = G / (np.sum(G) * ddir)
        S[ff, :k] = Ss[0, ff] * SG
    
    warnings.simplefilter('default')
    
    return S
