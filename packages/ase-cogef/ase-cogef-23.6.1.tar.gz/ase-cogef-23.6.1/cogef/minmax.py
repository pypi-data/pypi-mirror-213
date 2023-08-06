def first_maximum_index(values, tolerance):
    """ Find the first maximum.

    Return first value from list *values* for which the next values
    decrease by more than *tolerance* or return None when no maximum can be
    identified. Restart searching after a value which is None.

    Parameters
    ----------
    values: list of float
    tolerance: float

    Returns
    -------
    result: index of maximum or None

    """
    valuemax = None
    imax = 0
    for i, value in enumerate(values):
        if value is None:
            continue
        if (valuemax is None) or (value > valuemax):
            valuemax = value
            imax = i
        else:
            if valuemax > value + tolerance:
                return imax
    return None


def get_first_maximum(energies, energy_tolerance):
    imax = first_maximum_index(energies, energy_tolerance)
    if imax is None:
        return None
    return energies[imax]


def first_minimum_index(values, tolerance):
    """Find the first minimum.

    Return first value from list *values* for which the next values
    increase by more than *tolerance* or return None when no maximum can be
    identified. Restart searching after a value which is None.

    Parameters
    ----------
    values: list of float
    tolerance: float

    Returns
    -------
    result: float or None

    """
    valuemin = None
    for i, value in enumerate(values):
        if value is None:
            valuemin = None
            continue
        if (valuemin is None) or (value < valuemin):
            valuemin = value
        else:
            if valuemin < value - tolerance:
                return i - 1
    return None


def get_first_minimum(energies, energy_tolerance):
    imin = first_minimum_index(energies, energy_tolerance)
    if imin is None:
        return None
    return energies[imin]


def second_minimum_index(energies, energy_tolerance):
    imax = first_maximum_index(energies, energy_tolerance)
    if imax is None:
        return None
    imin = first_minimum_index(energies[imax:], energy_tolerance)
    if imin is None:
        return None
    return imax + imin


def check_energies(energies, energy_tolerance, i, is_maximum,
                   found_min):
    """Check energies of the existing images and check parameters.

        Search for energy maximum or minimum in 'energies' and check, if
        necessary, whether 'energies' is suitable in order to find
        the minimum by calculating further energy values.

        Parameters
        ----------
        energies: list of float and None
            Energies of exisiting images. Contains None for gaps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        i: int
            Image number of the corresponding reactant image.
        is_maximum: bool
            Maximum must be found if it is *True*, otherwise a minimum must be
            found.
        found_min: bool
            There is a known minimum at larger bond lengths if it is *True*.

        Returns
        -------
        energies: list of float and None
            Initial energies for finding the extrema.
        emax: float or None
            Energy of the maximum if already identified.
        emin: float or None
            Energy of the product minimum if already identified.

    """
    emax = get_first_maximum(energies, energy_tolerance)
    emin = None
    if not is_maximum:  # we are searching for a minimum
        if emax is None:
            if (len(energies) == 1) or \
               (get_first_maximum(energies, 0.) is not None) and \
               not found_min:
                raise ValueError(
                    'Cannot identify broken-bond ' +
                    'minimum. energy_tolerance is ' +
                    'too large or image ' + str(i) +
                    ' is not in the range in ' +
                    'which a barrier can be ' +
                    'found. Perhaps you can ' +
                    'prevent this error message ' +
                    'if you use the function ' +
                    "'set_last_intact_bond_image'.")
            if not found_min:
                raise RuntimeError(
                    'Cannot identify broken-bond ' +
                    'minimum of image ' + str(i) +
                    '. The maximum of this image ' +
                    'must be searched first.')
        else:
            energies = energies[energies.index(emax):]
        if (len(energies) > 1) and (found_min):
            # To prevent errors if only the
            # product/broken-bond minimum shall be calculated
            energies = energies[-1:]
        emin = get_first_minimum(energies, energy_tolerance)
        if emin is not None:
            j = energies.index(emin)
            if (len(energies) > j + 1) and (energies[j + 1] is None):
                raise RuntimeError('Something wrong with the ' +
                                   'found minimum.')
    return energies, emax, emin
