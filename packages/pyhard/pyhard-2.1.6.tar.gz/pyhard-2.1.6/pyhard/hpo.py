"""
Hyperparameter optimization (HPO) module. It is implemented on top of `hyperopt <http://hyperopt.github.io/hyperopt/>`_,
which is a Bayesian optimization Python package.
"""

import sys
from typing import Any, Dict, Optional, Type, Union

import numpy as np
from hyperopt import hp, tpe, fmin, space_eval, STATUS_OK
from hyperopt.pyll import scope
from sklearn.base import is_classifier, is_regressor, ClassifierMixin, RegressorMixin
from sklearn.model_selection import cross_val_score

_progressbar = True


def set_hyperopt_progressbar(flag: bool):
    global _progressbar
    _progressbar = flag


def predictor_hp_space(
        alias: str,
        predictor: Union[Type[ClassifierMixin], Type[RegressorMixin]],
        **kwargs
) -> Dict[str, Any]:
    """
    This function returns the predictor hyperparameter space, which will be searched to find the best parameters,
    given the training set.

    Args:
        alias: the predictor alias
        predictor: estimator class
        **kwargs: extra parameters

    Returns:
        dict: The predictor hyperparameter space
    """
    if is_classifier(predictor):
        func = getattr(sys.modules[__name__], f"_{alias}_hp_space")
    elif is_regressor(predictor):
        func = getattr(sys.modules[__name__], f"_{alias}_hp_space_r")
    else:
        raise ValueError
    return func(**kwargs)


def _objective(
        predictor: Union[Type[ClassifierMixin], Type[RegressorMixin]],
        params: Dict[str, Any],
        X: np.ndarray,
        y: np.ndarray
) -> Dict[str, Any]:
    predictor = predictor(**params)  # noqa
    if is_classifier(predictor):
        score = cross_val_score(predictor, X, y, cv=3, scoring='f1_micro', n_jobs=None).mean()
    elif is_regressor(predictor):
        score = cross_val_score(predictor, X, y, cv=3, scoring='neg_median_absolute_error', n_jobs=None).mean()
    else:
        raise TypeError("Predictor must be either a classifier or a regressor.")
    return {'loss': -score, 'status': STATUS_OK}


def find_best_params(
        alias: str,
        predictor: Union[Type[ClassifierMixin], Type[RegressorMixin]],
        X: np.ndarray,
        y: np.ndarray,
        fixed_params: Optional[Dict[str, Any]] = None,
        max_evals: int = 100,
        hpo_timeout: int = 90
) -> Dict[str, Any]:
    r"""
    Find the best solution searched over the hyperparameter space, minimizing a cross validation score function. It uses
    a Bayesian Optimization like method.

    Args:
        alias (str): the algorithm name, from which the search space is inferred
        predictor: a scikit-learn predictor class
        X (np.ndarray): the training dataset
        y (np.ndarray): the target values
        fixed_params (dict): set of parameters that will not be optimized
        max_evals (int): maximum number of evaluations
        hpo_timeout (int): timeout value; the search ends when either :math:`\sharp evals > max\_evals`
            or :math:`spent\_time > hpo\_timeout`

    Returns:
        dict: The best hyperparameters found
    """

    # TODO: timeout proportional to number of instances

    if fixed_params is None:
        fixed_params = dict()

    def objective(params):
        return _objective(predictor, params, X, y)

    space = predictor_hp_space(alias, predictor)
    space = {**space, **fixed_params}
    best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=max_evals,
                show_progressbar=_progressbar, timeout=hpo_timeout)

    return space_eval(space, best)


# Classifiers HP

def _random_forest_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
    :return: Random Forest parameter search space
    """
    space = {
        'n_estimators': hp.uniformint('n_estimators', 2, 200),
        'max_depth': hp.uniformint('max_depth', 1, 100),
        'criterion': hp.choice('criterion', ["gini", "entropy"])
    }
    return space


def _svc_linear_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    :return: SVM Linear parameter search space
    """
    space = {
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e3))
    }
    return space


def _svc_rbf_hp_space(n_features=10):
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    :param n_features:
    :return: SVM RBF parameter search space
    """
    space = {
        'kernel': 'rbf',
        'probability': True,
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e3)),
        'gamma': hp.loguniform('gamma', np.log(1. / n_features * 1e-1), np.log(1. / n_features * 1e1))
    }
    return space


def _gradient_boosting_hp_space():
    """
    http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
    :return: Gradient Boosting parameter search space
    """
    space = {'learning_rate': hp.lognormal('learning_rate', np.log(0.01), np.log(10.0)),
             'n_estimators': scope.int(hp.qloguniform('n_estimators', np.log(10.5), np.log(1000.5), 1)),
             'loss': hp.choice('loss', ['log_loss'])
             }
    return space


def _bagging_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html
    :return: Bagging parameter search space
    """
    space = {
        'n_estimators': hp.uniformint('n_estimators', 2, 200)
    }
    return space


def _gaussian_nb_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
    :return: Gaussian Naive Bayes classifier parameter search space
    """
    space = {
        'var_smoothing': hp.loguniform('var_smoothing', np.log(1e-9), np.log(1e-8))
    }
    return space


def _logistic_regression_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
    :return: Logistic Regression classifier parameter search space
    """
    space = {
        'C': hp.loguniform('C', np.log(1e-1), np.log(1e1))
    }
    return space


def _mlp_hp_space():
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
    :return: Multi-layer Perceptron parameter search space
    """
    space = {
        'max_iter': 300,
        'activation': hp.choice('activation', ['identity', 'logistic', 'tanh', 'relu']),
        'learning_rate': hp.choice('learning_rate', ['constant', 'invscaling', 'adaptive'])
    }
    return space


def _dummy_hp_space():
    """
    https://scikit-learn.org/0.16/modules/generated/sklearn.dummy.DummyClassifier.html
    :return: Dummy parameter search space
    """
    return {'random_state': None}


# Regressors HP

def _ada_boost_hp_space_r():
    space = {
        'n_estimators': hp.uniformint('n_estimators', 10, 150),
        'learning_rate': hp.lognormal('learning_rate', np.log(0.01), np.log(10.0)),
        'loss': hp.choice('loss', ['linear', 'square', 'exponential'])
    }
    return space


def _svr_linear_hp_space_r():
    space = {
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e3)),
        'loss': hp.choice('loss', ['epsilon_insensitive', 'squared_epsilon_insensitive'])
    }
    return space


def _svr_epsilon_hp_space_r():
    space = {
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e3)),
        'epsilon': hp.loguniform('epsilon', np.log(1e-2), np.log(1)),
    }
    return space


def _svr_nu_hp_space_r():
    space = {
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e3)),
        'nu': hp.loguniform('nu', np.log(1e-3), np.log(1)),
    }
    return space


def _decision_tree_hp_space_r():
    space = {
        'max_depth': hp.uniformint('max_depth', 1, 100),
        'criterion': hp.choice('criterion', ["squared_error", "friedman_mse", "absolute_error", "poisson"])
    }
    return space


def _random_forest_hp_space_r():
    space = {
        'n_estimators': hp.uniformint('n_estimators', 2, 200),
        'max_depth': hp.uniformint('max_depth', 1, 100),
        'criterion': hp.choice('criterion', ["squared_error", "absolute_error", "poisson"])
    }
    return space


def _extra_tree_hp_space_r():
    space = {
        'n_estimators': hp.uniformint('n_estimators', 2, 200),
        'max_depth': hp.uniformint('max_depth', 1, 100),
        'criterion': hp.choice('criterion', ["squared_error", "absolute_error"])
    }
    return space


def _gradient_boosting_hp_space_r():
    space = {
        'learning_rate': hp.lognormal('learning_rate', np.log(0.01), np.log(10.0)),
        'n_estimators': scope.int(hp.qloguniform('n_estimators', np.log(10.5), np.log(1000.5), 1)),
        'loss': hp.choice('loss', ['squared_error', 'absolute_error', 'huber']),
        'criterion': hp.choice('criterion', ['friedman_mse', 'squared_error'])
    }
    return space


def _mlp_hp_space_r():
    space = {
        'max_iter': 300,
        'activation': hp.choice('activation', ['identity', 'logistic', 'tanh', 'relu']),
        'learning_rate': hp.choice('learning_rate', ['constant', 'invscaling', 'adaptive'])
    }
    return space


def _bagging_hp_space_r():
    space = {
        'n_estimators': hp.uniformint('n_estimators', 2, 200)
    }
    return space


def _bayesian_ard_hp_space_r():
    space = {
        'alpha_1': hp.lognormal('alpha_1', np.log(1e-6), np.log(1e1)),
        'alpha_2': hp.lognormal('alpha_2', np.log(1e-6), np.log(1e1)),
        'lambda_1': hp.lognormal('lambda_1', np.log(1e-6), np.log(1e1)),
        'lambda_2': hp.lognormal('lambda_2', np.log(1e-6), np.log(1e1)),
    }
    return space


def _kernel_ridge_hp_space_r():
    space = {
        'alpha': hp.lognormal('alpha', np.log(1e-1), np.log(1e1))
    }
    return space


def _sgd_hp_space_r():
    space = {
        'alpha': hp.lognormal('alpha', np.log(1e-4), np.log(1e1)),
        'l1_ratio': hp.loguniform('l1_ratio', np.log(1e-1), np.log(1)),
    }
    return space


def _passive_aggressive_hp_space_r():
    space = {
        'C': hp.loguniform('C', np.log(1e-1), np.log(1e1))
    }
    return space


def _dummy_regressor_hp_space_r():
    return {'constant': None}
