from pathlib import Path
import pytest
from ase import Atoms
from ase.utils import workdir
from ase.calculators.morse import MorsePotential
from ase.optimize import FIRE
from ase.calculators.emt import EMT

from cogef import COGEF1D


@pytest.fixture(autouse=True)
def use_tmp_workdir(tmp_path):
    # Pytest can on some systems provide a Path from pathlib2.  Normalize:
    path = Path(str(tmp_path))
    with workdir(path, mkdir=True):
        yield tmp_path
    # We print the path so user can see where test failed, if it failed.
    print(f'Testpath: {path}')


@pytest.fixture
def H3():
    """create H3 optimized in EMT"""
    image = Atoms('H3', positions=[(0, 0, 0), (0.751, 0, 0), (0, 1., 0)])
    image.calc = EMT()
    opt = FIRE(image, logfile=None)
    opt.run(fmax=0.05)
    return image


@pytest.fixture
def H4():
    """Linear H4 with Morse potential"""
    image = Atoms('H4', positions=[(i, 0, 0) for i in range(4)])
    image.calc = MorsePotential()
    return image


@pytest.fixture
def H6():
    """Linear H6 with Morse potential"""
    image = Atoms('H6', positions=[(i, 0, 0) for i in range(6)])
    image.calc = MorsePotential()
    return image


@pytest.fixture
def H4_cogef1d(H4):
    fmax = 0.05
    pull_atoms = [0, 3]

    steps = 20
    stepsize = 0.1

    cogef1d = COGEF1D(*pull_atoms,
                      optimizer=FIRE, fmax=fmax,
                      optimizer_logfile=None)
    cogef1d.images = [H4]

    cogef1d.move(stepsize, steps)

    return cogef1d
