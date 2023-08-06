import sys
import numpy as np

from ase.constraints import ExternalForce

from .generalized import COGEF1D


class MinMaxDistanceExternalForce(ExternalForce):
    def __init__(self, a1: int, a2: int, f_ext: float,
                 dmax: float = sys.float_info.max,
                 dmin: float = 0):
        self.dmax = dmax
        self.dmin = dmin
        super().__init__(a1, a2, f_ext)

    def adjust_forces(self, atoms, forces):
        """Adjust forces up to the maximal/minimal distance"""
        dvec = np.subtract.reduce(atoms.positions[self.indices])
        d = np.linalg.norm(dvec)
        uvec = dvec / d
        if d > self.dmax or d < self.dmin:
            # we arrived at maximal/minimal distance
            for ia in self.indices:
                forces[ia] -= np.dot(forces[ia], uvec) * uvec
        else:
            super().adjust_forces(atoms, forces)


class EFEIpair(COGEF1D):
    def scan(self, df: float,
             dmax: float = sys.float_info.max,
             dmin: float = 0,
             maxsteps: int = 1000) -> None:
        """Scan force until maximal/minimal distance dmax/dmin
        is reached."""
        self.dmax = dmax
        self.dmin = dmin

        # get current force from last image
        self.current_force = 0
        mydict = self.get_constraint().todict()
        mydict['kwargs'].pop('f_ext', None)
        for constraint in self.images[-1].constraints:
            constrdict = constraint.todict()
            f_ext = constrdict['kwargs'].pop('f_ext', None)
            if constrdict == mydict:
                self.current_force = f_ext

        for i in range(maxsteps):
            self.move(df, 1)  # XXX rename this?
            d = self.images[-1].get_distance(self.atom1, self.atom2)
            if d > dmax or d < dmin:
                return

    def get_constraint(self):
        return MinMaxDistanceExternalForce(
            self.atom1, self.atom2, self.current_force,
            self.dmax, self.dmin)

    def shift_atoms(self, atoms, df):
        self.remove_my_constraint(atoms)
        self.current_force += df
