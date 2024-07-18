import numpy as np
from pathlib import Path
import pydist
import pytest


def test_loading_influenza_incubation():
    """
    Test that we can load a Weibull distribution for the influenza incubation
    period.
    """
    data_file = Path('tests') / 'influenza_incubation.rds'
    assert data_file.exists()
    dist = pydist.load_distribution(data_file)
    assert dist is not None

    # These are known properties of the distribution.
    expected_mean = 3.4
    expected_sd = 1.7
    assert np.allclose(dist.mean(), expected_mean)
    assert np.allclose(dist.std(), expected_sd)

    samples = dist.rvs(size=1000)
    assert np.all(samples > 0)


def test_known_scipy_dist():
    """
    Test that we can retrieve known SciPy distribution names.
    """
    dist = pydist.get_scipy_dist_name('poisson')
    assert dist == 'poisson'


def test_unknown_scipy_dist():
    """
    Test that unknown SciPy distribution names raise exceptions.
    """
    with pytest.raises(ValueError):
        pydist.get_scipy_dist_name('does_not_exist')


def test_known_scipy_params():
    """
    Test that we can retrieve known SciPy distribution parameters.
    """
    shape = 10
    scale = 20
    r_params = {'shape': shape, 'scale': scale}
    params = pydist.get_scipy_dist_params('weibull_min', r_params)
    assert set(params.keys()) == {'c', 'scale'}
    assert params['c'] == shape
    assert params['scale'] == scale


def test_unknown_scipy_params():
    """
    Test that invalid SciPy distribution parameters raise exceptions.
    """
    shape = 10
    scale = 20
    r_params = {'shape': shape, 'scale': scale}
    with pytest.raises(ValueError):
        pydist.get_scipy_dist_params('does_not_exist', r_params)


def test_invalid_input_file():
    """
    Test that attempting to read from an invalid file raises an exception.
    """
    invalid_file = Path('tests') / 'invalid_distribution.rds'
    assert invalid_file.exists()
    with pytest.raises(ValueError):
        pydist.load_distribution(invalid_file)


def test_custom_maps():
    """
    Test that we can provide custom mappings between R and Python, by
    instructing pydist to map Weibull distributions to Beta distributions.
    """
    data_file = Path('tests') / 'influenza_incubation.rds'
    dist_map = {'weibull': 'beta'}
    param_map = {'beta': {'shape': 'a', 'scale': 'b'}}
    dist = pydist.load_distribution(data_file, dist_map, param_map)

    # Check that the returned distribution has mean and variance that are
    # consistent with the expected Beta distribution.
    # NOTE: "a" (shape) is ~2.10 and "b" (scale) is ~3.84
    a = 2.1
    b = 3.84
    approx_mean = a / (a + b)
    approx_var = a * b / ((a + b) ** 2 * (a + b + 1))
    assert np.abs(approx_mean - dist.mean()) < 1e-3
    assert np.abs(approx_var - dist.var()) < 1e-3
