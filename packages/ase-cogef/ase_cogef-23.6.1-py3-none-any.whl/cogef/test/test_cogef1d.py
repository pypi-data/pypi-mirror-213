# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Tests for cogef/cogef1d.py and cogef/dissociation.py.

"""
from pathlib import Path
import pytest

from ase import Atoms, io
from ase.optimize import FIRE
from ase.calculators.emt import EMT
from ase.constraints import FixCom

from cogef import Dissociation
from cogef.dissociation.barrier import ElectronicBarrier, GibbsBarrier
from cogef.dissociation.diss_old import Dissociation as Diss_old
from cogef import COGEF1D
from cogef.units import nN


def H3_EMT(fmax):
    """create H3 optimized in EMT"""
    image = Atoms('H3', positions=[(0, 0, 0), (0.751, 0, 0), (0, 1., 0)])
    image.calc = EMT()
    opt = FIRE(image, logfile=None)
    opt.run(fmax=fmax)
    return image


def test_cogef1d():
    fmax = 0.05

    # Class COGEF
    atom1 = 0
    atom2 = 1
    steps = 10
    stepsize = 0.25

    # start from a pre-calculated structure
    fname = 'H3.extxyz'
    H3_EMT(fmax).write(fname)
    images = [io.read(fname)]

    def initialize(image):
        """Initialize the image."""
        image.calc = EMT()
        return image

    name = 'cogef'
    cogef = COGEF1D(atom1, atom2, name=name, initialize=initialize,
                    optimizer=FIRE, fmax=fmax, optimizer_logfile=None)
    cogef.images = images
    cogef.move(stepsize, steps)
    assert len(cogef.images) == 11

    # Pull further without initialize function
    cogef.move(stepsize, steps)
    assert len(cogef.images) == 21
    force1 = cogef.get_maximum_force()

    # Reload previous calculation results
    cogef = COGEF1D(atom1, atom2, name=name)
    force2 = cogef.get_maximum_force()

    assert force1 == force2

    print('Maximum force (electronic part):')
    print(cogef.get_maximum_force(method='use_energies') / nN, ' nN')
    print(cogef.get_maximum_force(method='use_forces') / nN, ' nN')

    # Class Dissociation
    T = 298
    P = 101325.
    loading_rate = 10.
    force_ext = 3.5
    force_min = 3.5
    force_max = 7.
    force_step = 0.02

    electronic_barrier = ElectronicBarrier(cogef)
    gibbs_barrier = GibbsBarrier(
        electronic_barrier, T, P, initialize,
        dirname='image', vib_method='frederiksen')

    pmax, pmin = electronic_barrier.electronic_extreme_values(force_ext)
    energies = electronic_barrier.modified_energies(force_ext)
    assert pmax[1] == energies[pmax[0]]
    assert pmin[1] == energies[pmin[0]]
    # Really a local maximum?
    assert pmax[1] >= energies[pmax[0] + 1]
    assert pmax[1] >= energies[pmax[0] - 1]
    # Really a local minimum?
    assert pmin[1] <= energies[pmin[0] + 1]
    assert pmin[1] <= energies[pmin[0] - 1]

    diss = Dissociation(electronic_barrier)

    f_ext = force_ext
    rate1 = diss.get_rate(f_ext, T, verbose=False)

    f_ext = force_ext
    rate2 = diss.get_rate(f_ext, T, verbose=False)
    assert rate1 == rate2
    print('Rate for f_ext=', f_ext / nN, 'nN:')
    print(str(rate1) + '/s')
    assert rate1 == pytest.approx(3.228420042041586e-13)

    diss = Dissociation(gibbs_barrier)
    # this is needed to avoid failure
    gibbs_barrier.barrier.energy_tolerance = 0.2

    f_rup, f_err = diss.rupture_force_and_uncertainty(
        T, loading_rate, force_max, force_min, force_step)
    print('Rupture force:')
    print(f_rup / nN, 'nN')
    assert f_rup == pytest.approx(4.27618920244618)
    print('Uncertainty:')
    print(f_err / nN, 'nN')
    assert f_err == pytest.approx(0.04)

    # XXX old functionality - do we need that? -----------

    diss = Diss_old(cogef, initialize,
                    dirname='image',
                    vib_method='frederiksen')
    # this is needed to avoid failure
    diss.barrier.energy_tolerance = 0.2

    # Search limits automatically
    factor = 10
    force_min, force_max = diss.get_force_limits(T, P, loading_rate,
                                                 force_step=force_step,
                                                 method='Gibbs',
                                                 factor=factor)
    dpdf, forces = diss.probability_density(T, P, loading_rate, force_max,
                                            force_min, force_step,
                                            method='Gibbs')
    assert dpdf[0] < max(dpdf) / factor
    assert dpdf[-1] < max(dpdf) / factor
    f_rup2 = diss.rupture_force(T, P, loading_rate, force_max, force_min,
                                force_step, method='Gibbs')
    assert round(f_rup, 1) == round(f_rup2, 1)


def test_initialization(tmp_path):
    fmax = 0.05

    # Class COGEF
    atom1 = 0
    atom2 = 1
    steps = 2
    stepsize = 0.25

    # first object
    name = str(tmp_path / 'cogef')
    trajname = 'custom.traj'
    cogef1 = COGEF1D(atom1, atom2, name=name, trajname=trajname,
                     optimizer_logfile=None)

    try:
        cogef1.move(stepsize, steps)
    except IndexError:
        # remove garbage
        Path(cogef1.trajname).unlink()
    else:
        assert 0, 'pull without images -> should fail'

    cogef1.images = [H3_EMT(fmax)]
    cogef1.move(stepsize, steps)
    assert len(cogef1.images) == 3

    # second object based on the results of the first
    def initialize(atoms):
        atoms.calc = EMT()
        return atoms

    cogef2 = COGEF1D(atom1, atom2, name=name, trajname=trajname,
                     optimizer_logfile=None, initialize=initialize)
    assert len(cogef2.images) == 3

    try:
        cogef1.images = [H3_EMT(fmax)]
    except RuntimeError:
        pass
    else:
        assert 0, 'Overwriting of existing images should fail'

    cogef2.move(stepsize, steps)
    assert len(cogef2.images) == 5


def test_trajectory():
    """Test first image in trajectory has energy"""
    image = H3_EMT(0.05)
    image.calc = EMT()
    name = 'tsttraj'
    cogef = COGEF1D(0, 1, name=name)
    cogef.images = [image]
    cogef.move(0.1, 2)

    cogef = COGEF1D(0, 1, name=name)
    print('energy=', cogef.images[0].get_potential_energy())


def test_keep_constraints():
    """Test COGEF to keep constraints"""
    fmax = 0.05
    cogef = COGEF1D(0, 1, optimizer=FIRE,
                    fmax=fmax, optimizer_logfile=None)
    cogef.images = [H3_EMT(fmax)]
    cogef.images[0].set_constraint(FixCom())

    steps = 3
    stepsize = 0.25
    cogef.move(stepsize, steps)

    assert len(cogef.images) == 4

    for image in cogef.images[1:]:
        assert len(image.constraints) == 2
