from cogef.minmax import first_maximum_index, second_minimum_index
from cogef.minmax import check_energies, get_first_minimum


def test_first_min():
    """Test minima location"""

    values = [2, 1, 1.1, 0.8, 1]
    assert get_first_minimum(values, 0) == 1
    assert get_first_minimum(values, 0.15) == 0.8
    assert get_first_minimum(values, 0.3) is None
    values = [2, None, 1.1, 0.8, 1]
    assert get_first_minimum(values, 0) == 0.8


def test_first_max():
    """Test maxima location"""

    values = [0, 1, 0.9, 1.2, 1]
    assert first_maximum_index(values, 0) == 1
    assert first_maximum_index(values, 0.15) == 3
    assert first_maximum_index(values, 0.3) is None
    values = [0, None, 0.9, 1.2, 1]
    assert first_maximum_index(values, 0.15) == 3
    values = [1, 1.02, 0.98, 0.8]
    assert first_maximum_index(values, 0.1) == 1


def test_second_min():
    """Test second minimum location"""

    values = [0, 1, 0.9, 1.1, 1, 0, 1]
    assert second_minimum_index(values, 0) == 2
    assert second_minimum_index(values, 0.3) == 5
    assert second_minimum_index(values, 2) is None


def test_check_energies():
    """Test check energies function for COGEF2D"""

    # Test 1
    energy_tolerance = 0.5
    i = 10
    is_maximum = False
    found_min = True
    engs = [1, None, None, 4]
    engs2, emax, emin = check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
    assert [engs2, emin] == [engs[-1:], None]

    # Test 2
    engs = [1]
    try:
        engs2, emax, emin = check_energies(
            engs, energy_tolerance, i, is_maximum, found_min)
    except ValueError:
        pass  # Energy tolerance is too small
    else:
        raise RuntimeError('Missing error message.')

    # Test 3
    # XXX this test uses an index that is larger than
    # XXX the maximal image number in the original implementation
    # XXX not sure why this should make sense => disabled
    if 0:
        i = 30
        engs = [1]
        engs2, emax, emin = check_energies(
            engs, energy_tolerance, i, is_maximum, found_min)
        assert [engs2, emin] == [engs, None]

    # Test 4
    i = 10
    found_min = False
    engs = [1, 2, 3, 2.9, 4, 5]
    try:
        engs2, emax, emin = check_energies(
            engs, energy_tolerance, i, is_maximum, found_min)
    except ValueError:
        pass  # Energy tolerance is too small
    else:
        raise RuntimeError('Missing error message.')

    # Test 5
    engs = [1, None, None, 3, 2.9, 4, 5]
    try:
        engs2, emax, emin = check_energies(
            engs, energy_tolerance, i, is_maximum, found_min)
    except ValueError:
        pass  # Energy tolerance is too small
    else:
        raise RuntimeError('Missing error message.')

    # Test 6
    found_min = True
    engs = [1, None, None, 4, 5]
    engs2, emax, emin = check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
    assert [engs2, emin] == [engs[-1:], None]

    # Test 7
    found_min = False
    engs = [1, 2, 3, 4, 5]
    try:
        engs2, emax, emin = check_energies(
            engs, energy_tolerance, i, is_maximum, found_min)
    except RuntimeError:
        pass  # Maximum must be obtained first
    else:
        raise RuntimeError('Missing error message.')

    # Test 8
    found_min = True
    engs = [1, 2, 3, 2.9, 4, 5]
    engs2, emax, emin = check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
    assert [engs2, emin] == [engs[-1:], None]
