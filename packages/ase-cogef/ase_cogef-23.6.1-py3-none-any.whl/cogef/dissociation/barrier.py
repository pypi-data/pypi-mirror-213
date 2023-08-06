import sys
from copy import deepcopy
from pathlib import Path
import numbers

import ase.vibrations as vibrations
from ase.thermochemistry import IdealGasThermo
from ase.parallel import world


class ElectronicBarrier:
    """Electronic barrier based on COGEF"""
    def __init__(self, cogef,
                 imagemin=0, imagemax=-1, modulo=1,
                 spring_constant=0., energy_tolerance=0,
                 allow_max_at_upper_limit=False):
        """
        Parameters
        ----------
        cogef: COGEF object
          The cogef path.
        imagemin: int
          Image number of first image used from the cogef path.
        imagemax: int
          Image number of last image used from the cogef path.
          Negative values can be used to count from the other direction.
        modulo: int
          Set it to a larger value that less images are used from the cogef
          path, e.g. *modulo=2* means that every second image is used.
          This can be used for numerical tests.
        allow_max_at_upper_limit: bool
          By default an error message will arise in method
          *electronic_extreme_values* if the energy maximum associated to the
          energy barrier lies at the end of the
          considered image interval because it indicates that the real maximum
          lies outside the interval. If you are sure that the maximum of the
          energy barrier lies within or at the end of the interval, you can use
          *allow_max_at_upper_limit=True* to suppress this error message.
        """
        self.cogef = cogef
        self.imagemin = imagemin
        self.imagemax = imagemax
        self.modulo = modulo
        self.spring_constant = spring_constant
        self.energy_tolerance = energy_tolerance
        self.allow_max_at_upper_limit = allow_max_at_upper_limit
        self.error = None

    @property
    def imagemin(self):
        return self._imagemin

    @imagemin.setter
    def imagemin(self, value):
        """Change first image number used from the cogef path.

        Parameters
        ----------
        value: int
            Image number.

        """
        if not isinstance(value, int):
            raise TypeError("imagemin takes only integer values")
        self._imagemin = value

    @property
    def imagemax(self):
        return self._imagemax

    @imagemax.setter
    def imagemax(self, value):
        """Change last image number used from the cogef path.

        Parameters
        ----------
        value: int
            Image number.
            (Negative values can be used to count from the other
            direction.)

        """
        if not isinstance(value, int):
            raise TypeError("imagemax takes only integer values")
        self._imagemax = value

    @property
    def energy_tolerance(self):
        return self._energy_tolerance

    @energy_tolerance.setter
    def energy_tolerance(self, value):
        """Use *energy_tolerance* to allow jumps over small energy barriers
        with *'dE' < energy_tolerance* during the search for the energy
        minimum.

        Parameters
        ----------
        value: float

        """
        if not isinstance(value, numbers.Real):
            raise TypeError("energy_tolerance takes only real numbers")
        self._energy_tolerance = value

    def value(self, f_ext: float) -> float:
        """Return the electronic activation energy/barrier height.

        Parameters
        ----------
        f_ext: External force [eV/A]

        Returns the barrier value [eV]
        """
        pmax, pmin = self.electronic_extreme_values(f_ext)
        return pmax[1] - pmin[1]

    def electronic_extreme_values(self, f_ext, shift=True,
                                  only_minimum=False):
        """Return the maximum and minimum defining the electronic energy
        barrier.

        Parameters
        ----------
        f_ext: float
            External force.
        shift: bool
            *True* means that the energies are shifted. The shift depends on
            the limits of the image interval and the external force.
        only_minimum: bool
            Set it to *True* in order to get only the energy minimum.

        Returns
        -------
        result1: tuple of two floats (optional)
            Image number and energy of the energy maximum.
        result2: tuple of two floats
            Image number and energy of the energy minimum.

        """
        self.error = None
        energies = self.modified_energies(f_ext, shift,
                                          only_intact_bond_images=True)
        energies_copy = deepcopy(energies)
        # Find minimum
        min_at_the_end = True
        while min_at_the_end:
            emin = None
            imin = None
            before_barrier = True
            imin_test = None
            for i, energy in enumerate(energies):
                if (emin is None) or (emin >= energy):
                    emin = energy
                    imin = i
                    min_at_the_end = True
                else:
                    min_at_the_end = False
                if (before_barrier) and \
                        (energy > emin + self.energy_tolerance):
                    before_barrier = False
                    imin_test = imin
            if imin_test is None:
                imin_test = imin
            if min_at_the_end:
                if imin == self.cogef.last_intact_bond_image:
                    break
                # Minimum of energy curve must not be placed at the upper
                # limit of the interval. Upper limit of the interval will
                # be reduced.
                energies = energies[:-1]
                if len(energies) <= 1:
                    self.error = 1
                    raise ValueError('Cannot find a local minimum which ' +
                                     'is not placed at the upper limit ' +
                                     'of the interval. f_ext is too ' +
                                     'large or the range of the ' +
                                     'interval is too small.')
        assert imin_test == imin, 'It seems as if the found minimum is ' + \
                                  'behind the barrier but it should be ' + \
                                  'before. To get rid of this error, ' + \
                                  "set 'last_intact_bond_image' of the " + \
                                  'COGEF object if it is known. Or you ' + \
                                  "could increase 'energy_tolerance' " + \
                                  'of this Dissociation object slightly.'
        if only_minimum:
            return (imin * self.modulo, emin)
        # Find maximum
        emax = None
        imax = None
        max_at_the_end = True
        # use *energies_copy* which contains all energies
        for i, energy in enumerate(energies_copy):
            if i <= imin:
                continue
            if (emax is None) or (emax <= energy):
                emax = energy
                imax = i
                max_at_the_end = True
            else:
                max_at_the_end = False
        if (imax is None) and (imin == self.cogef.last_intact_bond_image):
            # Minimum and maximum are merged together
            emax = emin
            imax = imin
        else:
            if (max_at_the_end) and not (self.allow_max_at_upper_limit) and \
                    (imax < self.cogef.last_intact_bond_image):
                self.error = 2
                raise ValueError('Local maxima of the energy curve must ' +
                                 'not be placed at the upper limit of the ' +
                                 'interval. f_ext or imagemax is too ' +
                                 'small. It may help to ' +
                                 "set 'last_intact_bond_image' of the " +
                                 'COGEF object if it is known.')
        return (imax * self.modulo, emax), (imin * self.modulo, emin)

    def set_spring_constant(self, spring_constant, T, force_min=0.,
                            spring_ref=None):
        """Set the spring constant of the cantilever which stretches the
        molecule.

        Parameters
        ----------
        spring_constant: float
            The new spring constant.
        T: float
            Temperature.
        force_min: float
            Initial external force.
        spring_ref: float (optional)
            Define the reference value for the calculation of the elongation
            if it should not be the initial stretching distance. This can be
            used for transitions starting from instable intermediate states.

        Returns
        -------
        result: float
            The initial stretching distance of the molecule in equilibrium
            associated to the initial external force and temperature.
            This value can be used as a reference value.

        """
        if spring_ref is None:
            self.spring_constant = 0.
            self.spring_ref = self.get_mean_distance(force_min, T)
        else:
            self.spring_ref = spring_ref
        return self.spring_ref

    def modified_energies(self, f_ext, shift=True,
                          only_intact_bond_images=False):
        """Add the influence of a constant external force (and a spring)
        on the electronic energy along the cogef path.

        Parameters
        ----------
        f_ext: float
            External force.
        shift: bool
            *True* means that the energies are shifted such that the global
            energy minimum gets zero.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.

        Returns
        -------
        result: list of floats
            Force-tilted energies in the order of the image numbers.

        """

        energies, distances = self.cogef.get_energy_curve(
            self.imagemin, self.imagemax, only_intact_bond_images,
            modulo=self.modulo)
        if self.spring_constant == 0.:
            energies -= f_ext * distances
        else:
            delta_d = distances - self.spring_ref
            energies += 1 / 2 * (self.spring_constant *
                                 delta_d**2.) - (f_ext * delta_d)
        if shift:
            energies -= min(energies)
        return energies


class GibbsBarrier:
    def __init__(self, electronic_barrier, T, P, initialize=None,
                 dirname='image',
                 vib_method='standard', vib_indices=None, vib_delta=0.01,
                 vib_nfree=2, vib_class='Vibrations', combine_vibfiles=True,
                 geometry='nonlinear', symmetrynumber=1, spin=0):
        """
        Parameters
        ----------
        electronic_barrier: COGEF object
          The electronic barrier
        T: float
            Temperature.
        P: float
            Pressure.
        initialize: function
          Initialization function which is executed before each vibrational
          analysis. See function *do_nothing_vib*.
        dirname: str
          The general directory name for files of the
          vibrational analysis. Image indices will be added automatically.
        vib_method: str
          The method used to obtain vibrational frequencies, see class
          *Vibrations*.
        vib_indices: list of int
          List of indices of atoms to vibrate. Default behavior is
          to vibrate all atoms.
        vib_delta: float
          Magnitude of displacements for vibrational analysis.
        vib_nfree: int
          Number of displacements per atom and cartesian coordinate,
          2 and 4 are
          supported. Default is 2 which will displace each atom +delta and
          -delta for each cartesian coordinate.
        vib_class: str
          The name of the class used. Possible classes are
          *Vibrations* and *Infrared*.
        combine_vibfiles: bool
          Use *True* to combine all pickle files of one image to
          a single pickle
          file after the vibrational analysis. Use *False* to not combine the
          files or to split the combined file to multiples files if it is
          already combined.
        geometry: 'linear', or 'nonlinear'
          Geometry of the molecule used for the calculation of Gibbs energies,
          see class *IdealGasThermo*.
        symmetrynumber: int
          Symmetry number of the molecule. See, for example, Table 10.1 and
          Appendix B of C. Cramer "Essentials of Computational Chemistry",
          2nd Ed.
        spin: float
          The total electronic spin. (0 for molecules in which all electrons
          are paired, 0.5 for a free radical with a single unpaired electron,
          1.0 for a triplet with two unpaired electrons, such as O_2.)
        """
        self.barrier = electronic_barrier
        self.cogef = self.barrier.cogef
        self.error = self.barrier.error
        self.T = T
        self.P = P
        self.initialize = initialize
        self.dirname = dirname
        self.vib_method = vib_method
        self.vib_indices = vib_indices
        self.vib_delta = vib_delta
        self.vib_nfree = vib_nfree
        self.vib_class = vib_class
        self.combine_vibfiles = combine_vibfiles
        assert geometry in ['nonlinear', 'linear']
        self.geometry = geometry
        self.symmetrynumber = symmetrynumber
        self.spin = spin

    def value(self, f_ext: float, verbose=True):
        """Return the Gibbs activation energy/barrier height

        Parameters
        ----------
        f_ext: External force.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        verbose = (verbose) and (world.rank == 0)
        # Canonical Transition-state theory:
        # Use Gibbs energies from the configurations of the
        # electronic maximum (Transition-state structure) and minimum.
        # This is an approximation.
        pmax, pmin = self.barrier.electronic_extreme_values(f_ext)
        emax = pmax[1]
        emin = pmin[1]
        imax = pmax[0]
        imin = pmin[0]
        # Gibbs energy at the minimum and maximum
        for is_maximum, i in [(False, imin), (True, imax)]:
            if verbose:
                if is_maximum:
                    sys.stdout.write('\n' + 'Maximum:')
                else:
                    sys.stdout.write('\n' + 'Minimum:')
            if is_maximum:
                potentialenergy = emax
            else:
                potentialenergy = emin
            gibbs = self.get_gibbs_energy(i, self.T, self.P,
                                          potentialenergy,
                                          is_maximum, verbose)
            if is_maximum:
                gibbs_max = gibbs
            else:
                gibbs_min = gibbs
        return gibbs_max - gibbs_min

    def calculate_vibrations(self, imageindex):
        """Use the class *Vibrations* or *Infrared* to get the files needed
        for the calculation of the Gibbs energy.

        Parameters
        ----------
        imageindex: int
            Image index.

        """
        if self.initialize is None:
            return
        cogef = self.barrier.cogef
        image = cogef.images[imageindex].copy()
        self.initialize(image)
        # No constraints should be set during the calculation of
        # the forces which are needed for the vibrational modes. Even the
        # FixBondLength constraint of the COGEF procedure must be removed.
        image.set_constraint()

        name = Path(cogef.name) / (self.dirname + str(imageindex))
        vib = getattr(vibrations, self.vib_class)(
            image, name=name,
            delta=self.vib_delta, nfree=self.vib_nfree)
        vib.run()
        return vib

    def get_gibbs_energy(self, imageindex, T, P, potentialenergy, is_maximum,
                         verbose):
        """Return the Gibbs energy.

        Parameters
        ----------
        imageindex: int
            Image index.
        T: float
            Temperature.
        P: float
            Pressure.
        potentialenergy: float
            Electronic energy.
        is_maximum: bool
            *True* means that the image corresponds to an energy maximum and
            not minimum.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        vib = self.calculate_vibrations(imageindex)
        image = self.barrier.cogef.images[imageindex].copy()

        vib_energies = vib.get_energies(method=self.vib_method)
        vib_energies = self.vib_energy_correction(
            vib_energies, image, is_maximum, T, P)
        thermo = IdealGasThermo(vib_energies=vib_energies,
                                potentialenergy=potentialenergy,
                                atoms=image,
                                geometry=self.geometry,
                                symmetrynumber=self.symmetrynumber,
                                spin=self.spin)
        return thermo.get_gibbs_energy(T, P, verbose=verbose)

    def vib_energy_correction(self, vib_energies, image, is_maximum, T, P):
        """This method can be used to correct vibrational frequencies.

        Parameters
        ----------
        vib_energies: numpy array of complex
            Vibrational energies.
        image: Atoms object
            The configuration.
        is_maximum: bool
            *True* means that the image corresponds to an energy maximum and
            not minimum.
        T: float
            Temperature.
        P: float
            Pressure.

        Returns
        -------
        result: numpy array of complex
            Corrected vibrational energies.

        """
        if is_maximum:
            # At the Transition-state (Maximum):
            # Do not use the imaginary frequency along the transition path
            natoms = len(image)
            if self.geometry == 'nonlinear':
                vib_energies = vib_energies[-(3 * natoms - 7):]
            elif self.geometry == 'linear':
                vib_energies = vib_energies[-(3 * natoms - 6):]
        return vib_energies
