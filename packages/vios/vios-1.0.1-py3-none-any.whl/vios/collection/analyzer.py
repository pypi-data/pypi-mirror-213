import numpy as np
from scipy.optimize import leastsq

__all__ = ['fit_t1']

# region fitting
def fit_t1(x, y, b: float, c: float):
    """fit T1

    ### A*exp(-t/T1)+B

    Args:
        x ([type]): [description]
        y ([type]): [description]
    """
    def fit(p, t):
        A, T1, B = p
        return A*np.exp(-t/T1)+B

    def err(p):
        return y-fit(p, x)

    p0 = [max(y)-min(y), x[-1]/3, min(y)]
    out = leastsq(err, p0, full_output=1)
    p = out[0]
    # print('probability: %g;   T1: %g ns;   Residue: %g' % (p[0], 1.0/p[1], p[2]))
    # deviation = np.sqrt(np.mean((fit(p,x)-y)**2))
    # print('deviation: ', deviation)
    return True, [(x, y), (x, fit(p, x))], [], f"T1: {p[1]}"


def fit_ramsey(x, y, T1: float = 10):
    """Fit Ramsey
    ### A*np.exp(-t/2/T1-np.square(t/Tphi))*np.cos(2*np.pi*delta*t+phi)+B

    Args:
        x ([type]): [description]
        y ([type]): [description]

    Returns:
        [type]: [description]
    """

    def fit(p, t):
        A, Tphi, delta, phi, B = p
        return A*np.exp(-t/2/T1-np.square(t/Tphi))*np.cos(2*np.pi*delta*t+phi)+B

    def err(p):
        return y-fit(p, x)

    p0 = [max(y)-min(y), x[-1]/3, 5, 0, min(y)]
    out = leastsq(err, p0, full_output=1)
    p = out[0]
    return True, [(x, y), (x, fit(p, x))], [], f"Ramsey: {p[1]},'Delta: {p[2]}"


def fit_test(x, y, a: float = 100, sa: set = {1, 2, 3}):
    """Doc Test

    Args:
        x ([type]): [description]
        y ([type]): [description]
        a (float, optional): [description]. Defaults to 100.
        sa (set, optional): [description]. Defaults to {1, 2, 3}.

    Returns:
        [type]: [description]
    """
    print('fit ramsey', x, y, a, sa, type(sa))
    return True, [(x, y), (x, y*np.random.randint(90, 100, 1)[0]/100)], [([x[5]], [y[5]])], 'testing'

# endregion fitting
