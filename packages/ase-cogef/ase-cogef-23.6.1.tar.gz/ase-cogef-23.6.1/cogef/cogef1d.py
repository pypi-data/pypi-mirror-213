"""Module for simulating forces with the COGEF
(COnstrained Geometries simulate External Force) method, where
the molecular geometry is relaxed with fixed bond length for each separation
of defined atoms (Beyer, M. K. J. Chem. Phys. 2000, 112, 7307).

"""
from pathlib import Path
import numpy as np
from numpy import array, polyfit
import matplotlib.pyplot as plt

from ase.constraints import dict2constraint, FixBondLength
from ase.optimize import FIRE
from ase import Atoms, io
from ase.io.trajectory import Trajectory
from ase.parallel import parprint
from ase.calculators.calculator import PropertyNotImplementedError
from ase.io.formats import UnknownFileTypeError

from cogef.utilities import mkparent


# XXX this example seems to be outdated
def do_nothing(image: Atoms) -> Atoms:
    return image


class COGEF(object):
    """COnstraint GEometry to simulate Forces (COGEF).

    Pull two atoms apart or press two atoms together by applying the COGEF
    method.

    Beyer, M. K. J. Chem. Phys. 112 (2000) 7307

    Parameters
    ----------
    atom1: int
        First atom index where force acts on.
    atom2: int
        Second atom index where force acts on.
    name: str
        Name used to store all necessary files.
        The name is formatted as name.format(atom1, atom2).
        It is currently used as a directory name.
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    fixed_atom_pairs: list of tuples of int
        Fixed Bond lengths which should be considered when atoms gets shifted
        and during optimization,
        e.g. *fixed_atom_pairs=[(1, 3), (4, 2), (10, 11)]*.

    """
    def __init__(self, atom1, atom2,
                 name=None, trajname='cogef.traj',
                 optimizer=FIRE, fmax=0.1,
                 optimizer_logfile='-',
                 fixed_atom_pairs=None):
        self.atom1 = atom1
        self.atom2 = atom2
        self.constdict = FixBondLength(atom1, atom2).todict()

        self.trajname = trajname
        self.name = name

        self.optimizer = optimizer
        self.fmax = fmax
        self.optimizer_logfile = optimizer_logfile

        self.set_fixed_atom_pairs(fixed_atom_pairs)

        self.last_intact_bond_image = float("inf")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = str(self.__class__.__name__).lower()
        else:
            self._name = str(value)

        # add pull positions as extension if not already there
        ext = '_{0}_{1}'.format(self.atom1, self.atom2)
        if ext not in self._name:
            self._name += ext

        # name change => remove images
        self._images = []
        self.look_for_images()

    @property
    def trajname(self):
        return Path(self._name) / self._trajname

    @trajname.setter
    def trajname(self, value):
        self._trajname = value

    def look_for_images(self):
        """Check whether there are images already based on the name"""
        try:
            self.images = io.Trajectory(self.trajname)
            parprint(self.__class__.__name__ + ': read', len(self.images),
                     'images from', self.trajname)
        except FileNotFoundError:
            pass

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        """Set images savely"""
        if len(self._images):
            raise RuntimeError(
                'There are images already. Try to remove ' +
                str(self.trajname))
        self._images = list(images)
        # require all energies to be there
        for image in self._images:
            image.get_potential_energy()

    def set_last_intact_bond_image(self, last_intact_bond_image):
        """Set the index of the last image with intact bond.

        From a certain image, on the COGEF trajectory can contain
        broken-bond images. You can set the last image number for which
        the bond is still intact to prevent error messages.

        Parameters
        ----------
        last_intact_bond_image: int

        """
        self.last_intact_bond_image = last_intact_bond_image

    def set_fixed_atom_pairs(self, pairs=None):
        """Define additional bond length constraints.

        Use this method if there are additional atom pairs whose bond
        length must be fixed during the complete pulling process.

        Parameters
        ----------
        pairs: list of tuples of int
            E.g. *pairs=[(1, 3), (4, 2), (10, 11)]*.

        """
        self.constraints = []
        if pairs:
            # At least one atom of the two atoms (self.atom1, self.atom2) must
            # not be part of a fixed atom pair
            atom1in = False
            atom2in = False
            for pair in pairs:
                if self.atom1 in pair:
                    atom1in = True
                if self.atom2 in pair:
                    atom2in = True
                self.constraints.append(FixBondLength(pair[0], pair[1]))
            assert not (atom1in) or not (atom2in)
        self.fixed_atom_pairs = pairs

    def insert(self, imagenum, steps=1, initialize=do_nothing,
               trajectory='pull.traj'):
        """Insert images.

        Parameters
        ----------
        imagenum: int
            Insert between *imagenum* and *imagenum + 1*
        steps: int
            Number of images inserted.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        image1 = self.images[imagenum]
        image2 = self.images[imagenum + 1]
        dist1 = self.get_distance(image1)
        dist2 = self.get_distance(image2)
        stepsize = (dist2 - dist1) / (steps + 1)
        return self._pull(imagenum, stepsize, steps, initialize, trajectory)

    def pull(self, stepsize, steps, initialize=None):
        """Pull or press atoms with numbers *self.atom1* and *self.atom2*.

        Parameters
        ----------
        stepsize: float
            Step size is positive for pulling and negative for pressing.
        steps: int
            Number of steps.
        initialize: function or None
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        # Use last image
        imagenum = len(self.images) - 1
        return self._pull(imagenum, stepsize, steps, initialize)

    def _pull(self, imagenum, stepsize, steps, initialize,
              finalize=do_nothing):
        """Pull or press atoms with numbers *self.atom1* and *self.atom2*.

        Parameters
        ----------
        imagenum: int
            Image number used to continue pulling or pressing.
        stepsize: float
            Step size is positive for pulling and negative for pressing.
        steps: int
            Number of steps.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.
        finalize: function
            Function which is executed after the optimization of each image.
            See function *do_nothing2*.
       """
        filename = Path(self.trajname)
        if filename.is_file():
            trajectory = Trajectory(filename, 'a')
            assert len(trajectory) == len(self.images)
        else:
            mkparent(filename)
            trajectory = Trajectory(filename, 'w')
            for image in self.images:
                trajectory.write(image)

        for step in range(steps):
            imagenum += 1

            # file name for optimizer trajectory
            optimizer_traj = (Path(self.name)
                              / 'image{0}.traj'.format(imagenum))

            # check for already existing optimization history
            try:
                image = io.read(optimizer_traj)
            except FileNotFoundError:
                mkparent(optimizer_traj)
                image = self.images[imagenum - 1].copy()
                self.shift_atoms(image, stepsize)

            self.images.insert(imagenum, image)

            if initialize is None:
                self.images[imagenum].calc = self.images[imagenum - 1].calc
            else:
                # let the user provided function take care about the image
                self.images[imagenum] = initialize(image)

            self.optimize(self.images[imagenum], optimizer_traj, step, steps)

            # Save the images
            trajectory.write(self.images[imagenum])

    def optimize(self, image, trajectory, step=None, steps=None):
        """Optimize a single image"""
        opt = self.optimizer(image, trajectory=str(trajectory),
                             logfile=self.optimizer_logfile)
        if step is not None:
            self.log(step, steps, image, opt.logfile)
        opt.run(fmax=self.fmax)

    # XXX keep for cogef2d
    def oldpull(self, stepsize, steps, initialize=do_nothing,
                trajectory='oldpull.traj'):
        imagenum = len(self.images) - 1
        return self._oldpull(imagenum, stepsize, steps, initialize, trajectory)

    # XXX keep for cogef2d
    def _oldpull(self, imagenum, stepsize, steps, initialize=do_nothing,
                 trajectory='pull.traj', finalize=do_nothing):
        """Pull or press atoms with numbers *self.atom1* and *self.atom2*.

        Parameters
        ----------
        imagenum: int
            Image number used to continue pulling or pressing.
        stepsize: float
            Step size is positive for pulling and negative for pressing.
        steps: int
            Number of steps.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.
        finalize: function
            Function which is executed after the optimization of each image.
            See function *do_nothing2*.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        import os
        from ase.parallel import world

        optimizer_traj = None
        for step in range(steps):
            image = self.images[imagenum].copy()
            imagenum += 1
            self.images.insert(imagenum, image)
            d1, d2 = self.shift_atoms(image, stepsize)
            world.barrier()

            try:
                # this is for COGEF2D
                optimizer_traj = initialize(image, imagenum, new_opt=True,
                                            get_filename=True,
                                            atom1=self.atom1,
                                            atom2=self.atom2, d1=d1, d2=d2)
            except TypeError:
                optimizer_traj = initialize(image, imagenum, new_opt=True,
                                            get_filename=True)

            # XXX do not mix filenames with messages
            if optimizer_traj == 'Finished':
                del self.images[imagenum]
                break

            mkparent(optimizer_traj)

            optimizer_traj_origin = optimizer_traj
            # XXX do not mix filenames with messages
            if (isinstance(optimizer_traj, str)
                    and optimizer_traj.startswith('new forces:')):
                optimizer_traj = optimizer_traj[len('new forces:'):]
                new_forces = True
            else:
                new_forces = False
            bak = False
            converged = False
            if (optimizer_traj) and (os.path.isfile(optimizer_traj)):
                # *optimizer_traj* already exists and will be further
                # optimized
                further_opt = True
                try:
                    # Do not change image to an *Atoms* object if image
                    # is no *Atoms* object
                    image.read(optimizer_traj)
                except AttributeError:
                    try:
                        # *Atoms* object has no attribute *read*
                        image = io.read(optimizer_traj)
                    except UnknownFileTypeError:
                        # Empty file?
                        further_opt = False
                except UnknownFileTypeError:
                    # Empty file?
                    further_opt = False
                if further_opt:
                    self.images[imagenum] = image
                    world.barrier()
                    if not (new_forces):
                        opt = self.optimizer(image)
                        opt.fmax = self.fmax
                        converged = opt.converged()
                    if not (converged):
                        # The return value of *initialize* should only depend
                        # on *imagenum* and not on *image*
                        try:
                            assert optimizer_traj_origin == \
                                initialize(image, imagenum, new_opt=False,
                                           get_filename=True,
                                           atom1=self.atom1, atom2=self.atom2,
                                           d1=0, d2=0)
                        except TypeError:
                            assert optimizer_traj_origin == \
                                initialize(image, imagenum, new_opt=False,
                                           get_filename=True)
                        if world.rank == 0:
                            os.rename(optimizer_traj, optimizer_traj + '.bak')
                        bak = True
            else:
                further_opt = False

            if not (converged):
                # Now it is clear that the optimization must start
                # therefore initialize the image with *get_filename=False*
                try:
                    initialize(image, imagenum, new_opt=not (further_opt),
                               get_filename=False, atom1=self.atom1,
                               atom2=self.atom2, d1=d1, d2=d2)
                except TypeError:
                    initialize(image, imagenum, new_opt=not (further_opt),
                               get_filename=False)
                world.barrier()

                opt = self.optimizer(image, trajectory=str(optimizer_traj),
                                     logfile=self.optimizer_logfile)
                self.log(step, steps, image, opt.logfile)
                opt.run(fmax=self.fmax)
                if (bak) and (world.rank == 0):
                    traj = Trajectory(optimizer_traj)
                    if (len(traj) == 1) and not (new_forces):
                        # Has not to be further optimized, so take old
                        # optimizer trajectory
                        os.rename(optimizer_traj + '.bak', optimizer_traj)
            finalize(image)
            if trajectory is not None:
                # Save the images
                self.oldwrite(trajectory)
        if optimizer_traj == 'Finished':
            return 'Canceled'

    def oldwrite(self, filename):
        """Save the images.

        Parameters
        ----------
        filename: str

        """
        mkparent(filename)

        traj = Trajectory(filename, 'w')
        for image in self.images:
            traj.write(image)
        traj.close()

    def log(self, step, steps, atoms, logfile):
        """Show the progress.

        Parameters
        ----------
        step: int
        steps: int
        atoms: Atoms object
        logfile: file object

        """
        if logfile is None:
            return
        name = self.__class__.__name__
        logfile.write('\n%s: step %d/%d, distance %15.6f\n\n'
                      % (name, step + 1, steps, self.get_distance(atoms)))

    def get_distance(self, atoms):
        """Get the distance between the pulling positions.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return np.linalg.norm(self.get_pulling_vector(atoms))

    def get_pulling_vector(self, atoms):
        """Get the relative position of the pulling positions.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: numpy array of float

        """
        return atoms[self.atom2].position - atoms[self.atom1].position

    def shift_atoms(self, atoms, stepsize):
        """Increase the distance between two atoms along der connection line
        and set constraints.

        The indices are defined by *self.atom1* and *self.atom2*. The
        the center of mass will not be changed if possible and a constraint
        is added for fixing this bond length and these defined by
        *self.fixed_atom_pairs*.

        Parameters
        ----------
        atoms: Atoms object
            Configuration used for modification.
        stepsize: float
            Total increase of distance between *self.atom1* and *self.atom2*.
            Set *stepsize* to *None* in order to only fix bond defined in
            *self.fixed_atom_pairs*.

        Returns
        -------
        result: tuple of two floats or tuple of two numpy arrays
            The shift vectors of both atoms.

        """
        vec = self.get_pulling_vector(atoms)
        vec /= np.linalg.norm(vec)
        mass1 = atoms[self.atom1].mass
        mass2 = atoms[self.atom2].mass
        value1 = mass2 / (mass1 + mass2) * stepsize
        value2 = mass1 / (mass1 + mass2) * stepsize

        if self.fixed_atom_pairs:
            atom1in = False
            atom2in = False
            for pair in self.fixed_atom_pairs:
                if self.atom1 in pair:
                    atom1in = True
                if self.atom2 in pair:
                    atom2in = True
            if atom1in:
                value2 = value1 + value2
                value1 = 0
            elif atom2in:
                value1 = value1 + value2
                value2 = 0

        atoms[self.atom1].position -= value1 * vec
        atoms[self.atom2].position += value2 * vec

        # we need to add a new constraint in order to
        # update new postions
        constraint = dict2constraint(self.constdict)
        constraints = []
        for const in atoms.constraints:
            if const.todict() != self.constdict:
                constraints.append(const)
        constraints.append(constraint)
        atoms.set_constraint(constraints)

        return -value1 * vec, value2 * vec

    def keep_images(self, imagenum):
        """Remove some images.

        Parameters
        ----------
        imagenum: int
            Keep only the images up to image number *imagenum*.
            If *imagenum* is zero, take only the zeroth image.

        """
        images = []
        for i, image in enumerate(self.images):
            if i > imagenum:
                break
            images.append(image)
        self.images = images

    def delete_image(self, imagenum):
        """Delete an image.

        Parameters
        ----------
        imagenum: int
             Image number of the image which will be deleted.

        """
        del self.images[imagenum]

    def get_maximum_force(self, method='use_energies', imagemin=0,
                          imagemax=-1, atoms1=None, atoms2=None):
        """Return the maximum force on the COGEF path.

        This is the maximum force acting between atoms with indices
        *self.atom1* and *self.atom2*.

        Parameters
        ----------
        See method *get_force_curve*.

        Returns
        -------
        result: float

        """
        return max(self.get_force_curve(method, imagemin, imagemax,
                                        atoms1=atoms1, atoms2=atoms2,
                                        only_intact_bond_images=True)[0])

    def get_energy_curve(self, imagemin=0, imagemax=-1,
                         only_intact_bond_images=False,
                         modulo=1):
        """Return the energy values and associated distances.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.
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
        if only_intact_bond_images:
            imagemax = min(imagemax, self.last_intact_bond_image)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.images[i]
            energies.append(image.get_potential_energy(
                apply_constraint=False))
            distances.append(self.get_distance(image))
        return np.array(energies), np.array(distances)

    def get_force_curve(self, method='use_energies', imagemin=0, imagemax=-1,
                        atoms1=None, atoms2=None,
                        only_intact_bond_images=False, modulo=1):
        """Return the constraint forces and associated distances.

        Parameters
        ----------
        method: str
            Use 'use_energies' to obtain constraint forces from energies by
            the finit-differences method. Use 'use_forces' to obtain
            constraint forces directly from forces.
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        atoms1: list of int (optional)
            Indices of atoms on the one side whose forces are used for the
            calculation of the constraint force. *self.atom1* is always
            included, additional atoms may be added to cancel forces which
            are zero only for a perfect structure optimization.
        atoms2: list of int (optional)
            Indices of atoms on the other side whose forces are used for the
            calculation of the constraint force. *self.atom2* is always
            included.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.
        modulo: int
            Set it to a larger value that less images are used, e.g. modulo=2
            means that every second image is used.

        Returns
        -------
        result: two list of floats
            Constraint forces and associated distances in the order of the
            image numbers. Returned distances also depend on the method.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        if only_intact_bond_images:
            imagemax = min(imagemax, self.last_intact_bond_image)
        if method == 'use_energies':
            energies, distances = self.get_energy_curve(
                imagemin, imagemax, only_intact_bond_images, modulo=modulo)
            forces = []
            fd_distances = []
            for i in range(len(energies) - 2):
                forces.append((energies[i + 2] - energies[i]) /
                              (distances[i + 2] - distances[i]))
                fd_distances.append((distances[i + 2] + distances[i]) / 2.)
            return np.array(forces), np.array(fd_distances)
        elif method == 'use_forces':
            forces = []
            distances = []
            for i in range(imagemin, imagemax + 1):
                if i % modulo != 0:
                    continue
                image = self.images[i]
                forces.append(self.constraint_force(i, atoms1, atoms2))
                distances.append(self.get_distance(image))
            return np.array(forces), np.array(distances)
        else:
            raise ValueError

    def constraint_force(self, imagenum, atoms1=None, atoms2=None):
        """Calculate the constraint force.

        Parameters
        ----------
        imagenum: int
            Image number of image used.
        atoms1: list of int (optional)
            Indices of atoms on the one side whose forces are used for the
            calculation of the constraint force. *self.atom1* is always
            included, additional atoms may be added to cancel forces which
            are zero only for a perfect structure optimization.
        atoms2: list of int (optional)
            Indices of atoms on the other side whose forces are used for the
            calculation of the constraint force. *self.atom2* is always
            included.

        Returns
        -------
        result: float
            Constraint force. Positive sign means attraction.

        """
        if atoms1:
            if self.atom1 not in atoms1:
                atoms1.append(self.atom1)
        else:
            atoms1 = [self.atom1]
        if atoms2:
            if self.atom2 not in atoms2:
                atoms2.append(self.atom2)
        else:
            atoms2 = [self.atom2]
        image = self.images[imagenum]
        # Do not consider constraints
        try:
            forces = image.get_forces(apply_constraint=False)
        except PropertyNotImplementedError:  # XXX bug in old cogef
            return 0.0
        vec = self.get_pulling_vector(image)
        vec /= np.linalg.norm(vec)
        delta_f = 0
        for atom in atoms1:
            delta_f += forces[atom]
        for atom in atoms2:
            delta_f -= forces[atom]
        return np.dot(delta_f, vec) / 2.

    def get_spring_constant(self, atom1=None, atom2=None, IMIN=None,
                            IMAX=None, images=None, plot=False):
        """Calculate and plot the spring constant.

        Parameters
        ----------
        atoms1: int
            Indices of atoms on the one side whose forces are used for the
            calculation of the spring constant force
        atoms2: int
            Indices of atoms on the other side whose forces are used for the
            calculation of the constraint force.
        IMAX: int
            number of images used for fitting
        images: list of atoms object
            name of trajectory

        Returns
        -------
        result: float
            spring constant value.

        """
        self.atom1 = atom1
        self.atom2 = atom2
        self.IMIN = IMIN
        self.IMAX = IMAX
        self.IMAX = len(images)

        def energy_spring(ds, pars):
            return pars[0] * ds**2 + pars[1]*ds + pars[2]

        def force_spring(ds, pars):
            return 2 * pars[0] * ds + pars[1]

        E = []
        D = []
        for mol in images:
            E.append(mol.get_potential_energy())
            D.append(mol.get_distance(atom1, atom2))
        E = array(E)
        E -= E[0]

        PARS = polyfit(D[IMIN:IMAX + 1], E[IMIN:IMAX + 1], 2)
        E_ = energy_spring(array(D), PARS)
        SPRING = PARS[0] * 2 * 1.602 * 10  # convert to N/m

        # Force spring
        # F_LIM = force_spring(D[IMAX], PARS) * 1.602  # convert to nN
        print('spring constant: ', round(SPRING, 1), 'N/m')

        if plot:
            FIG = plt.figure(0)
            AX = FIG.add_axes([0.15, 0.12, 0.8, 0.8])
            AX.set_xlabel(r'Outer Distance $d$ [$\AA$]')
            AX.set_ylabel('Relative energy $\\Delta U$ [eV]')
            AX.plot(D, E, 'o', ms=10)
            AX.plot(D, E_)
            AX.set_title('$SPRING\\mathrm{} \\approx$ %.1f N/m' % (SPRING))
            plt.show()
        return SPRING
