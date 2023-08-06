import numpy as np


class Bell:
    def __init__(self, De: float, Fmax: float):
        """Analytic Bell barrier"""
        self.De = De
        self.Fmax = Fmax

    def value(self, F_ext: float) -> float:
        return self.De * (1 - 2 * F_ext / self.Fmax)


class Quadratic:
    def __init__(self, De: float, Fmax: float):
        """Analytic quadratic barrier"""
        self.De = De
        self.Fmax = Fmax

    def value(self, F_ext: float) -> float:
        if F_ext > self.Fmax:
            return 0.0
        return self.De * (1 - F_ext / self.Fmax)**2


class Tabulated:
    def __init__(self, F_f, dH_f):
        """Tabulated barrier

        F_f: list of force values [eV/A]
        dH_f: list of barrier values [eV]
        """
        assert len(F_f) == len(dH_f)
        self.F_f = np.array(F_f)
        self.dH_f = np.array(dH_f)

    def value(self, F_ext: float) -> float:
        return np.interp(F_ext, self.F_f, self.dH_f)
