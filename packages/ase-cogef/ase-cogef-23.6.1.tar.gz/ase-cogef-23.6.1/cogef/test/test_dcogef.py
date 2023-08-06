import numpy as np
import pytest
from pathlib import Path

from ase import io
from ase.build import molecule
from ase.calculators.emt import EMT

from cogef.dcogef import get_angles, rotate_around_axis, splitted_indices
from cogef.dcogef import DCOGEF


biphenyl = molecule('biphenyl')
dihedral = [1, 0, 14, 15]


def test_rotate_biphenyl():
    biphenyl.calc = EMT()
    dcg = DCOGEF([biphenyl], dihedral)

    def initialize(atoms):
        atoms.calc = EMT()
        return atoms

    n = 5
    dcg.pull(2 * np.pi / n, n, initialize=initialize)

    fname = Path(f'dcogef_{dihedral[1]}_{dihedral[2]}') / 'dcogef.traj'
    assert fname.is_file()
    assert len(io.Trajectory(fname)) == n + 1


def test_split_biphenyl():
    indices1, indices2 = splitted_indices(biphenyl, *dihedral[1:3])
    # all indices
    assert len(indices1) + len(indices2) == len(biphenyl)
    # no duplicates
    assert len(set(indices1) & set(indices2)) == 0


def test_angles():
    r = 4
    theta = np.pi / 3

    for phi in [np.pi / 2, - np.pi / 2]:
        ph, th = get_angles(r * np.array([np.cos(phi) * np.sin(theta),
                                          np.sin(phi) * np.sin(theta),
                                          np.cos(theta)]))
        assert th == pytest.approx(theta)
        assert ph == pytest.approx(phi)

    # undefined angles
    ph, th = get_angles(np.zeros(3))
    assert ph == 0
    assert th == 0


def test_rotate():
    axis = np.ones(3)

    r = 3
    vector = r * np.array([1, 0, 0])
    assert np.allclose(rotate_around_axis(axis, vector, np.pi),
                       np.array([-1, 2, 2]))
