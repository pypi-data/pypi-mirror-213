import pytest

from cogef.generalized import Concerted


def test_bondlengths(H4):
    dx = 0.1
    pair1 = [0, 1]
    pair2 = [2, 3]
    cogef1d = Concerted([pair1, pair2])
    cogef1d.images = [H4]
    cogef1d.move(dx, 1)

    # check that bodlegths changed as wished
    for pair in [pair1, pair2]:
        d = (cogef1d.images[1].get_distance(*pair)
             - cogef1d.images[0].get_distance(*pair))
        assert d == pytest.approx(dx)

    assert cogef1d.name == 'concerted_{}_{}_{}_{}'.format(*pair1, *pair2)


def test_different_dx(H4):
    dx = [0.1, -0.1]
    pair1 = [0, 1]
    pair2 = [2, 3]
    cogef1d = Concerted([pair1, pair2])
    cogef1d.images = [H4]
    cogef1d.move(dx, 1)

    # check that bodlegths changed as wished
    for delta, pair in zip(dx, [pair1, pair2]):
        d = (cogef1d.images[1].get_distance(*pair)
             - cogef1d.images[0].get_distance(*pair))
        assert d == pytest.approx(delta)
