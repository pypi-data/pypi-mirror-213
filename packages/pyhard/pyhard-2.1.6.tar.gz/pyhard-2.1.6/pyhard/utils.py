import inspect
import json
import traceback
from pathlib import Path
from typing import Any, List, Union

import numpy as np
import pkg_resources
import requests
import yaml
from packaging.version import parse
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import NeighborhoodComponentsAnalysis
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_pypi_version(package: str, url_pattern: str = None):
    """
    Return version of package on pypi.python.org using json.

    Args:
        package: package name
        url_pattern: PyPI URL pattern

    Returns:
        Package version object
    """
    if url_pattern is None:
        url_pattern = URL_PATTERN

    req = requests.get(url_pattern.format(package=package), timeout=5)
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


def get_local_version(package: str = "pyhard") -> str:
    return pkg_resources.require(package)[0].version


def check_new_version(package: str) -> bool:
    try:
        pypi_version = parse(get_pypi_version(package).public)
    except requests.exceptions.RequestException:
        return False
    local_version = parse(get_local_version(package))
    return pypi_version > local_version


def load_yaml_file(path: Union[str, Path]) -> dict:
    """
    Helping function to load YAML files.

    Args:
        path (str or Path): file path

    Returns:
        dict: loaded file
    """
    try:
        with open(path, 'r') as file:
            try:
                return yaml.unsafe_load(file)
            except yaml.YAMLError:
                traceback.print_exc()
    except FileNotFoundError:
        traceback.print_exc()


def write_yaml_file(data: dict, path: Union[str, Path]):
    """
    Helping function to write YAML files.

    Args:
        data (dict): data to be written
        path (str or Path): file path
    """
    with open(path, 'w') as file:
        try:
            return yaml.dump(data, file, default_flow_style=False)
        except yaml.YAMLError:
            traceback.print_exc()


def get_param_names(method) -> List[str]:
    """
    Helping function to get parameters of a given method.

    Args:
        method: class method

    Returns:
        list: name of the parameters
    """
    assert callable(method)
    sig = inspect.signature(method)
    parameters = [p for p in sig.parameters.values() if p.name != 'self' and p.kind != p.VAR_KEYWORD]
    return sorted([p.name for p in parameters])


def call_module_func(module, name, *args, **kwargs) -> Any:
    """
    Calls a module function by its name.

    Args:
        module: a module
        name (str): name of the function
        *args: function args
        **kwargs: function kwargs

    Returns:
        The value returned by the called function
    """
    return getattr(module, name)(*args, **kwargs)


def reduce_dim(X: np.ndarray, y: np.ndarray, n_dim: int = 2, method: str = 'LDA'):
    method = str.upper(method)
    if method == 'LDA':
        model = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis(n_components=n_dim))
    elif method == 'NCA':
        model = make_pipeline(StandardScaler(), NeighborhoodComponentsAnalysis(n_components=n_dim))
    else:
        model = make_pipeline(StandardScaler(), PCA(n_components=n_dim))

    model.fit(X, y)
    X_embedded = model.transform(X)

    return X_embedded


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    r"""
    Call in a loop to create terminal progress bar.

    Args:
        iteration: current iteration
        total: total iterations
        prefix: prefix string
        suffix: suffix string
        decimals: positive number of decimals in percent complete
        length: character length of bar
        fill: bar fill character
        print_end: end character (e.g. \r, \r\n)

    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def pretty_time_delta(seconds: float):
    """
    Pretty print time delta.

    Args:
        seconds (int): elapsed time
    """
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)
