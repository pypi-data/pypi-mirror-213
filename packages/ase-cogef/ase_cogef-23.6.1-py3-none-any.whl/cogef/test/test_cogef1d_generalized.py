import pytest
from ase import Atoms
from ase.calculators.emt import EMT
from ase.constraints import FixBondLength

from cogef import COGEF1D


def test_unrelaxed(H3):
    """First [0] image should be relaxed without constraints"""
    image = Atoms('H3', positions=[(0, 0, 0), (0.751, 0, 0), (0, 1., 0)])
    image.calc = EMT()

    cogef1d = COGEF1D(0, 1, fmax=0.05)
    cogef1d.images = [image]
    cogef1d.move(0.1, 1)

    assert len(cogef1d.images) == 2
    assert len(cogef1d.images[0].constraints) == 0
    assert H3.get_distance(1, 2) == pytest.approx(
        cogef1d.images[0].get_distance(1, 2))


def test_restart(H3):

    def initialize(atoms):
        atoms.calc = EMT()
        return atoms

    break_atoms = [0, 1]
    cogef1d = COGEF1D(*break_atoms, initialize=initialize)
    cogef1d.images = [H3]
    d0 = H3.get_distance(*break_atoms)

    dstep = 0.25
    nfirst = 3
    cogef1d.move(dstep, nfirst)
    assert len(cogef1d) == nfirst + 1
    assert (cogef1d.images[-1].get_distance(*break_atoms)
            == pytest.approx(d0 + nfirst * dstep, 1e-6))

    # restart from previously calculated trajectory
    cogef1d = COGEF1D(*break_atoms, initialize=initialize)
    assert len(cogef1d) == nfirst + 1

    nsecond = 2
    cogef1d.move(dstep, nsecond)
    assert len(cogef1d) == nfirst + nsecond + 1
    assert (cogef1d.images[-1].get_distance(*break_atoms)
            == pytest.approx(d0 + (nfirst + nsecond) * dstep, 1e-6))


@pytest.fixture
def cogefH6(H6):
    break_atoms = [0, 5]
    cogef1d = COGEF1D(*break_atoms)
    cogef1d.images = [H6]
    return cogef1d


def test_constraint(cogefH6):
    """Make sure existing constraints are kept"""
    constraint = FixBondLength(1, 2)
    cogefH6.images[0].set_constraint(constraint)

    cogefH6.move(0.2, 1)
    image = cogefH6.images[-1]
    assert len(image.constraints) == 2   # cogef adds one

    hascons = False
    for cons in image.constraints:
        if cons.todict() == constraint.todict():
            hascons = True
    assert hascons


def test_constraint_initialize(cogefH6):
    """Make sure constraints set in initialize work"""
    constraint = FixBondLength(1, 2)

    def initialize(atoms):
        atoms.set_constraint(constraint)
        atoms.calc = EMT()
        return atoms

    # XXX too much couplig XXX
    cogefH6._initialize = initialize
    cogefH6.move(0.2, 1)
    image = cogefH6.images[-1]
    assert len(image.constraints) == 2   # cogef adds one

    hascons = False
    for cons in image.constraints:
        if cons.todict() == constraint.todict():
            hascons = True
    assert hascons


def test_distances_energies_forces(cogefH6):
    """Assure basic functions to exist and give correct result size"""
    cogefH6.move(0.2, 4)
    assert len(cogefH6.get_distances()) == len(cogefH6.images)
    assert len(cogefH6.get_energies()) == len(cogefH6.images)
    assert len(cogefH6.get_forces()) == len(cogefH6.images)
