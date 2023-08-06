from sys import float_info
import numpy as np


def quadratic(xlist, ylist, order=2):
    """Quadratic fit to a one dimensional function

    Returns: (x0, y0, a2)
      x0: x-value of the minimum
      y0: y-value of the minimum
      a2: second derivative at the minimum
    """
    assert len(xlist) == len(ylist)
    pars = np.polyfit(xlist, ylist, order)
    a2, a1, a0 = pars[-3:]
    x0 = - a1 / 2 / a2
    y0 = a0 + a1 * x0 + a2 * x0**2

    return x0, y0, a2


def spring_constant(distances, energies,
                    dmin=-float_info.max, dmax=float_info.max,
                    first=0, last=None):
    """Obtain the spring constant

    distances: list
    energies: list
    dmin: minimal distance to consider
    dmax: maximal distance to consider
    first: starting index to consider
    last: endig index to consider

    Returns: (x0, y0, k)
      x0: x-value of the minimum
      y0: y-value of the minimum
      k: spring constant
    """
    x = distances[first:last]
    y = energies[first:last]
    select = np.where((x >= dmin) & (x <= dmax))
    d0, e0, a2 = quadratic(x[select], y[select])

    return d0, e0, 2 * a2
