import numpy as np

def wavenumber(sigma, h):
    """"
    k = wavenumber(sigma,h)
    
    k is the matrix of same size as sigma and h containing the calculated wave numbers
    
    sigma is the wave frequencies in rad/s
    h is the water depth
    
    sigma and h must be scalars,vectors or matricies of the same dimensions
    
    
    modified from R.Dalrymple's java code
    """
    g = 9.81

    a0 = (sigma * sigma * h) / g
    b1 = 1 / np.tanh(a0 ** 0.75)
    a1 = a0 * (b1 ** 0.666)
    da1 = 1000

    d1 = np.ones(np.shape(h))
    while np.max(d1) == 1:
        d1 = np.abs(da1 / a1) > 0.00000001
        th = np.tanh(a1)
        ch = np.cosh(a1)
        f1 = a0 - (a1 * th)
        f2 = -a1 * (1 / ch) ** 2 - th
        da1 = -f1 / f2
        a1 += da1
    
    k = a1 / h

    return k