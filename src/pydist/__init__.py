import rdata
import scipy.stats


def load_distribution(rds_file, dist_map=None, param_map=None):
    """
    Return a frozen SciPy distribution that corresponds to an epiparameter
    probability distribution.

    :param rds_file: The RDS file from which to read the distribution details.
    :param dist_map: An optional custom mapping between R distribution names
        and ``scipy.stats`` functions; see :func:`dist_names_map`.
    :param param_map: An optional custom mapping between R shape parameter
        names and ``scipy.stats`` shape parameter names; see
        :func:`dist_params_map`.
    """
    results = rdata.read_rds(rds_file)

    expect_keys = {'name', 'params'}
    if set(results.keys()) != expect_keys:
        raise ValueError('RDS file contains unexpected items')

    dist_name = str(results['name'][0])
    params = {
        str(name): values[0] for name, values in results['params'].items()
    }

    scipy_name = get_scipy_dist_name(dist_name, mapping=dist_map)
    scipy_dist = getattr(scipy.stats, scipy_name)
    param_dict = get_scipy_dist_params(scipy_name, params, mapping=param_map)

    dist_obj = scipy_dist(**param_dict)
    return dist_obj


def dist_names_map():
    """
    Return a dictionary that maps R distribution names to those defined in the
    ``scipy.stats`` module.
    """
    return {'weibull': 'weibull_min'}


def get_scipy_dist_name(dist_name, mapping=None):
    """
    Return the name of a ``scipy.stats`` function that corresponds to the
    given R distribution.

    :param dist_name: The R name for the distribution.
    :param mapping: An optional custom mapping between R distribution names
        and ``scipy.stats`` functions.
    """
    if mapping is None:
        mapping = dist_names_map()

    if hasattr(scipy.stats, dist_name):
        return dist_name
    elif dist_name in mapping:
        return mapping[dist_name]
    else:
        raise ValueError(f'Unknown distribution "{dist_name}"')


def dist_params_map():
    """
    Return a dictionary that maps SciPy distribution names to dictionaries
    that map R shape parameter names to SciPy shape parameter names.
    """
    return {
        'weibull_min': {
            'shape': 'c',
            'scale': 'scale',
        },
    }


def get_scipy_dist_params(scipy_name, params, mapping=None):
    """
    Return a dictionary of keyword arguments for a ``scipy.stats`` function,
    corresponding to the R shape parameters for a distribution.

    :param scipy_name: The name of the ``scipy.stats`` function.
    :param params: A dictionary of R shape parameters.
    :param mapping: An optional custom mapping between R shape parameter names
        and ``scipy.stats`` shape parameter names.
    """
    if mapping is None:
        mapping = dist_params_map()

    if scipy_name not in mapping:
        raise ValueError(f'Unknown parameters for {scipy_name}')

    params_map = mapping[scipy_name]
    return {py_name: params[r_name] for r_name, py_name in params_map.items()}
