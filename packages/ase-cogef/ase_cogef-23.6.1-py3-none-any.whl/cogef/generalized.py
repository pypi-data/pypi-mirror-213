from pathlib import Path
import numpy as np
from typing import Union, List
from collections.abc import Iterable

from ase import io, Atoms
from ase.constraints import FixBondLength, FixBondLengths
from ase.parallel import parprint, world
from ase.utils import deprecated, IOContext
from ase.optimize.optimize import Optimizer
from ase.optimize import FIRE

from cogef import COGEF
from cogef.utilities import mkparent


def shift_atoms_mass_weighted(
        atoms: Atoms, i1: int, i2: int, stepsize: float):
    a1 = atoms[i1]
    a2 = atoms[i2]
    nvec12 = a2.position - a1.position
    nvec12 /= np.linalg.norm(nvec12)
    # shift mass weighted
    a1.position -= stepsize * a2.mass / (a1.mass + a2.mass) * nvec12
    a2.position += stepsize * a1.mass / (a1.mass + a2.mass) * nvec12


def pair_extended_name(cls, pair: List[int], value: str = None) -> str:
    if value is None:
        name = str(cls.__class__.__name__).lower()
    else:
        name = str(value)

    # add pull positions as extension if not already there
    ext = '_{0}_{1}'.format(*pair)
    if ext not in name:
        name += ext

    return name


class COGEF1D(COGEF, IOContext):
    def __init__(self, atom1: int, atom2: int, initialize=None,
                 name=None,
                 optimizer: Optimizer = FIRE,
                 fmax: float = 0.1,
                 trajname: str = 'cogef.traj',
                 txt='-',
                 comm=world,
                 optimizer_logfile='-'):
        self.trajname = trajname
        self.txt = self.openfile(txt, comm)

        self.atom1 = atom1
        self.atom2 = atom2
        # XXX remove
        self.constdict = FixBondLength(atom1, atom2).todict()

        self._initialize = initialize
        self.name = name
        self.optimizer = optimizer
        self.fmax = fmax

        # XXX is this needed?
        self.optimizer_logfile = optimizer_logfile
        self.last_intact_bond_image = float("inf")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = pair_extended_name(
            self, [self.atom1, self.atom2], value)

        # name change => remove images
        self._images = []
        self.look_for_images()

    def shift_and_optimize(self, mother, dstep, index):
        """Shift atoms by dstep and optimze

        mother: Atoms
          the Atoms object to be shifted
        dstep: float
          value of the shift
        index:
          index of atoms needed for optimizer trajectory filename

        retruns relaxed atoms
        """
        atoms = mother.copy()

        # file name for optimizer trajectory
        optimizer_traj = (Path(self.name)
                          / 'image{0}.traj'.format(index))

        # check for already existing optimization history
        try:
            atoms = io.read(optimizer_traj)
        except FileNotFoundError:
            mkparent(optimizer_traj)
            atoms = mother.copy()
            self.shift_atoms(atoms, dstep)

        # make sure my constraint is there before initialize
        self.add_my_constraint(atoms)

        atoms = self.initialize(atoms)

        # make sure, my constraint is not accidently removed
        self.add_my_constraint(atoms)

        return self._optimize(atoms)

    def initialize(self, atoms):
        if self._initialize is None:
            atoms.calc = self.images[-1].calc
        else:
            # let the user provided function take care about the image
            atoms = self._initialize(atoms)
        return atoms

    def _optimize(self, atoms):
        opt = self.optimizer(atoms, logfile=self.txt)
        opt.run(fmax=self.fmax)
        return atoms

    def update_trajectory(self, name: str) -> io.Trajectory:
        filename = Path(name)

        if filename.is_file():
            trajectory = io.Trajectory(filename, 'a')
            assert len(trajectory) == len(self.images)
        else:
            mkparent(filename)
            trajectory = io.Trajectory(filename, 'w')
            for image in self.images:
                trajectory.write(image)

        return trajectory

    def move(self, dstep, steps):
        if len(self.images) == 1:
            # make sure first image is relaxed
            self.images[0] = self._optimize(self.images[0])

        trajectory = self.update_trajectory(self.trajname)

        for i in range(steps):
            parprint(self.__class__.__name__, f'step {i + 1}/{steps}',
                     file=self.txt)
            self.images.append(
                self.shift_and_optimize(
                    self.images[-1], dstep=dstep, index=len(self.images)))
            trajectory.write(self.images[-1])

    @deprecated(DeprecationWarning('Please use move'))
    def pull(self, dstep, steps, initialize=None):
        self.move(dstep, steps)

    def __len__(self):
        return len(self.images)

    def shift_atoms(self, atoms: Atoms, stepsize: float) -> None:
        """Shift atoms by stepsize"""
        shift_atoms_mass_weighted(atoms, self.atom1, self.atom2, stepsize)

    def add_my_constraint(self, atoms):
        """make sure my constraint is present"""
        self.remove_my_constraint(atoms)
        atoms.constraints.append(self.get_constraint())

    def remove_my_constraint(self, atoms):
        """make sure my constraint is not present"""
        mydict = self.get_constraint().todict()
        constraints = []
        for i, constraint in enumerate(atoms.constraints):
            if constraint.todict() != mydict:
                constraints.append(constraint)
        atoms.constraints = constraints

    def get_constraint(self):
        # we need to create a new constraint for every image
        return FixBondLength(self.atom1, self.atom2)

    def get_distances(self):
        return np.array([img.get_distance(self.atom1, self.atom2)
                         for img in self.images])

    def get_energies(self):
        return np.array([img.get_potential_energy()
                         for img in self.images])

    def get_forces(self):
        """Return forces due to constraint"""

        def constraint_force(image):
            vec = image[self.atom2].position - image[self.atom1].position
            vec /= np.linalg.norm(vec)
            forces = image.get_forces(apply_constraint=False)
            delta_f = forces[self.atom1] - forces[self.atom2]
            return np.dot(delta_f, vec) / 2.

        return np.array([constraint_force(img)
                         for img in self.images])

    def look_for_images(self):
        """Read images if the Trajectory-file exists already"""
        if Path(self.trajname).exists():
            with io.Trajectory(self.trajname) as traj:
                self.images = [img for img in traj]
            parprint(self.__class__.__name__ + ': read', len(self.images),
                     'images from', self.trajname, file=self.txt)


class Concerted(COGEF1D):
    """COGEF1D for concerted variation of two bonds"""
    def __init__(self, pairs, *args, **kwargs):
        """
        pair1: indices of first bond
        pair2: indices of second bond
        """
        self.pairs = pairs
        COGEF1D.__init__(self, *pairs[0], *args, **kwargs)

    def move(self, dstep: Union[float, Iterable], steps: int):
        """Move pairs by dstep for given number of steps"""
        if isinstance(dstep, Iterable):
            assert len(dstep) == 2  # 2 pairs up to now
        else:
            dstep = [dstep] * 2
        super().move(dstep, steps)

    def shift_atoms(self, atoms: Atoms, stepsize: List[float]):
        for dx, (i1, i2) in zip(stepsize, self.pairs):
            shift_atoms_mass_weighted(atoms, i1, i2, dx)

    def get_constraint(self):
        # we need to create a new constraint for every image
        return FixBondLengths(self.pairs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        name = pair_extended_name(
            self, self.pairs[0], value)
        for pair in self.pairs[1:]:
            name = pair_extended_name(self, pair, name)
        self._name = name

        # name change => remove images
        self._images = []
        self.look_for_images()
