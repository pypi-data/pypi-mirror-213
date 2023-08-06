from ase.units import J, m
from scipy.special import lambertw

from cogef.units import nN, kB, _hplanck, _e
import numpy as np
from numpy import arange, exp, array, real

f = m / J * 1e9  # ev/A -> nN
h = _hplanck / _e


class MPF:
    """

    Class for calculating Most Probable Force (MPF)
    """
    def __init__(self, De: float, Fmax: float):
        """

        :param De: dissociation energy, eV
        :param Fmax: maximal force, eV/A
        These parameters are unique to given molecule

        """
        self.De = De
        self.Fmax = Fmax

    def getParams(self, T_K: float, alpha_nNs: float):
        """

        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s
        The loading rate is usually given in nN/s in experiments

        :return: alpha = loading rate, eV/As
        beta = inverse thermal energy, 1/eV
        tau = lifetime of dissociation energy, s
        tmax = time required to reach maximum force, s

        """
        beta = 1 / (kB * T_K)
        alpha = alpha_nNs * nN  # eV/As
        # multiply units (eg. nN) to get values in cogef units (eV/A)
        # [no diff for s]
        tmax = self.Fmax / alpha
        prefactor = kB * T_K / h
        inverse_tau = prefactor * np.exp(-beta * self.De)
        tau = 1 / inverse_tau

        return alpha, beta, tau, tmax

    def bell(self, T_K, alpha_nNs):
        """

        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s
        In experiments, the loading rate is generally given in nN/s

        :return: Most probable relative force F*/Fmax (unitless)

        """
        alpha, beta, tau, tmax = self.getParams(T_K=T_K, alpha_nNs=alpha_nNs)
        num = 2 * tau * beta * self.De / tmax
        den = 2 * beta * self.De
        relative_f = np.log(num) / den
        return relative_f

    def bell_pd(self, T_K, alpha_nNs, force_step=0.01, prob_break_value=0.0):
        """

        Probability density calculations for relative force, Bell
        different from numerical as we take normalized rates, forces here
        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s
        :param force_step: set force increment value
        :param prob_break_value: set probability until which MPF calculations
        are to be run.
        If bond break does not occur at this probability value, calculation
        is stopped

        :return: dp/df values
        array of relative forces, unitless

        """
        alpha, beta, tau, tmax = self.getParams(T_K=T_K, alpha_nNs=alpha_nNs)
        integration = 0.
        dpdf = []
        relative_forces = []
        start = True
        for f_n in arange(0, 1 + force_step / 2.,
                          force_step):
            # unitless rate for Bell
            rate = np.exp(2 * beta * self.De * f_n)
            if start:
                start = False
                # In the first round only one half step
            else:
                # Half step
                integration += rate * force_step / 2.
            prob = exp(-tmax * integration / tau)
            dpdf.append(tmax * rate * prob / tau)
            relative_forces.append(f_n)
            if prob <= prob_break_value:
                break
            # Half step
            integration += rate * force_step / 2.

        return array(dpdf), array(relative_forces)

    def general(self, T_K, alpha_nNs):
        """

        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s

        :return: Most probable relative force F*/Fmax (unitless)

        """
        alpha, beta, tau, tmax = self.getParams(T_K=T_K, alpha_nNs=alpha_nNs)
        const = tmax * np.exp(beta * self.De) / (tau * 2 * beta * self.De)
        W = lambertw(2 * beta * self.De * (const ** 2)) / (2 * beta * self.De)
        # lambertw function gives complex number, considering real forces
        relative_f = real(1 - np.sqrt(W))

        return relative_f

    def general_pd(self, T_K, alpha_nNs, force_step=0.01, prob_break_value=0):
        """

        Probability density calculations for relative force, General
        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s
        :param force_step: set force increment value
        :param prob_break_value: set probability until which MPF calculations
        are to be run.
        If bond break does not occur at this probability value, calculation
        is stopped

        :return: dp/df values
        array of forces, unitless

        """
        alpha, beta, tau, tmax = self.getParams(T_K=T_K, alpha_nNs=alpha_nNs)
        integration = 0.
        dpdf = []
        relative_forces = []
        start = True
        for f_n in arange(0, 1 + force_step / 2.,
                          force_step):
            # unitless rate for general expression
            rate = np.exp(beta * self.De * f_n * (2 - f_n))
            if start:
                start = False
                # In the first round only one half step
            else:
                # Half step
                integration += rate * force_step / 2.
            prob = exp(-tmax * integration / tau)
            dpdf.append(tmax * rate * prob / tau)
            relative_forces.append(f_n)
            if prob <= prob_break_value:
                break
            # Half step
            integration += rate * force_step / 2.
        return array(dpdf), array(relative_forces)

    def general_verify(self, relative_f, T_K, alpha_nNs):
        """

        Verifying against the f by using it on right hand of real equation
                    tmax         1
            1-f =  ------ * ------------ * exp [ beta * U * f (2 - f) ]
                     tou    2 * beta * U
        :param relative_f: relative_f, unitless
        :param T_K: Temperature, K
        :param alpha_nNs: Loading rate, nN/s

        :return: expected relative force, unitless

        """
        alpha, beta, tau, tmax = self.getParams(T_K=T_K, alpha_nNs=alpha_nNs)
        exponential = exp(beta * self.De * relative_f * (2 - relative_f))
        one_minus_f = ((tmax / tau) * 1 / (2 * beta * self.De) * exponential)
        expected_f = 1 - one_minus_f
        return expected_f

    def width_f(self, T_K):
        """
        width of relative MPF applicable for both General and Bell expressions
        :param T_K: Temperature, K
        :return: width of relative most probable force

        """
        beta = 1 / (kB * T_K)
        width = 1.925 / (2 * beta * self.De)
        return width
