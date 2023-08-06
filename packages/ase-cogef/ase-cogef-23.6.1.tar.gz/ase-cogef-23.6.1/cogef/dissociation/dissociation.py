# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module for calculating rupture forces based on the dissociation
rates.

"""
from numpy import exp, arange, log, array

from cogef.units import kB, _hplanck, _e

from cogef import rupture_force_from_dpdf
from cogef import rupture_force_and_uncertainty_from_dpdf

# h in units eV * s
h = _hplanck / _e


class Dissociation(object):
    """Class for calculating energy barriers, dissociation rates
    and the resulting rupture force at a given temperature and pressure.

    ***Force units are in eV/A***
    """

    def __init__(self, barrier):
        """
        Parameter
        ----------
        barrier: Barrier object
        """
        self.barrier = barrier

        self.spring_constant = 0.
        self.spring_ref = 0.
        self.energy_tolerance = 0
        self.error = None

        self.barrier = barrier

    def get_rate(self, f_ext, T, verbose=True):
        """Return dissociation rate constant from the Eyring equation
        at given temperature and pressure.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        P: float
            Pressure.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        try:
            barrier = self.barrier.value(f_ext)
        except ValueError as e:
            self.error = self.barrier.error
            raise e

        kBT = kB * T
        return kBT / h * exp(- barrier / kBT)

    def get_rate_constants(self, T, P, force_max, force_min=0.,
                           force_step=0.01, method='Gibbs', verbose=False):
        """Return dissociation rate constants.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result1: list of floats
            Rate constants.
        result2: list of floats
            External forces.

        """
        rates = []
        forces = []
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            rates.append(self.get_rate(f_ext, T, verbose))
            forces.append(f_ext)
        return rates, forces

    def save_rate_constants(self, T, P, force_max, force_min=0.,
                            force_step=0.01, method='Gibbs',
                            fileout='rates.dat'):
        """Save dissociation rate constants to a file.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        fileout: str
            Filename.

        """
        rates, forces = self.get_rate_constants(T, P, force_max, force_min,
                                                force_step, method)
        fd = open(fileout, 'w')
        if self.spring_constant == 0.:
            fd.write('Force\t' + 'Rate constant\n')
            space = '\t'
        else:
            fd.write('Loading rate * time\t' + 'Rate constant\n')
            space = '\t\t\t'
        for i in range(len(rates)):
            fd.write(str(round(forces[i], 10)) + space + str(rates[i]) + '\n')
        fd.close()

    def probability_density(self, T, loading_rate, force_max,
                            force_min=0., force_step=0.01,
                            verbose=False, probability_break_value=0.):
        """Return a list of dp/df-values within a given force interval.

        p is the bond-breaking probability and f is the external force.
        The maximum of the dp/df-values corresponds to the most probable
        rupture force.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.
        probability_break_value: float
            The calculation is canceled when the probability that the bond is
            not broken drops below this value.

        Returns
        -------
        result1: numpy array of float
            dp/df-values.
        result2: numpy array of float
            External forces.

        """
        integration = 0.
        dpdf = []
        forces = []
        start = True
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            last_rate = self.get_rate(f_ext, T, verbose=verbose)
            if start:
                start = False
                # In the first round only one half step
            else:
                # Half step
                integration += last_rate * force_step / 2.
            prob = exp(-integration / loading_rate)
            dpdf.append(last_rate / loading_rate * prob)
            forces.append(f_ext)
            if prob <= probability_break_value:
                break
            # Half step
            integration += last_rate * force_step / 2.
        return array(dpdf), array(forces)

    def external_force(self, T, force_max, force_min=0., force_step=0.01):
        """Return a list of external force values.

        The external force is not equal to
        f_ext = 'spring constant' * 'velocity'  * 'time' + force_min
        due to the spring and the elongation of the molecule.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of *f_ext* interval.
        force_min: float
            Lower limit of *f_ext* interval.
        force_step: float
            Step size of *f_ext*.

        Returns
        -------
        result 1: List of float
            External forces.
        result 2: List of float
            *f_ext* values.

        """
        if self.spring_ref is None:
            raise ValueError('You have to set the spring constant first.')
        spring_constant = self.spring_constant
        fs_tot = []
        forces = []
        # 'f_ext' has the meaning of [loading rate * time + force_min]
        # which is the external force for zero spring constant or unchanged
        # molecule length
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            d = self.get_mean_distance(f_ext, T)
            delta_d = d - self.spring_ref
            fs_tot.append(f_ext - spring_constant * delta_d)
            forces.append(f_ext)
        return fs_tot, forces

    def save_external_forces(self, T, force_max, force_min=0.,
                             force_step=0.01, fileout='force.dat'):
        """Save external forces. See method *external_force*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of *f_ext* interval.
        force_min: float
            Lower limit of *f_ext* interval.
        force_step: float
            Step size of *f_ext*.
        fileout: str
            Filename.

        """
        fs_tot, forces = self.external_force(T, force_max, force_min,
                                             force_step)
        fd = open(fileout, 'w')
        fd.write('Loading rate * time\t' + 'External force\n')
        for i in range(len(fs_tot)):
            fd.write(str(round(forces[i], 10)) + '\t\t\t' + str(fs_tot[i]) +
                     '\n')
        fd.close()

    def rupture_force(self, T, P, loading_rate, force_max, force_min=0.,
                      force_step=0.01, method='Gibbs', verbose=False):
        """Calculate the average rupture force for a given loading rate
        by numerical integration.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval. It should be set as
            large as possible and as necessary for a good result.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        dpdf, forces = self.probability_density(T, P, loading_rate,
                                                force_max, force_min,
                                                force_step, method, verbose)
        if self.spring_constant == 0.:
            return rupture_force_from_dpdf(dpdf, forces)
        else:
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step)
            return rupture_force_from_dpdf(dpdf, fs_tot, force_step)

    def rupture_force_and_uncertainty(self, T, loading_rate, force_max,
                                      force_min=0., force_step=0.01,
                                      method='Gibbs', verbose=False):
        """Calculate the average rupture force and its uncertainty for a
        given loading rate.

        The uncertainty is defined as the range
        around the average rupture force which contains all forces with a
        total probability of 68.3% (one standard deviation).

        Parameters
        ----------
        T: float
            Temperature.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval. It should be set as
            large as possible and as necessary for a good result.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result 1: float
            Rupture force.
        result 2: float
            Standard deviation.

        """
        dpdf, forces = self.probability_density(T, loading_rate,
                                                force_max, force_min,
                                                force_step, method, verbose)
        if self.spring_constant == 0.:
            return rupture_force_and_uncertainty_from_dpdf(dpdf, forces)
        else:
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step)
            return rupture_force_and_uncertainty_from_dpdf(dpdf, fs_tot,
                                                           force_step)

    def most_probable_force_is_larger(self, f_ext, T, loading_rate,
                                      force_step=0.01):
        """Return *True* if the most probable force is larger than *f_ext*.

        The method is 'electronic'. The forces are only considered in the
        interval in which the rates can be calculated.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_step: float
            Force step size used.

        Returns
        -------
        result: bool

        """
        try:
            dpdf, forces = self.probability_density(
                T, loading_rate, force_max=f_ext + force_step,
                force_min=f_ext, force_step=force_step)
        except ValueError:
            assert self.error in [1, 2]
            if self.error == 1:
                # *f_ext* or *f_ext + force_step* are too large for the
                # calculation of the rate
                return False
            elif self.error == 2:
                # *f_ext* or *f_ext + force_step* are too small for the
                # calculation of the rate
                return True
        if dpdf[0] < 1e-30:
            # If the *dpdf* values are near to zero than only because of
            # very small or very large rates
            rate = self.get_rate(f_ext, T, verbose=False)
            return rate / loading_rate < 1e-20
        # The ratio between two *dpdf* values are independent of *force_min*
        # and can be used to find the maximum
        return dpdf[1] / dpdf[0] > 1

    def get_force_limits(self, T, loading_rate, factor=10,
                         force_step=0.01, method='Gibbs'):
        """Determine good force limits for the calculation of the rupture
        force.

        The initial external force is assumed to be zero.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        factor: float
            The probability density at the limits of the interval will be
            smaller than the maximum of the probability distribution divided
            by *factor*.
        force_step: float
            Force step size used. The limits are multiples of *force_step*.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.

        Returns
        -------
        result 1: float
            Lower limit.
        result 2: float
            Upper limit.

        """
        assert method in ['electronic', 'Gibbs']
        self.error = None
        force_min = 0.
        if method == 'electronic':
            # Search most probable force
            n = -1
            f_ext = 0.
            while self.most_probable_force_is_larger(f_ext, T,
                                                     loading_rate,
                                                     force_step=force_step):
                n += 1
                f_ext = force_step * 2**n
            n -= 2
            if n < 0:
                self.error = 3
                raise ValueError('force_step is not small enough or the ' +
                                 'COGEF-trajectory was not calculated ' +
                                 'far enough.')
            f_ext -= force_step * 2**n
            while n >= 0:
                n -= 1
                if self.most_probable_force_is_larger(f_ext, T,
                                                      loading_rate,
                                                      force_step=force_step):
                    if n >= 0:
                        f_ext += force_step * 2**n
                    else:
                        f_ext += force_step
                else:
                    if n >= 0:
                        f_ext -= force_step * 2**n
            # Increase interval range around the most probable force in
            # dependence of *factor*
            force_max = f_ext
            ratio = 1.
            while ratio >= 1. / factor:
                try:
                    dpdf, forces = self.probability_density(
                        T, loading_rate, force_max + force_step,
                        force_max, force_step)
                except ValueError:
                    assert self.error in [1, 2]
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                if dpdf[0] < 1e-30:
                    self.error = 3
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                ratio *= dpdf[1] / dpdf[0]
                force_max += force_step

            force_min = f_ext
            ratio = 1.
            while ratio >= 1. / factor:
                try:
                    dpdf, forces = self.probability_density(
                        T, loading_rate, force_min, force_min - force_step,
                        force_step)
                except ValueError:
                    assert self.error in [1, 2]
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                if dpdf[0] < 1e-30:
                    self.error = 3
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                ratio *= dpdf[0] / dpdf[1]
                force_min -= force_step
            return force_min, force_max
        elif method == 'Gibbs':
            # Calculate limits for method='electronic'
            force_min, force_max = self.get_force_limits(T, loading_rate,
                                                         factor,
                                                         force_step,
                                                         method='electronic')
            P = 0  # XXX probably get rid of this code
            return self.get_force_limits_gibbs(T, P, loading_rate, force_min,
                                               force_max, factor, force_step)

    def get_force_limits_gibbs(self, T, P, loading_rate, force_min, force_max,
                               factor=10, force_step=0.01):
        """Determine good force limits for the calculation of the rupture
        force with method='Gibbs'.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_min: float
            Lower limit for method='electronic'.
        force_max: float
            Upper limit for method='electronic'.
        factor: float
            The probability density at the limits of the interval will be
            smaller than the maximum of the probability distribution divided
            by *factor*.
        force_step: float
            Force step size used. The limits are multiples of *force_step*.

        Returns
        -------
        result 1: float
            Lower limit.
        result 2: float
            Upper limit.

        """
        # Estimate shift if method is changed from 'electronic' to 'Gibbs'
        rate_el_max = self.get_rate(force_max, T, verbose=False)
        f_ext = force_min
        rate_gibbs = self.get_rate(f_ext, T, verbose=False)
        while rate_gibbs > rate_el_max:
            f_ext -= force_step
            try:
                rate_gibbs = self.get_rate(f_ext, T, verbose=False)
            except ValueError:
                self.error = 3
                raise ValueError('COGEF-trajectory was not ' +
                                 'calculated far enough.')
        while rate_gibbs < rate_el_max:
            f_ext += force_step
            try:
                rate_gibbs = self.get_rate(f_ext, T, P, 'Gibbs',
                                           verbose=False)
            except ValueError:
                self.error = 3
                raise ValueError('COGEF-trajectory was not ' +
                                 'calculated far enough.')
        df = f_ext - force_max
        force_max += df
        force_min += df
        try:
            dpdf, forces = self.probability_density(T, P, loading_rate,
                                                    force_max, force_min,
                                                    force_step,
                                                    method='Gibbs')
        except ValueError:
            self.error = 3
            raise ValueError('COGEF-trajectory was not ' +
                             'calculated far enough.')
        imax = list(dpdf).index(max(dpdf))
        # Most probable force
        f_ext = forces[imax]
        # Increase the range of the interval in dependence of 'factor'
        force_max = f_ext
        ratio = 1.
        while ratio >= 1. / factor:
            try:
                dpdf, forces = self.probability_density(
                    T, P, loading_rate, force_max + force_step,
                    force_max, force_step, method='Gibbs')
            except ValueError:
                assert self.error in [1, 2]
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            if dpdf[0] < 1e-30:
                self.error = 3
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            ratio *= dpdf[1] / dpdf[0]
            force_max += force_step

        force_min = f_ext
        ratio = 1.
        while ratio >= 1. / factor:
            try:
                dpdf, forces = self.probability_density(
                    T, P, loading_rate, force_min, force_min - force_step,
                    force_step, method='Gibbs')
            except ValueError:
                assert self.error in [1, 2]
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            if dpdf[0] < 1e-30:
                self.error = 3
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            ratio *= dpdf[0] / dpdf[1]
            force_min -= force_step
        return force_min, force_max

    def get_minimum_distances(self):
        """Return the distances from the cogef images with intact bond.

        Returns
        -------
        result: list of floats

        """
        energies, distances = self.barrier.cogef.get_energy_curve(
            self.imagemin, self.imagemax, only_intact_bond_images=True,
            modulo=self.modulo)
        return distances

    def get_mean_distance(self, f_ext, T, check=True):
        """Return the mean distance from the cogef images.

        It is assumed that the molecule structure is always one image of the
        calculated minimum trajectory and Boltzmann distributed associated
        to their electronic energies.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        check: bool
            Set it to *True* in order to check whether the number of the
            last intact bond minimum is set. This is recommended.

        Returns
        -------
        result: float

        """
        distances = self.get_minimum_distances()
        energies = self.modified_energies(f_ext, only_intact_bond_images=True)
        assert len(distances) == len(energies)
        if (check) and (self.cogef.last_intact_bond_image >= len(energies)):
            raise ValueError("You have to set 'last_intact_bond_image' of " +
                             'the COGEF object.')
        sum_dist = 0.
        sum_weight = 0.
        for i, energy in enumerate(energies):
            dist = distances[i]
            weight = exp(-energy / (kB * T))
            sum_dist += dist * weight
            sum_weight += weight
        return sum_dist / sum_weight

    def get_mean_distances(self, T, force_max, force_min=0., force_step=0.01,
                           use_spring_ref=False):
        """Return mean distances. See method *get_mean_distance*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        use_spring_ref: bool
            *True* means that distances are obtained relative to the
            equilibrium distance. This is possible if a spring constant
            is set.

        Returns
        -------
        result 1: list of float
            Mean distances.
        result 2: list of float
            External forces.

        """
        dists = []
        forces = []
        if use_spring_ref:
            assert self.spring_ref is not None
            dist0 = self.spring_ref
        else:
            dist0 = 0.
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            dists.append(self.get_mean_distance(f_ext, T) - dist0)
            forces.append(f_ext)
        return dists, forces

    def save_mean_distances(self, T, force_max, force_min=0., force_step=0.01,
                            fileout='dists.dat', use_spring_ref=False):
        """Save mean distances to a file. See method *get_mean_distances*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        fileout: str
            Filename.
        use_spring_ref: bool
            *True* means that distances are obtained relative to the
            equilibrium distance. This is possible if a spring constant
            is set.

        """
        dists, forces = self.get_mean_distances(T, force_max, force_min,
                                                force_step, use_spring_ref)
        if use_spring_ref:
            distance = 'delta d'
        else:
            distance = 'distance'
        fd = open(fileout, 'w')
        if self.spring_constant == 0.:
            fd.write('Force\t' + 'Mean ' + distance + '\n')
            space = '\t'
        else:
            fd.write('Loading rate * time\t' + 'Mean ' + distance + '\n')
            space = '\t\t\t'
        for i in range(len(dists)):
            fd.write(str(round(forces[i], 10)) + space + str(dists[i]) + '\n')
        fd.close()

    def get_d_parameter(self, T, P, loading_rate, dpdf, forces,
                        method='Gibbs'):
        """Get the d-parameter.

        The parameter d can be used to describe the dependence of the
        rupture force on loading rate and temperature using the function
        *estimate_force_change*.

        Parameters
        ----------
        T: float
            Temperature used for dpdf.
        P: float
            Pressure used for dpdf.
        loading_rate: float
            Loading rate used for dpdf.
        dpdf: numpy array of float
            dpdf-values from method *probability_density*.
        forces: numpy array of float
            External forces from method *probability_density* associated to
            dpdf.
        method: 'electronic' or 'Gibbs'
            Method used for dpdf.

        Returns
        -------
        result: float
            The d-parameter in Angstrom.

        """

        index = list(dpdf).index(max(dpdf))
        # Most probable rupture force
        fmp = forces[index]
        rate = self.get_rate(fmp, T, P, method, verbose=False)
        return kB * T / loading_rate * rate


def estimate_force_change(d, T, T_new, loading_rate, loading_rate_new):
    """Estimate change of the rupture force.

    The rupture force change can be estimated for small changes of
    temperature and loading rate with the help of the d-parameter from
    method *get_d_parameter* in class *Dissociation*.

    Parameters
    ----------
    d: float
        d-parameter.
    T: float
        Temperature associated to the d-parameter.
    T_new: float
        Temperature of the estimated rupture force.
    loading_rate: float
        Loading rate associated to the d-parameter.
    loading_rate_new: float
        Loading rate of the estimated rupture force.

    """
    factor = 1.
    part1 = T * log(loading_rate * d * h / (kB * T)**2)
    part2 = T_new * log(loading_rate_new * d * h / (kB * T_new)**2)
    return kB / d * (part2 - part1) * factor
