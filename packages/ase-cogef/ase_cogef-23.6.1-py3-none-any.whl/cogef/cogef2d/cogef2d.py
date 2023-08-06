# -*- coding: utf-8 -*-

# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Similar to class COGEF in module cogef.py but considering two dimensions
of the Born-Oppenheimer surface.

"""
import sys

from ase.constraints import FixBondLength, ExternalForce
from ase.optimize import FIRE
from ase.parallel import parprint, world
from ase.io.trajectory import Trajectory

from cogef import COGEF, do_nothing
from cogef.utilities import mkparent, insubdir
from cogef.minmax import get_first_maximum, get_first_minimum
from cogef.minmax import check_energies


def do_nothing2d(image):
    return image


class COGEF2D(COGEF):
    """COnstraint GEometry to simulate Forces (COGEF) in two dimensions.

    This class can be used to calculate 3S-COGEF paths as explained here:
    O. Brügner, M. Walter, Phys. Rev. Materials 2018, 2, 113603

    Pull two atoms apart or press two atoms together. In addition to class
    COGEF (1S-COGEF), these methods from here can be used to simulate the
    influence of the thermal motion on a given bond (3S-COGEF).
    The first segment of the 3S-COGEF path obtained here (reactant curve)
    is the 1S-COGEF path which can also be obtained from
    class COGEF and contains reactant states in dependence of the external
    force. The second segment of the 3S-COGEF path (maximum curve)
    belongs to the energy curve associated to the transition states of the
    bond breaking reaction in dependence of the force.
    The third segment (product minimum curve) contains product (and
    transition) states in dependence of the force. In general, searching
    transition states on the 3S-COGEF path is more accurate compared to the
    1S-COGEF path as two dimensions of the BO-surface are considered in the
    former. 3S-COGEF also allows to address different bonds for the bond
    breaking reaction in order to compare their acivation energies
    (see class Dissociation2d). Product states which can be obtained here
    (in contrast to class COGEF) can be used to get activation energies for
    the back reaction.

    Parameters
    ----------
    pullatompair: tuple of two ints
        Two atom indices where force acts on.
    breakatompair: tuple of two ints
        Two atom indices associated to the breaking bond.
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
    fix_force: bool
        Defines the additional constraint during variation of the breaking
        bond length. Use *True* to fix the external force, use *False* to
        fix the distance between the atoms where force acts on. These are two
        different procedures in order to find the maximum curve (and the
        product minimum curve).
    placeholdernumber: int
        The number of the reactant image used as placeholder, see property
        *placeholder*.
    """
    def __init__(self, pullatompair, breakatompair,
                 name='cogef2d',
                 maximum_images=None, minimum_images=None,
                 optimizer=FIRE, fmax=0.1, optimizer_logfile='-',
                 max_image_number=20,
                 fix_force=True, placeholdernumber=0):
        self.pullatompair = pullatompair
        COGEF.__init__(self, pullatompair[0], pullatompair[1],
                       name=name,
                       optimizer=optimizer, fmax=fmax,
                       optimizer_logfile=optimizer_logfile)

        self.breakatompair = breakatompair

        self.placeholdernumber = placeholdernumber

        # XXX what is this good for?
        n_images = 0
        if hasattr(self, '_images'):
            n_images = len(self.images)
        self.maximum_images = [None] * n_images
        if maximum_images:
            cogef = COGEF(0, 1)
            cogef.images = maximum_images
            for i, max_image in enumerate(cogef.images):
                # Don't consider placeholder
                if max_image != self.placeholder:
                    self.maximum_images[i] = max_image
        self.minimum_images = [None] * n_images
        if minimum_images:
            cogef = COGEF(0, 1)
            cogef.images = minimum_images
            for i, min_image in enumerate(cogef.images):
                # Don't consider placeholder
                if min_image != self.placeholder:
                    self.minimum_images[i] = min_image

        self.max_image_number = max_image_number
        self.fix_force = fix_force
        self.f_ext = None
        self.last_broken_bond_image = float("inf")

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        super(COGEF2D, self.__class__).images.fset(self, images)
        self.maximum_images = [None] * len(self.images)
        self.minimum_images = [None] * len(self.images)

    @property
    def placeholder(self):
        """Return a configuration standing for an empty image in all
        trajectories except of the reactant curve.

        It may be an image of the reactant curve.

        Returns
        -------
        result: Atoms object

        """
        return self.images[self.placeholdernumber]

    def set_last_broken_bond_image(self, last_broken_bond_image):
        """ Set the index of the last product (broken bond) image.

        From a certain image on, the product minimum trajectory can contain
        images which do not belong anymore to the product of the current but to
        the product of a new transition indicated by energy release.
        In this case, you must set
        the last image number which still belongs to the current
        transition to prevent wrong results.

        Parameters
        ----------
        last_broken_bond_image: int

        """
        self.last_broken_bond_image = last_broken_bond_image

    def pull(self, stepsize, steps, initialize=do_nothing):
        """Obtain the reactant curve. See class COGEF."""
        COGEF.pull(self, stepsize, steps, initialize)
        self.maximum_images += [None] * steps
        self.minimum_images += [None] * steps

    def get_break_cogef(self, images, base_path=None):
        # XXX require base_path once _use_image is cleaned
        """Get the cogef object for pulling the atoms with indices
        *self.breakatompair* apart.

        Parameters
        ----------
        images: str or list of Atoms objects
            Initial trajectory or its filename.

        Returns
        -------
        result: COGEF object

        """
        # XXX remove this once _use_image is cleaned
        if base_path is None:
            base_path = self.name
        cogef = COGEF(self.breakatompair[0], self.breakatompair[1],
                      name=str(base_path / 'cogef'),
                      optimizer=self.optimizer, fmax=self.fmax,
                      optimizer_logfile=self.optimizer_logfile)
        if not len(cogef.images):
            cogef.images = images

        # set constraints
        if self.fix_force:
            constraint = ExternalForce(self.pullatompair[0],
                                       self.pullatompair[1],
                                       self.f_ext)
        else:
            constraint = FixBondLength(self.pullatompair[0],
                                       self.pullatompair[1])
        cogef.constraints = [constraint]
        # and set them immediately
        for img in cogef.images:
            img.set_constraint(cogef.constraints)

        return cogef

    def calc_maximum_curve(self, imageindices, stepsize,
                           energy_tolerance=0.01, initialize=do_nothing2d,
                           max_trajectory='pull_max.traj',
                           breakdirectory='pull',
                           and_minimum_curve=False,
                           min_trajectory='pull_min.traj', use_image=None,
                           only_minimum_curve=False):
        """Calculate maximum curve and/or product minimum curve by variation
        of the breaking bond length.

        The bond lengths are varied until all requested extrema are found or
        the maximum number *self.max_image_number* is reached. Problems in
        finding extrema lead to error messages.

        imageindices: list of int
            The variation of the breaking bond is started at the reactant
            minima with indices *imageindices*.
        stepsize: float
            Step size of bond length steps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2d*.
        max_trajectory: str
            Name of the trajectory file where the images of the maximum curve
            will be saved in the order of the reactant image numbers.
            *self.placeholder* will be used as placeholder if
            not all maximum images are calculated.
        breakdirectory: str
            A directory with name *breakdirectory + _ + 'image index'* will
            be created for each of the indices in *imageindices*.
        and_minimum_curve: bool
            Product minimum curve will also be obtained if it is *True*.
        min_trajectory: str
            Name of the trajectory file where the images of the product
            minimum curve will be saved in the order of the reactant image
            numbers. *self.placeholder* will be used as
            placeholder if not all product minimum images are calculated.
        use_image: bool
            Set *use_image* to an image number for which
            the maximum image was already calculated if you want that this
            maximum image should be used as initial structure for the search
            process of the new maximum images. This can reduce the computing
            time. But it could lead to gaps in *breaktrajectory*.
            *self.placeholder* will be used as placeholder then.
        only_minimum_curve: bool
            No maximum curve will be obtained if it is *True*.

        """
        if only_minimum_curve:
            and_minimum_curve = True
        if (use_image is None) and (only_minimum_curve):
            raise ValueError('If use_image is not set, ' +
                             'only_minimum_curve must be set to False ' +
                             'because maximum must be calculated ' +
                             'first and the minimum later.')

        for i in imageindices:
            assert i >= 0, \
                'Only image numbers larger or equal to zero are allowed.'
            if world.rank == 0:
                sys.stdout.write('\n' + 'Get image ' + str(i))
                if not only_minimum_curve:
                    sys.stdout.write(' maximum')
                    if and_minimum_curve:
                        sys.stdout.write(' and')
                if and_minimum_curve:
                    sys.stdout.write(' product minimum')
                sys.stdout.write('\n')

            # output directory
            if self.fix_force:
                self.f_ext = self.constraint_force(i)
                parprint('F_ext =', self.f_ext)
                output_dir = str(breakdirectory) + '_ff'
            else:
                parprint('d =', self.get_distance(self.images[i]))
                output_dir = str(breakdirectory) + '_fd'
            output_dir = insubdir(str(output_dir)
                                  + '_{0}'.format(i), self.name)
            mkparent(output_dir / 'dummy')

            # cogef1d
            cogef = self.get_break_cogef([self.images[i]], output_dir)

            is_maxs = []
            if not only_minimum_curve:
                # Get maximum
                is_maxs.append(True)
            if and_minimum_curve:
                # Get product/broken-bond minimum
                is_maxs.append(False)

            for is_maximum in is_maxs:
                if use_image:
                    cogef, found_min = self._use_image(cogef, use_image, i,
                                                       stepsize,
                                                       energy_tolerance,
                                                       maximum=is_maximum)
                else:
                    found_min = False

                engs = [img.get_potential_energy() for img in cogef.images]
                for j, img in enumerate(cogef.images):
                    if img == self.placeholder:
                        # Placeholder
                        engs[j] = None

                engs, emax, emin = check_energies(
                    engs, energy_tolerance, i, is_maximum, found_min)

                for j in range(len(cogef.images), self.max_image_number):
                    if (is_maximum) and (emax is not None) or \
                       not is_maximum and (emin is not None):
                        break  # success !

                    # XXX do we need to invoke external initialize?
                    if cogef.pull(stepsize, 1,
                                  initialize) == 'Canceled':
                        break   # XXX, when does this happen?

                    engs.append(cogef.images[-1].get_potential_energy())
                    if is_maximum:
                        emax = get_first_maximum(engs, energy_tolerance)
                    else:
                        emin = get_first_minimum(engs, energy_tolerance)
                else:
                    if (is_maximum) and (emax is None):
                        raise ValueError('Cannot find energy maximum. ' +
                                         'Maximum image number is too ' +
                                         'small or energy_tolerance ' +
                                         'is too large or too small. ' +
                                         'If you want to ' +
                                         'increase energy_tolerance, ' +
                                         'remove ' +
                                         ' first.')
                    if not is_maximum and (emin is None):
                        raise ValueError('Cannot find energy minimum. ' +
                                         'Maximum image number is too small.')

                if is_maximum:
                    # set the maximum image corresponding to the
                    # reactant minimum
                    self.maximum_images[i] = cogef.images[engs.index(emax)]
                else:
                    engs = [img.get_potential_energy()
                            for img in cogef.images]
                    imagenum = engs.index(emin)
                    if imagenum == 0:
                        image = cogef.images[0]
                    else:
                        # XXX
                        image = cogef.images[imagenum]
                        if initialize is not None:
                            initialize(image)
                        self.optimize(image,
                                      trajectory=insubdir('bbm.traj',
                                                          self.name))
                        if self.maximum_images[i] is not None:
                            self.check_broken_bond_images(i, image, stepsize)
                    # set the product minimum image corresponding to the
                    # reactant minimum
                    self.minimum_images[i] = image

            # Save trajectories

            imgtraj = []
            if not only_minimum_curve:
                imgtraj.append((self.maximum_images,
                                insubdir(max_trajectory, self.name)))
            if and_minimum_curve:
                imgtraj.append((self.minimum_images,
                                insubdir(min_trajectory, self.name)))
            for images, trajectory in imgtraj:
                if trajectory is None:
                    continue
                # Trajectory cannot save different constraints for
                # different images, therefore remove the constraint
                images[i].set_constraint()
                traj = Trajectory(trajectory, 'w')
                for img in images:
                    if img:
                        traj.write(img)
                    else:
                        traj.write(self.placeholder)  # Placeholder
                traj.close()

            # Output

            if world.rank == 0:
                sys.stdout.write('\n' + 'Image ' + str(i) + ':\n')
                if not only_minimum_curve:
                    sys.stdout.write('Emax = ' +
                                     str(self.maximum_images[i].
                                         get_potential_energy()) +
                                     ' eV')
                    if self.fix_force:
                        sys.stdout.write(', Emax-F*d = ' + str(emax) + ' eV')
                    sys.stdout.write('\n')
                if and_minimum_curve:
                    sys.stdout.write('Emin = ' +
                                     str(self.minimum_images[i].
                                         get_potential_energy()) +
                                     ' eV')
                    if self.fix_force:
                        sys.stdout.write(', Emin-F*d = ' + str(emin) + ' eV')
                    sys.stdout.write('\n')
                sys.stdout.write('\n')

    def check_broken_bond_images(self, i, broken_bond_image, stepsize):
        """Check whether product/broken-bond minimum image is ok.

        Parameters
        ----------
        i: int
            Image number of the corresponding reactant image.
        broken_bond_image: Atoms object
            The product image under investigation.
        stepsize: float
            Defines the tolerance. Product image is not ok if the breaking
            bond length is smaller than that of the corresponging maximum
            image minus this tolerance.

        """
        maximum_image = self.maximum_images[i]
        if self.get_break_distance(broken_bond_image) < \
           self.get_break_distance(maximum_image) - stepsize:
            raise RuntimeError(
                'Found wrong product/broken-bond image (' + str(i) +
                '). Bond length is smaller than that of the ' +
                'maximum image.')

    def get_break_distance(self, atoms):
        """Get the distance between the atoms of the breaking bond.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return atoms.get_distance(self.breakatompair[0],
                                  self.breakatompair[1])

    def get_break_atoms(self):
        """Get atoms which are involved in the calculation of the
        break-coordinate.

        This method can be modified for classes which inherite by COGEF2D.

        Returns
        -------
        result: list of tuple of two ints
            If there are more than two atoms, write it like this:
            >>> return [(1, 2), (3, 4), (5, 6)]
            if atom indices 1 to 6 are involved.

        """
        return [self.breakatompair]

    def get_break_imagenum(self, dist, dist0, stepsize):
        """Get the next image number associated to a given breaking bond
        length by variation of this bond length.

        Parameters
        ----------
        dist: float
            Bond length for which image number is needed.
        dist0: float
            Bond length from the corresponding reactant configuration.
        stepsize: float
            Step size defining the image numbers.

        Returns
        -------
        result: int

        """
        imagenum = int(round((dist - dist0) / stepsize + 0.5))
        if imagenum < 0:
            imagenum = 0
        return imagenum

    def shift_pull_atoms(self, use_atoms, shift_d):
        """Fix the breaking bond length and pull the atoms apart where
        force acts on.

        Parameters
        ----------
        use_atoms: Atoms object
            The configuration under modification.
        shift_d: float
            Total increase of distance.

        """
        cogef = COGEF([], self.pullatompair[0], self.pullatompair[1],
                      fixed_atom_pairs=self.get_break_atoms())
        cogef.shift_atoms(use_atoms, shift_d)

    def _use_image(self, cogef, use_image_num, get_image_num, stepsize,
                   energy_tolerance, maximum=True):
        """Search ideal start position for finding a certain extremum
        somewhere in the COGEF path for variation of the breaking bond.

        The configuration of this start position is obtained from another
        configuration with different distance between the atoms where the
        force acts on.

        Parameters
        ----------
        cogef: COGEF object
            COGEF path for variation of the breaking bond.
        use_image_num: int
            Image number with respect to the corresponding reactant image
            of the other configuration used in order to obtain the start
            position.
        get_image_num: int
            Image number with respect to the corresponding reactant image
            of the wanted configuration.
        stepsize: float
            Step size of bond length steps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        maximum: bool
            Maximum must be found if it is *True*, otherwise a minimum must be
            found.

        Returns
        -------
        result 1: COGEF object
            Initialized COGEF path for variation of the breaking bond and
            for finding the extremum.
        result 2: bool
            Is *True* if and only if the extremum was already found.

        """
        if not self.fix_force:
            assert abs(use_image_num - get_image_num) == 1
        atoms = self.images[get_image_num]
        dist = self.get_break_distance(atoms)
        pull_dist = self.get_distance(atoms)
        if maximum:
            use_atoms = self.maximum_images[use_image_num].copy()
        else:
            use_atoms = self.minimum_images[use_image_num].copy()
        if use_atoms is None:
            if maximum:
                raise ValueError('Cannot find maximum image with number ' +
                                 str(use_image_num) + '.')
            else:
                raise ValueError('Cannot find minimum image with number ' +
                                 str(use_image_num) + '.')
        use_atoms_dist = self.get_break_distance(use_atoms)
        use_atoms_pull_dist = self.get_distance(use_atoms)
        imagenum = self.get_break_imagenum(use_atoms_dist, dist, stepsize)
        use_dist = dist + imagenum * stepsize
        emaxmin = None
        if (len(cogef.images) <= imagenum) or \
           (cogef.images[imagenum] == self.placeholder):
            # Add *use_atoms* with shifted bond length or add earlier image
            shift = use_dist - use_atoms_dist
            if self.fix_force:
                con = ExternalForce(self.pullatompair[0],
                                    self.pullatompair[1], self.f_ext)
            else:
                shift_d = pull_dist - use_atoms_pull_dist
                self.shift_pull_atoms(use_atoms, shift_d)
                con = None
            use_atoms.set_constraint(con)
            engs = []
            while emaxmin is None:
                if imagenum == 0:
                    if maximum:
                        # Cut all images *i >= 1* to prevent starting
                        # maximum-search behind the minimum
                        cogef = self.get_break_cogef([cogef.images[0]])
                    return cogef, emaxmin is not None
                cogef2 = self.get_break_cogef([use_atoms] * imagenum)
                if not self.fix_force:
                    cogef2.set_fixed_atom_pairs([self.pullatompair])
                cogef2.pull(shift, 1, self.initialize, trajectory=None)
                use_atoms = cogef2.images[imagenum]
                engs.append(use_atoms.get_potential_energy())
                if maximum:
                    emaxmin = get_first_maximum(engs, energy_tolerance)
                else:
                    emaxmin = get_first_minimum(engs, energy_tolerance)
                shift = -stepsize
                imagenum -= 1
            imagenum += 1
            cogef.images[0].set_constraint(con)
            cogef2.images[imagenum].set_constraint(con)
            engs = [cogef.images[0].get_potential_energy(),
                    cogef2.images[imagenum].get_potential_energy()]
            emax = get_first_maximum(engs, energy_tolerance)
            if (maximum) and (emax is not None) and (engs.index(emax) == 0):
                # Set image 0 to a placeholder image to get no problems
                # when searching for the maximum
                images_ini = [self.placeholder] + cogef.images[1:imagenum]
            else:
                images_ini = cogef.images[:imagenum]
            images = images_ini + [self.placeholder] * \
                (imagenum - len(images_ini)) + [cogef2.images[imagenum]]
            cogef = self.get_break_cogef(images)
        else:
            # Image already exists
            if maximum:
                # Cut all images *i > imagenum* to prevent starting
                # maximum-search behind the minimum
                images = cogef.images[:imagenum + 1]
                cogef = self.get_break_cogef(images)
        return cogef, emaxmin is not None

    def get_maximum_energy_curve(self, imagemin=0, imagemax=-1, modulo=1):
        """Return the energy values and associated distances of the
        maximum curve.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        modulo: int
            Set it to a larger value that less images are used, e.g.
            *modulo=2* means that every second image is used.

        Returns
        -------
        result: two list of floats
            Energies and associated distances in the order of the image
            numbers.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.maximum_images[i]
            if not image:
                continue
            energies.append(image.get_potential_energy())
            distances.append(self.get_distance(image))
        return energies, distances

    def get_minimum_energy_curve(self, imagemin=0, imagemax=-1,
                                 only_broken_bond_images=False, modulo=1):
        """Return the energy values and associated distances of the
        product minimum curve. Use method *get_energy_curve* to get the
        reactant minimum curve associated to the intact bond.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        only_broken_bond_images: bool
            *True* means that the given number of the last
            product/broken-bond image defines the upper limit of used images.
        modulo: int
            Set it to a larger value that less images are used, e.g.
            *modulo=2* means that every second image is used.

        Returns
        -------
        result: two list of floats
            Energies and associated distances in the order of the image
            numbers.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        if only_broken_bond_images:
            imagemax = min(imagemax, self.last_broken_bond_image)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.minimum_images[i]
            if not image:
                continue
            energies.append(image.get_potential_energy())
            distances.append(self.get_distance(image))
        return energies, distances
