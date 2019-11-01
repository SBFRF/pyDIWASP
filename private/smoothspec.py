import numpy as np

def smoothspec(S, kernel):
    """
    smooths a directional spectrum using the 
    first dimension is frequency
    kernel is 2*3 matrix with smoothing parameters
    """

    f1 = kernel[0][2]
    f2 = kernel[0][1]
    f3 = kernel[0][0]
    d1 = kernel[1][2]
    d2 = kernel[1][1]
    d3 = kernel[1][0]
    tot = 2 * f1 + 2 * f2 + f3 + 2 * d1 + 2 * d2 + d3

    nf, nd = np.shape(S['S'])

    Sin = S['S']; Sin[np.isnan(Sin)] = 0

    S['S'][2:nf - 2, 2:nd - 2] = (f1 * Sin[:nf - 4, 2:nd - 2] + f2 * 
        Sin[1:nf - 3, 2:nd - 2] + f3 * Sin[2:nf - 2, 2:nd - 2] + f2 * 
        Sin[3:nf - 1, 2:nd - 2] + f1 * Sin[4:nf, 2:nd - 2] + d1 * 
        Sin[2:nf - 2, :nd - 4] + d2 * Sin[2:nf - 2, 1:nd - 3] + d3 * 
        Sin[2:nf - 2, 2:nd - 2] + d2 * Sin[2:nf - 2, 3:nd - 1] + d1 * 
        Sin[2:nf - 2, 4:nd]) / tot
    
    return S