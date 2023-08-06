import pytest
import numpy as np
from cogef.mpf import MPF

T = 300
alpha = 1
De = 1
Fmax = 1


def test_bell():
    mpf = MPF(De, Fmax)
    assert mpf.bell(T_K=T, alpha_nNs=alpha) == pytest.approx(0.1692, 0.001)


def test_general():
    mpf = MPF(De, Fmax)
    assert mpf.general(T_K=T, alpha_nNs=alpha) == pytest.approx(0.1834, 0.001)


def test__width():
    # applicable for both Bell and General
    mpf = MPF(De, Fmax)
    width = mpf.width_f(T_K=T)
    assert width == pytest.approx(0.0249, 0.001)


def test_bell_pd():
    mpf = MPF(De, Fmax)
    dpdf, f = mpf.bell_pd(T_K=T, alpha_nNs=alpha)
    index = np.argmax(dpdf)
    assert dpdf[-1] == pytest.approx(0.0)
    assert f[-1] == 0.26
    # check with actual expression of MPF (Bell)
    f_check = mpf.bell(T_K=T, alpha_nNs=alpha)
    assert f[index] == pytest.approx(f_check, 0.1)


def test_general_pd():
    mpf = MPF(De, Fmax)
    dpdf, f = mpf.general_pd(T_K=T, alpha_nNs=alpha)
    index = np.argmax(dpdf)
    assert dpdf[-1] == 0.0
    assert f[-1] == 0.3
    # check with actual expression of MPF (General)
    f_check = mpf.general(T_K=T, alpha_nNs=alpha)
    assert f[index] == pytest.approx(f_check, 0.1)


def test_general_verify():
    mpf = MPF(De, Fmax)
    f_general = mpf.general(T_K=T, alpha_nNs=alpha)
    f_exp = mpf.general_verify(relative_f=f_general, T_K=T, alpha_nNs=alpha)
    assert f_exp == pytest.approx(f_general, 1E-7)
