from pathlib import Path
import numpy as np

from ase import Atoms
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.neb import NEBTools

from cogef import COGEF1D
from cogef.neb import apply_neb


def test_H3(H3):
    d0 = 4
    image = Atoms(
        'H4',
        positions=[[-2, 0, 0], [-1, 0, 0], [d0 - 3, 0, 0], [d0 - 2, 0, 0]])
    image.constraints = [FixAtoms(indices=[0, 3])]

    # make sure all tests do the same
    rng = np.random.RandomState(42)

    def initialize(atoms):
        atoms.rattle(stdev=0.01, rng=rng)
        atoms.calc = EMT()
        return atoms

    cogef1d = COGEF1D(1, 2, fmax=0.05, initialize=initialize)
    cogef1d.images = [initialize(image)]
    cogef1d.move(-0.2, 8)
    cgbarrier = NEBTools(cogef1d.images).get_barrier(fit=False)[0]

    images = apply_neb(cogef1d)
    nebbarrier = NEBTools(images).get_barrier(fit=False)[0]
    assert (Path(cogef1d.name) / 'neb.traj').is_file()
    assert (Path(cogef1d.name) / 'neb_restart.traj').is_file()
    print('Barrier cogef:', cgbarrier, ', neb:', nebbarrier)
