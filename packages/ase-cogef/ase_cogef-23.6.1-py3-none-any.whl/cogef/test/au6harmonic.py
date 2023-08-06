import numpy as np

from ase import Atoms
from ase.calculators.calculator import Calculator
from ase.optimize import FIRE


class Au6harmonicPotential(Calculator):
    implemented_properties = ['energy', 'forces']
    default_parameters = {'EB': -1.08,  # binding energy of bond
                          'kb': 0.74,   # spring constant of bond
                          'ks': 0.25,   # spring constant of connected spring
                          'b0': 2.0}    # default bond length

    def calculate(self, atoms=None, properties=['energy'],
                  system_changes=['positions']):
        Calculator.calculate(self, atoms, properties, system_changes)
        assert len(self.atoms) == 3

        positions = self.atoms.get_positions()
        energy = 0.0
        forces = np.zeros((len(self.atoms), 3))

        # connected spring between atoms 1 and 2

        b0 = self.parameters.b0
        ks = self.parameters.ks
        vs = positions[1] - positions[2]
        s = np.linalg.norm(vs)

        energy = 0.5 * ks**2 * (s - b0)**2
        f_c = ks * (s - b0) * vs / s
        forces[1] -= f_c
        forces[2] += f_c

        # bond

        kb = self.parameters.kb
        vb = positions[0] - positions[1]
        b = np.linalg.norm(vb)

        energy_b = max(self.parameters.EB + 0.5 * kb**2 * (b - b0)**2, 0)
        if energy_b <= 0:  # bound
            energy += energy_b
            f_c = kb * (b - b0) * vb / b
            forces[0] -= f_c
            forces[1] += f_c

        self.results['energy'] = energy
        self.results['forces'] = forces


def Au6harmonic(fmax):
    """Create linear H4 optimzed with Morse"""
    image = Atoms('H3', positions=[(2 * i, 0, 0) for i in range(3)])
    image.calc = Au6harmonicPotential()
    FIRE(image, logfile=None).run(fmax=fmax)
    return image
