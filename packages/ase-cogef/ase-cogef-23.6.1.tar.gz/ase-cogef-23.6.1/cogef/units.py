import ase.units as u

# get all globals from ase.units
globals().update(vars(u))

nN = 1e-9 * u.J / u.m
