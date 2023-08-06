import pytest
import numpy as np
from ase import Atoms

from cogef.potentials import HOcut


def test_hocut():
    atoms = Atoms('H2')
    atoms.calc = HOcut()
    # r - r0 = -1
    assert atoms.get_potential_energy() == pytest.approx(35)
    # r - r0 = 1
    atoms[1].position[1] = 2
    assert atoms.get_potential_energy() == pytest.approx(0)

    # set values
    kwargs = {'De': 2, 'r0': 3, 'kb': 10}
    bmax = np.sqrt(2 * kwargs['De'] / kwargs['kb'])
    atoms.calc = HOcut(**kwargs)

    atoms[1].position[1] = kwargs['r0']
    assert atoms.get_potential_energy() == pytest.approx(-kwargs['De'])

    atoms[1].position[1] = kwargs['r0'] + bmax
    assert atoms.get_potential_energy() == pytest.approx(0)
