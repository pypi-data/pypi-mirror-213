import pytest

from ase import Atoms
from ase.calculators.morse import MorsePotential
from cogef import Dissociation, COGEF1D, COGEF
from cogef.dissociation.barrier import ElectronicBarrier
from cogef.units import kB, _hplanck, _e
from numpy import arange, exp, testing


@pytest.fixture
def cogef1d(H6):
    cogef = COGEF1D(0, 5, txt=None)
    cogef.images = [H6]

    cogef.move(0.2, 5)
    return cogef


@pytest.fixture
def dimer():
    H2 = Atoms('H2', positions=[[0, 0, 0], [1, 0, 0]])
    H2.calc = MorsePotential()

    cogef = COGEF1D(0, 1, txt=None)
    cogef.images = [H2]
    cogef.move(0.02, 20)
    return cogef


def test_modified_energies_H6(cogef1d):
    energies = cogef1d.get_energies()
    barrier = ElectronicBarrier(cogef1d)

    assert (barrier.modified_energies(0., False)
            == pytest.approx(energies, 1.e-8))
    energies -= energies.min()
    assert (barrier.modified_energies(0.) ==
            pytest.approx(energies, 1.e-8))

    # applied force should lower energies
    assert (barrier.modified_energies(0.2)[1:] < energies[1:]).all()


def test_modified_energies_H2(dimer):
    engs = dimer.get_energies()
    barrier = ElectronicBarrier(dimer)

    assert (barrier.modified_energies(0., False)
            == pytest.approx(engs, 1e-8))
    assert (barrier.modified_energies(0.)
            == pytest.approx(engs - engs.min(), 1e-8))

    F = 6 / 5
    dists = dimer.get_distances()
    assert (barrier.modified_energies(F, False)
            == pytest.approx(engs - F * dists))


def test_force_T(cogef1d):
    disn = Dissociation(ElectronicBarrier(cogef1d))

    LOADING_RATE = 1  # [nN/s]
    T = 300  # Temperature [K]

    fstep = 0.1
    method = 'electronic'
    fmin, fmax = disn.get_force_limits(T, LOADING_RATE,
                                       force_step=fstep, method=method)
    force, error = disn.rupture_force_and_uncertainty(T, LOADING_RATE,
                                                      fmax, fmin, fstep)
    # pre-calculated values
    assert force == pytest.approx(1.185196470726945)
    assert error == pytest.approx(0.1)


def not_test_force_Gibbs_T(cogef1d):
    cogef1d.move(0.2, 5)

    def initialize(image):
        image.calc = MorsePotential()
        return image

    disn = Dissociation(cogef1d, initialize=initialize)

    LOADING_RATE = 10  # [nN/s]
    T = 300  # Temperature [K]

    fstep = 0.1
    method = 'Gibbs'
    fmin, fmax = disn.get_force_limits(T, LOADING_RATE,
                                       force_step=fstep, method=method)
    force, error = disn.rupture_force_and_uncertainty(T, LOADING_RATE,
                                                      fmax, fmin, fstep,
                                                      method=method)
    # XXX assert something


def test_probability_density(monkeypatch):
    """
    From (PHYSICAL REVIEW E 74, 031909 (2006)),
    paper by Felix Hanke and Hans Jürgen Kreuzer

    The probability density is given by,
     dp     -A
    ---- = ---- exp(-beta * delV(f)) * P
     df     alpha

     assuming V(f) = Constant, => delV(f) = 0;
     this reduces the exp(-beta * delV(f)) to 1
     the equation reduces to
     dp    -A
    ---- = --- * df
     P     alpha
     integrating from f0 to f, with f0=0 we get
     P = exp (-A/alpha * integral_f0_to_f(df))
     =>
     P = exp(-A/alpha * f)

    """

    def mock_value(force_ext):
        return 0

    T = 300
    # barrier is used instead of gibbs
    h = _hplanck / _e
    A = kB * T / h  # pre-factor value
    alpha = 10 ** 10  # loading rate (consideration of large value
    # to reduce A/alpha value) since there is no contribution from
    # delV(f) and beta term,
    # beta = 1 / (kB * T)

    fmin = 0
    fmax = 1
    fstep = .1

    f = arange(fmin, fmax + fstep / 2., fstep)
    P = exp(-A / alpha * f)
    print(P)
    exp_probability_density = (A / alpha) * P  # negative sign is omitted
    # (even in paper, the plots have positive values for dp/df)

    cogef = COGEF(0, 1)
    disn = Dissociation(ElectronicBarrier(cogef))

    # Mocking electronic_energy_barrier
    monkeypatch.setattr(disn.barrier, 'value',
                        mock_value)

    calc_probability_density, force = disn.probability_density(
        T=T, loading_rate=alpha, force_max=fmax, force_min=fmin,
        force_step=fstep)

    print(exp_probability_density, calc_probability_density)
    testing.assert_allclose(calc_probability_density, exp_probability_density)
