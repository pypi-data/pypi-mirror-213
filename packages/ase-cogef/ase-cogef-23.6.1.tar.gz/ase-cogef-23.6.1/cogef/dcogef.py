# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Similar to class COGEF in cogef.py but changing a dihedral angle instead
of a distance.

"""

from numpy import dot, pi, sin, cos, arccos, sqrt, array
from typing import List, Tuple

from ase import Atoms
from ase.constraints import FixInternals, FixBondLengths, ExternalForce
from ase.constraints import MirrorTorque
from ase.optimize import FIRE
from ase.build.connected import connected_indices

from cogef import COGEF, do_nothing
from cogef.cogef2d import COGEF2D
from cogef.cogef2d.cogef2d import do_nothing2d
from cogef.cogef2d.cogef2in1 import COGEF2IN1


def rotate_around_axis(axis, vector, angle):
    """Rotate vector around axis.

    Parameters
    ----------
    axis: numpy array of three floats
    vecor: numpy array of three floats
    angle: float

    Returns
    -------
    result: numpy array of three floats

    """
    phi, theta = get_angles(axis)
    vector = rotate(vector, -phi)
    vector = rotate(vector, 0., theta)
    vector = rotate(vector, angle)
    vector = rotate(vector, 0., -theta)
    return rotate(vector, phi)


def get_angles(axis):
    """Get phi and theta angles from the axis.

    Parameters
    ----------
    axis: numpy array of three floats

    Returns
    -------
    phi: float
    theta: float

    """
    x = axis[0]
    y = axis[1]
    z = axis[2]
    # Get phi
    d = sqrt(x**2 + y**2)
    if d == 0:
        phi = 0.
    else:
        if y >= 0:
            phi = arccos(x / d)
        else:
            phi = -arccos(x / d)
    # Now set axis in xz-plane, pointing towards positive x
    x, y, z = rotate(axis, -phi)
    # Get theta
    d = sqrt(x**2 + z**2)
    if d == 0:
        theta = 0.
    else:
        theta = arccos(z / d)
    return phi, theta


def rotate(vector, phi, theta=0., psi=0.):
    """Rotate vector by phi, theta and psi angles.

    Parameters
    ----------
    axis: numpy array of three floats
    phi: float
    theta: float
    psi: float

    Returns
    -------
    result: numpy array of three floats

    """
    sinphi = sin(phi)
    cosphi = cos(phi)
    sintheta = sin(theta)
    costheta = cos(theta)
    sinpsi = sin(psi)
    cospsi = cos(psi)
    rot_mat = array([[cosphi * costheta,
                      -sinphi * cospsi - cosphi * sintheta * sinpsi,
                      sinphi * sinpsi - cosphi * sintheta * cospsi],
                     [sinphi * costheta,
                      cosphi * cospsi - sinphi * sintheta * sinpsi,
                      -cosphi * sinpsi - sinphi * sintheta * cospsi],
                     [sintheta, costheta * sinpsi, costheta * cospsi]])
    return dot(rot_mat, vector)


def splitted_indices(atoms: Atoms,
                     index1: int, index2: int,
                     **kwargs) -> Tuple[List[int], List[int]]:
    def connected(i1, i2):
        atoms_copy = atoms.copy()
        atoms_copy[i1].symbol = 'X'
        return connected_indices(atoms_copy, i2, **kwargs)

    return connected(index2, index1), connected(index1, index2)


class DCOGEF(COGEF):
    """COGEF method based on the dihedral angle.

    Parameters
    ----------
    images: str or list of Atoms objects
        Initial trajectory or its filename.
    dihedral_indices: list of four ints
        Four atom indices which define the dihedral angle.
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    fixed_atom_pairs: list of tuples of int
        Fixed Bond lengths which should be considered when angle gets rotated
        and during optimization,
        e.g. *fixed_atom_pairs=[(1, 3), (4, 2), (10, 11)]*.

    """
    def __init__(self, images, dihedral_indices, optimizer=FIRE, fmax=0.1,
                 optimizer_logfile='-',
                 fixed_atom_pairs=None):
        COGEF.__init__(self, dihedral_indices[1], dihedral_indices[2],
                       'dcogef', 'dcogef.traj',
                       optimizer, fmax, optimizer_logfile,
                       fixed_atom_pairs)  # TODO: dihedral_indices[1] -> [3] ?
        self.images = images
        self.dihedral_indices = dihedral_indices

        _, self.rotated_indices = splitted_indices(images[0],
                                                   *dihedral_indices[1:3])

    def pull(self, stepangle, steps, initialize=do_nothing):
        """Obtain the COGEF path by rotating the dihedral angle.
        See also class COGEF.

        """
        return COGEF.pull(self, stepsize=stepangle, steps=steps,
                          initialize=initialize)

    def insert(self, imagenum, steps=1, initialize=do_nothing,
               trajectory='pull.traj'):
        raise NotImplementedError('The method "insert" is not ' +
                                  'implemented, yet.')

    def log(self, step, steps, atoms, logfile):
        """Show the progress. See class COGEF.

        """
        if logfile is None:
            return
        name = self.__class__.__name__
        logfile.write('\n%s: step %d/%d, dihedral angle %15.6f degrees\n\n'
                      % (name, step + 1, steps,
                         atoms.get_dihedral(self.dihedral_indices[0],
                                            self.dihedral_indices[1],
                                            self.dihedral_indices[2],
                                            self.dihedral_indices[3])))

    def shift_atoms(self, atoms: Atoms, stepangle: float):
        pos0 = atoms[self.dihedral_indices[1]].position
        axis = atoms[self.dihedral_indices[2]].position - pos0

        for ia in self.rotated_indices:
            atoms[ia].position = (
                pos0 + rotate_around_axis(
                    axis, atoms[ia].position - pos0, stepangle))

        dihedral_deg = atoms.get_dihedral(*self.dihedral_indices)
        atoms.constaint = FixInternals(
            dihedrals_deg=[[dihedral_deg, self.dihedral_indices]])


class DCOGEF2D(COGEF2D):
    """Like class COGEF2D but the second constraint parameter is a
    dihedral angle instead of a bond length.

    Parameters
    ----------
    pullatompair: tuple of two ints
        Two atom indices where force acts on.
    breakdihedral_indices: tuple of four ints
        Four atom indices which define the dihedral angle.
    images: str or list of Atoms objects
        Initial trajectory of the reactant (minimum) curve or its filename
        (minima with intact bond).
    maximum_images: str or list of Atoms objects (optional)
        Initial trajectory of the (transition) maximum curve or its filename.
    minimum_images: str or list of Atoms objects (optional)
        Initial trajectory of the product minimum curve or its filename
        (minima with broken bond).
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    max_image_number: int
        Maximum number of images for variation of the breaking bond length
    fix_force_for_max_curve: bool
        Defines the additional constraint during variation of the breaking
        bond length. Use *True* to fix the external force, use *False* to
        fix the distance between the atoms where force acts on. These are two
        different procedures in order to find the maximum curve (and the
        product minimum curve).
    placeholdernumber: int
        The number of the reactant image used as placeholder, see property
        *placeholder* in class *COGEF2D*.

    """
    def __init__(self, pullatompair, breakdihedral_indices, images,
                 maximum_images=None, minimum_images=None,
                 optimizer=FIRE, fmax=0.1, optimizer_logfile='-',
                 max_image_number=20,
                 fix_force_for_max_curve=True, placeholdernumber=0):
        COGEF2D.__init__(self, pullatompair, (breakdihedral_indices[0],
                                              breakdihedral_indices[3]),
                         images, maximum_images, minimum_images, optimizer,
                         fmax, optimizer_logfile,
                         max_image_number, fix_force_for_max_curve,
                         placeholdernumber=placeholdernumber)
        self.breakdihedral_indices = breakdihedral_indices

    def initialize(self, image, imagenum, new_opt, get_filename):
        """See class COGEF2D.

        """
        if get_filename:
            return self.initialize2d(image, self.directory, imagenum, new_opt,
                                     get_filename)
        if self.fix_force_for_max_curve:
            if new_opt:
                con1 = ExternalForce(self.pullatompair[0],
                                     self.pullatompair[1], self.f_ext)
                con2 = image.constraints[0]
                assert isinstance(con2, FixInternals)
                image.set_constraint([con1, con2])
            else:
                assert str(image.constraints[0].__class__) == \
                    'ase.constraints.ExternalForce'
                assert isinstance(image.constraints[1], FixInternals)
        return self.initialize2d(image, self.directory, imagenum, new_opt,
                                 get_filename)

    def get_break_cogef(self, images):
        """Get the cogef object for rotating the dihedral angle with indices
        *breakdihedral_indices*. See class COGEF2D.

        """
        return DCOGEF(images, self.breakdihedral_indices,
                      optimizer=self.optimizer, fmax=self.fmax)

    def calc_maximum_curve(self, imageindices, stepangle,
                           energy_tolerance=0.01, initialize2d=do_nothing2d,
                           max_trajectory='pull_max.traj',
                           breakdirectory='pull', breaktrajectory='pull.traj',
                           and_minimum_curve=False,
                           min_trajectory='pull_min.traj', use_image=None,
                           only_minimum_curve=False):
        """Calculate maximum curve and/or product minimum curve by variation
        of the dihedral angle in steps of *stepangle*. See also class COGEF2D.

        """
        COGEF2D.calc_maximum_curve(self, imageindices, stepsize=stepangle,
                                   energy_tolerance=energy_tolerance,
                                   initialize2d=initialize2d,
                                   max_trajectory=max_trajectory,
                                   breakdirectory=breakdirectory,
                                   breaktrajectory=breaktrajectory,
                                   and_minimum_curve=and_minimum_curve,
                                   min_trajectory=min_trajectory,
                                   use_image=use_image,
                                   only_minimum_curve=only_minimum_curve)

    def check_broken_bond_images(self, i, broken_bond_image, stepsize):
        """See class COGEF2D."""
        # TODO: Test should be added.
        pass

    def get_break_distance(self, atoms):
        """Get the dihedral angle.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return atoms.get_dihedral(self.breakdihedral_indices[0],
                                  self.breakdihedral_indices[1],
                                  self.breakdihedral_indices[2],
                                  self.breakdihedral_indices[3]) * pi / 180.

    def get_break_atoms(self):
        """See class COGEF2D.

        """
        pair1 = (self.breakdihedral_indices[0], self.breakdihedral_indices[1])
        pair2 = (self.breakdihedral_indices[2], self.breakdihedral_indices[3])
        return [pair1, pair2]

    def get_break_imagenum(self, angle, angle0, stepangle):
        """Get the next image number associated to a given dihedral angle
        by variation of this angle.

        Parameters
        ----------
        angle: float
            Dihedral angle for which image number is needed.
        angle0: float
            Dihedral angle from the corresponding reactant configuration.
        stepangle: float
            Step of the dihedral angle defining the image numbers.

        Returns
        -------
        result: int

        """
        angle -= angle0
        if angle * stepangle < 0:
            if stepangle > 0:
                angle += 2 * pi
            else:
                angle -= 2 * pi
        return COGEF2D.get_break_imagenum(self, dist=angle, dist0=0,
                                          stepsize=stepangle)


class DCOGEF2IN1(COGEF2IN1):
    """Like class COGEF2IN1 but the maximum curve is found by maximizing
    the energy with respect to a dihedral angle instead of a bond length.

    Parameters
    ----------
    pullatompair: tuple of two ints
        Two atom indices where force acts on.
    breakdihedral_indices: tuple of four ints
        Four atom indices which define the dihedral angle.
    max_angle: float
        Product is assumed to be reached when the dihedral angle is larger
        than this value.
    images: str or list of Atoms objects
        Initial trajectory of the reactant (minimum) curve or its filename
        (minima with intact bond).
    maximum_images: str or list of Atoms objects (optional)
        Initial trajectory of the (transition) maximum curve or its filename.
    minimum_images: str or list of Atoms objects (optional)
        Initial trajectory of the product minimum curve or its filename
        (minima with broken bond).
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    min_angle: float
        Dihedral angle is assumed to be too small for finding a configuration
        of the maximum curve when the angle reaches this value.
    stepangle: float
        The dihedral angle is increased in the first step of the maximum
        and the product minimum curve by *stepangle* to ensure that the
        correct maximum and minimum can be found.
    transition_image_shift: int
        Defines the first image of the transition maximum curve relative to
        the last image of the reactant curve (in negative direction).
    product_image_shift: int
        Defines the first image of the product minimum curve relative to the
        last image of the transition maximum curve.
    placeholdernumber: int
        The number of the reactant image used as placeholder, see property
        *placeholder* in class *COGEF2IN1*.

    """
    def __init__(self, pullatompair, breakdihedral_indices, max_angle,
                 images, maximum_images=None, minimum_images=None,
                 optimizer=FIRE, fmax=0.1, optimizer_logfile='-',
                 min_angle=0.,
                 stepangle=5. * pi / 180., transition_image_shift=0,
                 product_image_shift=0, placeholdernumber=0):
        COGEF2IN1.__init__(self, pullatompair, (breakdihedral_indices[0],
                                                breakdihedral_indices[3]),
                           max_angle, images, maximum_images, minimum_images,
                           optimizer, fmax, optimizer_logfile,
                           min_angle,
                           transition_image_shift, product_image_shift,
                           placeholdernumber=placeholdernumber)
        self.breakdihedral_indices = breakdihedral_indices
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.stepangle = stepangle
        self.distance_type = 'Dihedral angle'

    def get_break_distance(self, atoms):
        """Get the dihedral angle.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return atoms.get_dihedral(self.breakdihedral_indices[0],
                                  self.breakdihedral_indices[1],
                                  self.breakdihedral_indices[2],
                                  self.breakdihedral_indices[3]) * pi / 180.

    def initialize_transition(self, image, imagenum, new_opt, get_filename):
        """Initialization function for images of the transition maximum curve.

        This function adds the MirrorTorque constraint, increases the dihedral
        angle in the first cogef step to ensure that the correct maximum
        will be found and transfers all information plus the name of the curve
        type to self.initialize, see function *do_nothing2in1* in
        cogef2in1.py.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        if get_filename:
            return self.initialize(image, 'transition', imagenum, new_opt,
                                   get_filename)
        if new_opt:
            if (self.start) or (self.always_increase):
                image_copy = image.copy()
                dcogef = DCOGEF([], self.breakdihedral_indices,
                                fixed_atom_pairs=[self.pullatompair])
                dcogef.shift_atoms(image_copy, self.stepangle)
                image.positions = image_copy.positions
            con2 = image.constraints[0]
        else:
            assert str(image.constraints[0].__class__) == \
                'ase.constraints.MirrorTorque'
            con2 = image.constraints[1]
        con1 = MirrorTorque(self.breakdihedral_indices[0],
                            self.breakdihedral_indices[1],
                            self.breakdihedral_indices[2],
                            self.breakdihedral_indices[3],
                            self.max_angle, self.min_angle,
                            fmax=self.fmax)
        assert isinstance(con2, FixBondLengths)
        image.set_constraint([con1, con2])
        return self.initialize(image, 'transition', imagenum, new_opt,
                               get_filename)

    def initialize_product(self, image, imagenum, new_opt, get_filename):
        """Initialization function for images of the product minimum curve.

        This function increases the dihedral angle in the first cogef step to
        ensure that the correct minimum will be found and transfers all
        information plus the name of the curve type to self.initialize,
        see function *do_nothing2in1* in cogef2in1.py.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        if get_filename:
            return self.initialize(image, 'product', imagenum, new_opt,
                                   get_filename)
        if new_opt:
            if (self.start) or (self.always_increase):
                image_copy = image.copy()
                dcogef = DCOGEF([], self.breakdihedral_indices,
                                fixed_atom_pairs=[self.pullatompair])
                dcogef.shift_atoms(image_copy, self.stepangle)
                image.positions = image_copy.positions
        return self.initialize(image, 'product', imagenum, new_opt,
                               get_filename)

    def check_product_distance(self, image):
        """Check whether product minimum image is ok.

        If the dihedral angle is too small, it is not identified as a
        correct product state.

        Parameters
        ----------
        image: Atoms object
            The product image under investigation.

        """
        if self.get_break_distance(image) < self.min_product_distance:
            raise RuntimeError('Dihedral angle is too small. Cannot find ' +
                               'product curve. It may help to increase ' +
                               "'product_image_shift' but you must remove " +
                               'or rename the old product curve data first.')
