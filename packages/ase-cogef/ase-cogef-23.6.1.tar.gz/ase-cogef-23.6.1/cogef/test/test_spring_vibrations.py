import pytest
import numpy as np

from ase import Atoms
from ase.calculators.morse import MorsePotential

from cogef.vibrations import SpringVib, SpringInf


class DipoleMorse(MorsePotential):
    """Morse calculator giving a fake dipole"""
    implemented_properties = ['energy', 'forces', 'dipole']

    def calculate(self, atoms=None, properties=['energy'],
                  system_changes=['positions', 'numbers', 'cell',
                                  'pbc', 'charges', 'magmoms']):
        MorsePotential.calculate(self, atoms, properties, system_changes)
        dipole = np.zeros((3,))
        for ia, atom in enumerate(self.atoms):
            for ib in range(ia + 1, len(self.atoms)):
                dipole += self.atoms[ib].position - atom.position
        self.results['dipole'] = dipole


@pytest.mark.xfail
def test_define_and_execute(tmp_path):
    image = Atoms('H2', positions=[(0, 0, 0), (0, 0, 1)])
    image.calc = DipoleMorse()

    svib = SpringVib(image, atom1=0, atom2=1, name=str(tmp_path / 'svib'))
    svib.run()
    svib.read()

    sinf = SpringInf(image, atom1=0, atom2=1, name=str(tmp_path / 'sinf'))
    sinf.run()
    sinf.read()
