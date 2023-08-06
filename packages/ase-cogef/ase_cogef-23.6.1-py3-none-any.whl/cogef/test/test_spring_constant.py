import pytest

from ase.build import molecule
from ase.calculators.morse import MorsePotential
from ase.optimize import FIRE

from cogef.generalized import COGEF1D
from cogef.spring_constant import quadratic, spring_constant


def test_spring_constant(tmp_path):
    image = molecule('H2')
    image.calc = MorsePotential()
    fmax = 0.01
    FIRE(image, logfile=None).run(fmax=fmax)

    atom1 = 0
    atom2 = 1
    steps = 15
    stepsize = 0.001

    cogef = COGEF1D(atom1, atom2, fmax=fmax, optimizer_logfile=None)
    cogef.images = [image]
    cogef.move(stepsize, steps)

    dl = cogef.get_distances()
    el = cogef.get_energies()
    d0, e0, k0 = spring_constant(dl, el)
    assert k0 == pytest.approx(63.3, 0.1)

    # restricting region leads to larger spring constant
    d0, e0, k1 = spring_constant(dl, el, last=5)
    assert k1 > k0

    # restricting region by distance
    d1, e1, k2 = spring_constant(dl, el, dmax=1.005)
    assert d0 == d1
    assert e0 == e1
    assert k1 == k2


def test_quadratic():
    # y = (x - 1)^2
    x = [-1, 1.5, 2, 3]
    y = [4, 0.25, 1, 4]

    xmin, ymin, a2 = quadratic(x, y, order=3)
    assert xmin == pytest.approx(1)
    assert ymin == pytest.approx(0)
    assert a2 == pytest.approx(1)
