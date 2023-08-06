import pytest
import numpy as np

from cogef.dissociation.tabulated_barrier import Bell, Quadratic, Tabulated
from cogef import Dissociation
from cogef.mpf import MPF
from cogef.units import nN


def test_against_analytic():
    Fmax = 5
    De = 3
    mpf = MPF(De, Fmax)

    T = 300

    # test Bell

    diss = Dissociation(Bell(De, Fmax))
    for alpha_nNs in [0.1, 10]:
        F_ana = Fmax * mpf.bell(T_K=T, alpha_nNs=alpha_nNs)
        F_rup, F_err = diss.rupture_force_and_uncertainty(
            T, alpha_nNs * nN, Fmax, 0.0, 0.001)
        assert F_rup == pytest.approx(F_ana, 0.01)

    # test Quadratic

    diss = Dissociation(Quadratic(De, Fmax))
    for alpha_nNs in [0.1, 10]:
        F_ana = Fmax * mpf.general(T_K=T, alpha_nNs=alpha_nNs)
        F_rup, F_err = diss.rupture_force_and_uncertainty(
            T, alpha_nNs * nN, Fmax, 0.0, 0.001)
        assert F_rup == pytest.approx(F_ana, 0.01)


def test_tabulated():
    """Compare a tabulated barrier against an analytic barrier"""
    Fmax = 5
    De = 3

    T = 300
    alpha_nNs = 1

    bexact = Quadratic(De, Fmax)
    dexact = Dissociation(bexact)

    # create a tabulated barrier from an exact one and compare
    # their most probable forces
    F_f = np.linspace(0, Fmax, 21)
    dH_f = [bexact.value(F) for F in F_f]
    btab = Tabulated(F_f, dH_f)
    dtab = Dissociation(btab)
    for alpha_nNs in [0.1, 10]:
        Fexact, _ = dexact.rupture_force_and_uncertainty(
            T, alpha_nNs * nN, Fmax, 0.0, 0.001)
        Ftab, _ = dtab.rupture_force_and_uncertainty(
            T, alpha_nNs * nN, Fmax, 0.0, 0.001)
        assert Ftab == pytest.approx(Fexact, 1e-3)
