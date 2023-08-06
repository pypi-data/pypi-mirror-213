import numpy as np
from ase.calculators.calculator import Calculator


class HOcut(Calculator):
    implemented_properties = ['energy', 'forces']
    default_parameters = {'kb': 72, 'r0': 1.0, 'De': 1}

    def __init__(self, **kwargs):
        """Cut harmonic oscillator ASE potential

        Parameters:
        -----------

        kb: spring constant, default 72
        r0: equlibrium distance, default 1
        De: dissociation energy, default 1

        The potential is
          V = 0 for r - r0 > sqrt(2 * De / kb)
          V = -De + kb * (r - r0)**2 / 2 else
        """
        self.parameters = {}
        self.parameters.update(self.default_parameters)
        self.parameters.update(**kwargs)
        super().__init__(**kwargs)

    def calculate(self, atoms, *ignored):
        assert len(atoms) == 2
        self.atoms = atoms.copy()

        k = self.parameters['kb']
        De = self.parameters['De']
        r0 = self.parameters['r0']

        bmax = np.sqrt(2 * De / k)

        dist_c = atoms[1].position - atoms[0].position
        r = np.linalg.norm(dist_c)
        if r > 0:
            h_c = dist_c / r
        else:
            h_c = dist_c
        b = r - r0

        if b <= bmax:
            self.energy = - De + k / 2 * b**2
            self.forces = k * b * np.array([h_c, - h_c])
        else:
            self.energy = 0.
            self.forces = np.zeros((2, 3))

        self.results['energy'] = self.energy
        self.results['forces'] = self.forces
