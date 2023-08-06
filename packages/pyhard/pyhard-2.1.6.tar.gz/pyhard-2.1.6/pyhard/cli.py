"""
Command-line interface module.
"""

import logging
import os
import shutil
import time
from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import typer
from pyispace.example import save_opts
from pyispace.trace import trace_build_wrapper, make_summary, _empty_footprint  # noqa
from pyispace.utils import save_footprint, scriptcsv

from . import integrator, formatter
from .app import ClassificationApp, RegressionApp
from .context import Configuration, Workspace
from .feature_selection import filtfeat, variance_filter, correlation_filter
from .metrics import loss_threshold
from .structures import Configurations, GeneralConfig, FSConfig, HPOConfig, ISAConfig
from .utils import pretty_time_delta, check_new_version
from .validator import *
from .visualization import Demo


_conf_file = 'config.yaml'
_logger = logging.getLogger(__name__)

cli = typer.Typer(
    no_args_is_help=True,
    help="PyHard CLI application help.",
    add_completion=False
)


def _load_config(path: Optional[Path] = None) -> Configurations:
    _my_path = Path().absolute()

    if path is None:
        config_path = _my_path / _conf_file
    else:
        config_path = path
    _logger.info(f"Configuration file: '{str(config_path)}'")

    return Configuration(config_path).load()


def _validate_paths(config: Configurations) -> Configurations:
    _my_path = Path().absolute()
    config_valid = config.copy()

    for name, path_str in config_valid.general.get_path_fields().items():
        if path_str is None:
            continue

        path = Path(path_str)
        if not path.is_absolute():
            path = _my_path / path
            path = path.resolve()

        if name.endswith('dir') and not path.is_dir():
            raise NotADirectoryError(f"Field '{name}' contains an invalid directory path: '{str(path)}'")
        elif name.endswith('file') and not path.is_file():
            raise FileNotFoundError(f"Field '{name}' contains an invalid file path: '{str(path)}'")
        else:
            config_valid.general.set(name, path)

    return config_valid


@cli.callback()
def start_up():
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logging.getLogger().addHandler(sh)

    if check_new_version("pyhard"):
        typer.secho(
            "There is a new version of PyHard available in PyPI. Run the command to update it:\n"
            "\n\tpip install --upgrade pyhard\n",
            fg=typer.colors.YELLOW
        )


# @cli.command()
def wizard():
    """
    """
    typer.echo("Welcome to the PyHard Wizard.\n")
    typer.echo(
        "Throughout the next steps the fields of the configuration file will be set."
    )

    typer.secho("\n# General options #", fg=typer.colors.GREEN)
    typer.secho(
        "\nPlease use forward slash ('/') for paths, and also note that they can be relative to the current dir.",
        fg=typer.colors.YELLOW
    )
    rootdir = typer.prompt(
        "\nEnter the directory path ('rootdir') where the config and output files will be saved",
        default='.',
        type=Path
    )
    datafile = typer.prompt(
        "\nAnd the file path to the dataset (path/to/data.csv)",
        type=Path
    )

    class Problem(str, Enum):
        classification = 'c'
        regression = 'r'
    problem = typer.prompt(
        "\nWhat is the problem type? It should be either classification (c) or regression (r)",
        type=Problem
    )
    problem = problem.name

    target_col = typer.prompt(
        "\nThe name of the column containing target values or leave the default as the last column of the dataset",
        type=str,
        default=''
    )
    target_col = None if target_col == '' else target_col

    seed = typer.prompt(
        "\nParameter 'seed' is used to control reproducibiity. "
        "For reproducible results, set it to any integer value",
        type=int,
        default=-1
    )
    seed = None if seed == -1 else seed

    general_conf = GeneralConfig(rootdir, datafile, None, problem, target_col, seed)

    typer.secho("\n# Feature selection options #", fg=typer.colors.GREEN)
    enable_fs = typer.confirm(
        "\nThe purpose of this step is to select only the most relevant meta-features when building the meta-dataset. "
        "Do you want to enable it (recommended yes)",
        default=True,
        prompt_suffix='? '
    )
    if enable_fs:
        max_n_features = typer.prompt(
            "\nMaximum number of features to select",
            type=int,
            default=10
        )

        class Method(str, Enum):
            nca = 'NCA'
            it = 'IT'
        method = typer.prompt(
            "\nAvailable methods are Neighbourhood Component based ('NCA', recommended), "
            "or Information Theoretic based ('IT'). Which one to use",
            type=Method,
            default=Method('NCA'),
            prompt_suffix="? "
        )
        method = method.name

        var_filter = typer.confirm(
            "\nNaive variance filter removes features whose variance is smaller than a given threshold. "
            "Enable it (recommended yes)",
            default=True,
            prompt_suffix='? '
        )
        if var_filter:
            var_threshold = typer.prompt(
                "\nVariance threshold (default 0, recommended)",
                type=float,
                default=0
            )
        else:
            var_threshold = 0

        corr_filter = typer.confirm(
            "\nCorrelation filter greedly removes redundant features based on their correlation coefficient. "
            "Enable it (recommended yes)",
            default=True,
            prompt_suffix='? '
        )
        if corr_filter:
            corr_threshold = typer.prompt(
                "\nCorrelation threshold (default 0.95, recommended)",
                type=float,
                default=0.95
            )
        else:
            corr_threshold = 0.95

        fs_conf = FSConfig(
            enable_fs,
            max_n_features,
            method,
            dict(),
            var_filter,
            var_threshold,
            corr_filter,
            corr_threshold
        )
    else:
        fs_conf = FSConfig(enabled=False)

    typer.secho("\n# Hyper-parameter optimization options #", fg=typer.colors.GREEN)
    enable_hpo = typer.confirm(
        "\nDo you want to enable hyper-parameter optimization",
        default=False,
        prompt_suffix='? '
    )

    if enable_hpo:
        evals = typer.prompt(
            "\nMaximum number of evaluations (per algorithm per fold)",
            type=int,
            default=10
        )

        timeout = typer.prompt(
            "\nTimeout for each fold (in seconds)",
            type=int,
            default=90
        )

        hpo_conf = HPOConfig(enable_hpo, evals, timeout)
    else:
        hpo_conf = HPOConfig(enabled=False)

    typer.secho("\n# ISA options #", fg=typer.colors.GREEN)
    performance_threshold = typer.prompt(
        "\nPerformance threshold below which an instance is considered good",
        default='auto'
    )

    adjust_rotation = typer.confirm(
        "\nAdjust IS orientation, such that hard instances are placed in the upper left corner",
        prompt_suffix="? "
    )

    typer.echo("\nInstance hardness footprint parameters")
    ih_threshold = typer.prompt(
        "Instance easiness threshold (we recommend not to change it)",
        default=0.4,
        type=float
    )
    ih_purity = typer.prompt(
        "Purity (we recommend not to change it)",
        default=0.4,
        type=float
    )

    typer.secho("\n# Hardness measures #", fg=typer.colors.GREEN)

    default_measures = {
        'classification': [
            'kDN',
            'DCP',
            'TD_P',
            'TD_U',
            'CL',
            'CLD',
            'N1',
            'N2',
            'LSC',
            'LSR',
            'Harmfulness',
            'Usefulness',
            'F1'
        ],
        'regression': [
            'C4',
            'L1',
            'S1',
            'S2',
            'S3',
            'FO',
            'POT',
            'HB',
            'EDS',
            'EZR'
        ]
    }

    typer.echo(f"\nSuggested measures for {problem} are:")

    isa_conf = ISAConfig(
        'python',
        performance_threshold,
        adjust_rotation,
        ih_threshold,
        ih_purity
    )

    typer.secho(general_conf, fg=typer.colors.RED)
    typer.secho(fs_conf, fg=typer.colors.RED)
    typer.secho(hpo_conf, fg=typer.colors.RED)
    typer.secho(isa_conf, fg=typer.colors.RED)


@cli.command("demo")
def launch_demo():
    """
    Launches the demo application
    """
    typer.echo("Launching demo mode...")
    typer.echo("Press ^C to exit")
    demo = Demo()
    pane = demo.display()
    pane.servable()
    pane.show(title="Demo", port=5001, websocket_origin=['127.0.0.1:5001', 'localhost:5001'])


help_text_init = """
This command will generate in the current folder the following files:

config.yaml     => Provides configuration for each step of PyHard

options.json    => ISA options file
"""


@cli.command(
    help=help_text_init,
    short_help="Generates the configuration files in the current folder"
)
def init():
    """
    Generates the configuration files and saves in the current folder
    """
    src = Path(__file__).parent
    dest = Path().absolute()
    shutil.copy(src / f'conf/{_conf_file}', dest)
    save_opts(dest)
    typer.secho("Success! Config files generated.", fg=typer.colors.GREEN)


@cli.command("app")
def launch_app(
        config: Optional[Path] = typer.Option(None, exists=True, file_okay=True, help="alternative configuration file"),
        browser: bool = typer.Option(True, "--no-browser", help="whether to avoid launching the browser automatically"),
        port: int = typer.Option(5001, "--port", "-p", help="port to listen on")
):
    """
    Launches PyHard web app GUI
    """

    conf = _load_config(config)
    try:
        conf = _validate_paths(conf)
    except (NotADirectoryError, FileNotFoundError):
        _logger.exception("There are fields with invalid paths.")
        raise typer.Exit(1)

    _logger.info("Loading workspace files.")
    workspace = Workspace(conf.general.rootdir, conf.general.datafile)
    workspace.load()

    problem = conf.general.problem.lower()
    if problem == 'classification':
        app_viz = ClassificationApp(workspace)
    elif problem == 'regression':
        app_viz = RegressionApp(workspace)
    else:
        _logger.error(f"Unknown problem type '{problem}'.")
        raise typer.Exit(1)
    _logger.info(f"Type of problem: '{problem}'")

    logging.getLogger().setLevel(logging.WARNING)
    app_viz.start(port=port, show=browser)


@cli.command()
def run(
        meta: bool = typer.Option(True, "--no-meta", help="does not generate a new metadata file; uses previously "
                                                          "saved instead"),
        isa: bool = typer.Option(True, "--no-isa", help="does not execute the instance space analysis"),
        config: Optional[Path] = typer.Option(None, exists=True, file_okay=True, help="alternative configuration file"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose mode")
):
    """
    Triggers the analysis process
    """
    start = time.time()

    if verbose:
        _logger.setLevel(logging.DEBUG)

    try:
        conf = _load_config(config)
    except FileNotFoundError:
        _logger.error(f"File '{str(config) if config is not None else 'config.yaml'}' not found.")
        raise typer.Exit(1)

    # check whether paths exist
    try:
        conf = _validate_paths(conf)
    except (NotADirectoryError, FileNotFoundError):
        _logger.exception("There are fields with invalid paths.")
        raise typer.Exit(1)

    file_path = conf.general.datafile
    rootdir_path = conf.general.rootdir
    problem = conf.general.problem.lower()
    seed = conf.general.seed

    _logger.info("Reading input dataset: '{0}'".format(file_path))
    df_dataset = pd.read_csv(file_path)

    # check problem type
    if problem in {'classification', 'regression'}:
        _logger.info(f"Type of problem: '{problem}'")
    else:
        _logger.error(f"Unknown problem type '{problem}'.")
        raise typer.Exit(1)

    # basic validation tests (dtypes and NaNs)
    target_col = conf.general.target_col
    if target_col is None:
        target_col = df_dataset.columns[-1]
    try:
        has_no_missing_values(df_dataset)
        are_features_numeric(df_dataset.drop(columns=target_col))
        is_target_dtype_valid(problem, df_dataset[target_col])
    except AssertionError:
        _logger.exception("Data did not pass validation checks.")
        raise typer.Exit(1)

    # warn about class imbalance
    if problem == 'classification' and not are_classes_balanced(df_dataset[target_col]):
        _logger.warning(
            "Classes are unbalanced (imbalance ratio > 1.5). "
            "This may change the way the results are interpreted."
        )

    # set seed
    if isinstance(seed, int):
        os.environ["PYHARD_SEED"] = repr(seed)
        _logger.info(f"Seed={seed}")
    else:
        os.environ["PYHARD_SEED"] = ""
        _logger.info(f"Using random seed")

    if meta:
        _logger.info("Building metadata.")

        df_metadata, df_ih = integrator.build_metadata(
            data=df_dataset,
            config=conf,
            return_ih=True,
            verbose=verbose
        )
        df_metadata.to_csv(rootdir_path / 'metadata.csv')
        df_ih.to_csv(rootdir_path / 'ih.csv')
    else:
        try:
            df_metadata = pd.read_csv(rootdir_path / 'metadata.csv', index_col='instances')
            df_ih = pd.read_csv(rootdir_path / 'ih.csv', index_col='instances')
        except FileNotFoundError as error:
            _logger.error(f"File '{error.filename}' missing. "
                          f"Either replace it or run the analysis without '--no-meta' option.")
            raise typer.Exit(1)

    if isa:
        if conf.fs.enabled:
            min_n_features = 3
            n_feat_cols = len(df_metadata.filter(regex='^feature_').columns)
            if n_feat_cols > min_n_features:
                _logger.info("Feature selection on")

                df_metadata.to_csv(rootdir_path / 'metadata_full.csv')

                df_features = df_metadata.filter(regex='^feature_')
                df_algo = df_metadata.filter(regex='^algo_')
                features = df_features.columns
                X = df_features.values
                Y = df_algo.values

                mask = np.ones(X.shape[1], dtype=bool)
                idx = np.arange(X.shape[1])
                if conf.fs.var_filter:
                    _logger.info("Applying varicance threshold")
                    mask = variance_filter(X, threshold=conf.fs.var_threshold)
                    idx = idx[mask]
                    _logger.info(f"Removed features: {features[~mask].to_list()}")
                if conf.fs.corr_filter:
                    _logger.info("Applying correlation threshold")
                    mask2 = correlation_filter(X[:, mask], threshold=conf.fs.corr_threshold)
                    idx = idx[mask2]
                    _logger.info(f"Removed features: {features[mask][~mask2].to_list()}")

                _logger.info(f"Applying main filtering method: {conf.fs.method}")
                fs_params = {**conf.fs.parameters, **{'standardize': False}}
                selected = filtfeat(
                    X=X[:, idx],
                    Y=Y,
                    method=conf.fs.method,
                    max_n_features=conf.fs.max_n_features,
                    names=features[idx].to_list(),
                    n_jobs=-1,
                    **fs_params
                )

                if len(selected) < min_n_features:
                    _logger.warning(
                        f"An insufficient number of features has been selected ({len(selected) < min_n_features}). "
                        f"An attempt with the minimum number of features to be selected ({min_n_features}) will be made"
                    )
                    fs_params = {**fs_params, **{'n_features_to_select': min_n_features}}
                    selected = filtfeat(
                        X=X[:, idx],
                        Y=Y,
                        method=conf.fs.method,
                        max_n_features=conf.fs.max_n_features,
                        names=features[idx].to_list(),
                        n_jobs=-1,
                        **fs_params
                    )

                _logger.info(f"Selected features: {selected}")

                df_metadata = pd.concat([df_features[selected], df_algo], axis=1)
                df_metadata.to_csv(rootdir_path / 'metadata.csv')
            elif n_feat_cols == min_n_features:
                _logger.info(f"Skipping feature selection: cannot select less than {min_n_features} features.")
            else:
                _logger.error(f"Metadata does not contain the minimum number of features ({min_n_features})!")
                raise typer.Exit(1)
        else:
            _logger.info("Feature selection off")

        isa_engine = str.lower(conf.isa.engine)
        _logger.info(f"Running Instance Space Analysis with {repr(isa_engine)} engine.")
        if isa_engine == 'python':
            # changes ISA 'perf':'epsilon' option
            epsilon = conf.isa.performance_threshold
            abs_perf = True
            if epsilon == 'auto':
                if problem == 'classification':
                    n_classes = df_dataset.iloc[:, -1].nunique()
                    epsilon = loss_threshold(n_classes, metric=conf.algos.metric)
                elif problem == 'regression':
                    epsilon = np.median(np.quantile(df_metadata.filter(regex="^algo_"), q=0.9, axis=0))
                    # epsilon = 0.3
                    # abs_perf = False
            other = {'perf': {'epsilon': epsilon, 'AbsPerf': abs_perf}}

            _logger.info("Adding gaussian noise to the metadata for numerical stability.")
            df_features = df_metadata.filter(regex='^feature_')
            # df_metadata[df_features.columns] += np.random.rand(*df_features.shape) * 1e-3
            df_metadata[df_features.columns] += np.random.normal(0, 1e-3, size=df_features.shape)

            model = integrator.run_isa(
                rootdir=rootdir_path,
                metadata=df_metadata,
                settings=other,
                rotation_adjust=conf.isa.adjust_rotation,
                save_output=False,
                verbose=verbose
            )

            threshold = conf.isa.ih_threshold
            pi = conf.isa.ih_purity
            _logger.info("Calculating instance easiness footprint area")
            _logger.info(f"An instance is easy if its IH-value <= {threshold}")
            Ybin = df_ih.values[:, 0] <= threshold
            ih_fp = trace_build_wrapper(model.pilot.Z, Ybin, pi)

            # Calculate IH summary
            ih_summary = make_summary(
                space=model.trace.space,
                good=[ih_fp],
                best=[_empty_footprint()],
                algolabels=['instance_easiness']
            )
            model.trace.summary = pd.concat([model.trace.summary, ih_summary])

            # Save footprints and models
            save_footprint(ih_fp, rootdir_path, 'instance_easiness')
            scriptcsv(model, rootdir_path)
        elif isa_engine == 'matlab':
            _logger.warning("This engine will no longer be supported in future versions. Use 'python' engine instead.")
            _ = integrator.run_matilda(metadata=df_metadata, rootdir=conf.general.rootdir,
                                       matildadir=conf.general.matildadir)
        elif isa_engine == 'matlab_compiled':
            _logger.warning("This engine will no longer be supported in future versions. Use 'python' engine instead.")
            integrator.run_matilda_module(rootdir=rootdir_path)
        else:
            _logger.error(f"Unknown ISA engine '{repr(isa_engine)}'.")
            raise typer.Exit(1)

    end = time.time()
    elapsed_time = int(end - start)
    _logger.info(f"Total elapsed time: {pretty_time_delta(elapsed_time)}")

    _logger.info("Instance Hardness analysis finished.")
    typer.Exit(0)
