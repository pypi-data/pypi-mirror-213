from unittest.mock import Mock

import numpy as np
import pytest
from numpy import exp
from cogef import Dissociation, COGEF, COGEF1D
from cogef.units import kB, _hplanck, _e
from cogef.dissociation.barrier import ElectronicBarrier
from ase import Atoms
from ase.calculators.morse import MorsePotential


@pytest.fixture
def default_cogef():
    return COGEF(0, 1)


@pytest.fixture
def dimer():
    H2 = Atoms('H2', positions=[[0, 0, 0], [1, 0, 0]])
    H2.calc = MorsePotential()

    cogef = COGEF1D(0, 1, txt=None)
    cogef.images = [H2]
    cogef.move(0.02, 20)
    return cogef


@pytest.fixture
def default_barrier(default_cogef):
    return ElectronicBarrier(default_cogef)


@pytest.fixture
def default_dissociation(default_barrier):
    return Dissociation(default_barrier)


""" Monkey-patching/mocking
Mock the behavior of a function (f1) when another function (f2)
under test calls it
    Eg: We need not consider *get_mean_distance* function when testing
    *set_spring_constant* (which calls it)
Here the function *mock_get_mean_distance* gives value of 10 when called
"""


@pytest.fixture
def mock_get_mean_distance(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get_mean_dis(*args, **kwargs):
        return 10

    monkeypatch.setattr("get", mock_get_mean_dis)


##
@pytest.mark.parametrize("energy_tolerance", [100, 100.00])
def test_energy_tolerance(default_barrier, energy_tolerance):
    default_barrier.energy_tolerance = energy_tolerance
    assert default_barrier.energy_tolerance == energy_tolerance


@pytest.mark.parametrize("energy_tolerance", ["notNumber", complex(1, 2)])
def test_energy_tolerance_nonReal(default_barrier, energy_tolerance):
    with pytest.raises(TypeError, match=".*takes only real.*"):
        default_barrier.energy_tolerance = energy_tolerance


@pytest.mark.parametrize("imagemin", [1, -1])
def test_imagemin(default_barrier, imagemin):
    default_barrier.imagemin = imagemin
    assert default_barrier.imagemin == imagemin


@pytest.mark.parametrize("imagemin", [0.1, "1"])
def test_imagemin_nonInts(default_barrier, imagemin):
    with pytest.raises(TypeError, match=".*takes only integer.*"):
        default_barrier.imagemin = imagemin


@pytest.mark.parametrize("imagemax", [1, -1])
def test_imagemax(default_barrier, imagemax):
    default_barrier.imagemax = imagemax
    assert default_barrier.imagemax == imagemax


@pytest.mark.parametrize("imagemax", [0.1, "1"])
def test_imagemax_nonInts(default_barrier, imagemax):
    with pytest.raises(TypeError, match=".*takes only integer.*"):
        default_barrier.imagemax = imagemax


"""
-----------------------------------------------------------------------------
                    SPRING SECTION
-----------------------------------------------------------------------------
"""

# test for set_spring_constant
SPRING_REF = 40  # spring_ref corresponds to distance
SPRING_CONST = 20
MOCK_SPRING_CONST = 0
MOCK_SPRING_REF = 10  # when spring_ref is 'None',
ENERGY_BARRIER = 10
FORCE_EX = 10
TEMPERATURE = 200


@pytest.mark.parametrize("mock_energies, mock_distances",
                         [(np.zeros(5), np.zeros(5)),
                          (np.zeros(5), np.ones(5)),
                          (np.ones(5), np.zeros(5)),
                          (np.ones(5), np.ones(5))])
def test_modified_energies_no_shift(mock_energies, mock_distances):
    mockCOGEF = Mock()
    mockCOGEF.get_energy_curve.return_value = mock_energies, mock_distances
    barrier = ElectronicBarrier(mockCOGEF)
    expected_energies = (mock_energies - (FORCE_EX * mock_distances))
    actual_energies = barrier.modified_energies(f_ext=FORCE_EX, shift=False)
    assert all(actual_energies == expected_energies)


@pytest.mark.parametrize("mock_energies, mock_distances",
                         [(np.zeros(5), np.zeros(5)),
                          (np.zeros(5), np.ones(5)),
                          (np.ones(5), np.zeros(5)),
                          (np.ones(5), np.ones(5))])
def test_modified_energies_shift(mock_energies, mock_distances):
    mockCOGEF = Mock()
    mockCOGEF.get_energy_curve.return_value = mock_energies, mock_distances
    barrier = ElectronicBarrier(mockCOGEF)
    expected_energies = (mock_energies - (FORCE_EX * mock_distances))
    expected_energies -= min(expected_energies)
    actual_energies = barrier.modified_energies(f_ext=FORCE_EX, shift=True)
    assert all(actual_energies == expected_energies)


@pytest.mark.parametrize("mock_energies, mock_distances",
                         [(np.zeros(5), np.zeros(5)),
                          (np.zeros(5), np.ones(5)),
                          (np.ones(5), np.zeros(5)),
                          (np.ones(5), np.ones(5))])
def test_modified_energies_spring_shift(mock_energies, mock_distances):
    mockCOGEF = Mock()
    mockCOGEF.get_energy_curve.return_value = mock_energies, mock_distances
    barrier = ElectronicBarrier(mockCOGEF)
    barrier.set_spring_constant(spring_constant=SPRING_CONST, T=TEMPERATURE,
                                spring_ref=SPRING_REF)
    del_d = mock_distances - SPRING_REF
    expected_energies = (mock_energies + 1/2 * (SPRING_CONST * del_d ** 2)
                         - FORCE_EX * del_d)
    expected_energies -= min(expected_energies)
    actual_energies = barrier.modified_energies(
        f_ext=FORCE_EX, shift=True)
    assert all(actual_energies == expected_energies)


def test_get_rate(monkeypatch, default_barrier, default_dissociation):
    def mock_value(*args, **kwargs):
        return ENERGY_BARRIER

    monkeypatch.setattr(default_barrier, 'value',
                        mock_value)

    h = _hplanck / _e
    prefactor = kB * TEMPERATURE / h
    exponent = -ENERGY_BARRIER / (kB * TEMPERATURE)
    expected_rate = prefactor * exp(exponent)
    actual_rate = default_dissociation.get_rate(f_ext=FORCE_EX,
                                                T=TEMPERATURE)
    assert actual_rate == expected_rate
