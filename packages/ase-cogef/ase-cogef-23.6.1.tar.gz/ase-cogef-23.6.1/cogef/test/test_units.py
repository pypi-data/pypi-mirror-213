import ase.units as aseu
from cogef.units import nN
import cogef.units as cogefu


def test_units():
    assert nN == 1e-9 * aseu.J / aseu.m
    assert cogefu.nN == 1e-9 * cogefu.J / cogefu.m
