import numpy as np


def twoD_Gaussian(xy, amplitude, xo, yo, sigma_x, sigma_y, offset):
    """ Used for fitting the PSF in 2-D. """
    x, y = xy
    xo = float(xo)
    yo = float(yo)
    a = 1 / (2 * sigma_x ** 2)
    c = 1 / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(-(a * ((x - xo) ** 2) + c * ((y - yo) ** 2)))
    return g.ravel()
