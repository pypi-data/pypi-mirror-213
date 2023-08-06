"""
Module that implements the Hardness Measures, for both classification and regression.
"""

import itertools
import logging

import numpy as np
import pandas as pd
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.stats import iqr
from sklearn import tree
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import DistanceMetric
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from . import get_seed
from .base import Measures


def minmax(f: np.ndarray, y: np.ndarray) -> float:
    r"""
    For binary classes, calculates :math:`\min \max (f_i) = \min ( \max (f^{c_1}_i), \max (f^{c_2}_i) )`, where
    :math:`f^{c_j}_i` is the i-th feature values for members of class :math:`c_j`.

    Args:
        f (array-like): i-th feature vector
        y (array-like): corresponding class vector

    Returns:
        float: minmax value

    Raises:
        AssertionError: If classes are not binary

    """
    classes = np.unique(y)
    assert len(classes) == 2
    c1 = classes[0]
    c2 = classes[1]
    return min(np.max(f[y == c1]), np.max(f[y == c2]))


def maxmin(f: np.ndarray, y: np.ndarray):
    r"""
    For binary classes, calculates :math:`\max \min (f_i) = \max ( \min (f^{c_1}_i), \min (f^{c_2}_i) )`, where
    :math:`f^{c_j}_i` is the i-th feature values for members of class :math:`c_j`.

    Args:
        f (array-like): i-th feature vector
        y (array-like): corresponding class vector

    Returns:
        float: maxmin value

    Raises:
        AssertionError: If classes are not binary

    """
    classes = np.unique(y)
    assert len(classes) == 2
    c1 = classes[0]
    c2 = classes[1]
    return max(np.min(f[y == c1]), np.min(f[y == c2]))


def maxmax(f: np.ndarray, y: np.ndarray):
    r"""
    For binary classes, calculates :math:`\max \max (f_i) = \min ( \max (f^{c_1}_i), \max (f^{c_2}_i) )`, where
    :math:`f^{c_j}_i` is the i-th feature values for members of class :math:`c_j`.

    Args:
        f (array-like): i-th feature vector
        y (array-like): corresponding class vector

    Returns:
        float: maxmax value

    Raises:
        AssertionError: If classes are not binary

    """
    classes = np.unique(y)
    assert len(classes) == 2
    c1 = classes[0]
    c2 = classes[1]
    return max(np.max(f[y == c1]), np.max(f[y == c2]))


def minmin(f: np.ndarray, y: np.ndarray):
    r"""
    For binary classes, calculates :math:`\min \min (f_i) = \min ( \min (f^{c_1}_i), \min (f^{c_2}_i) )`, where
    :math:`f^{c_j}_i` is the i-th feature values for members of class :math:`c_j`.

    Args:
        f (array-like): i-th feature vector
        y (array-like): corresponding class vector

    Returns:
        float: minmin value

    Raises:
        AssertionError: If classes are not binary

    """
    classes = np.unique(y)
    assert len(classes) == 2
    c1 = classes[0]
    c2 = classes[1]
    return min(np.min(f[y == c1]), np.min(f[y == c2]))


def gower_distance(X: pd.DataFrame) -> np.ndarray:
    """
    Calculates the Gower's distance (similarity). The samples may contain both categorical and numerical features. It
    returns a value between 0 (identical) and 1 (maximally dissimilar).

    Args:
        X (pd.DataFrame): the feature matrix

    Returns:
        float: coefficient measuring the similarity between two samples.
    """
    N = len(X)
    n_feat = X.shape[1]
    cumsum_dist = np.zeros((N, N))

    for i in range(n_feat):
        feature = X.iloc[:, [i]]
        if feature.dtypes[0] == object:
            feature_dist = DistanceMetric.get_metric('dice').pairwise(pd.get_dummies(feature))
        else:
            feature_dist = DistanceMetric.get_metric('manhattan').pairwise(feature)
            feature_dist /= max(np.ptp(feature.values), 1e-8)

        cumsum_dist += feature_dist * 1 / n_feat

    return cumsum_dist


class ClassificationMeasures(Measures):
    """
    Hardness measures for classification. It provides separate methods to compute each measure.

    Args:
        data (pd.DataFrame): a dataframe where each line is an instace and columns are features. One column should
            contain the labels. The name of the column with labels can be set with parameter `labels_col`
        target_col (str): name of the column that contains the labels of the instances (default None - uses the
            last column)
        ccp_alpha (float): pruning parameter for pruned tree measures. If none is passed, then it attempts to tune
            it automatically
    """

    _measures_dict = {
        'kDN': 'k_disagreeing_neighbors',
        'DS': 'disjunct_size',
        'DCP': 'disjunct_class_percentage',
        'TD_P': 'tree_depth_pruned',
        'TD_U': 'tree_depth_unpruned',
        'CL': 'class_likeliood',
        'CLD': 'class_likeliood_diff',
        'MV': 'minority_value',
        'CB': 'class_balance',
        'N1': 'borderline_points',
        'N2': 'intra_extra_ratio',
        'LSC': 'local_set_cardinality',
        'LSR': 'ls_radius',
        'Harmfulness': 'harmfulness',
        'Usefulness': 'usefulness',
        'F1': 'f1',
        'F2': 'f2',
        'F3': 'f3',
        'F4': 'f4'
    }

    logger = logging.getLogger(__name__)

    def __init__(self, data: pd.DataFrame, target_col=None, ccp_alpha=None):
        if target_col is None:
            self.target_col = data.columns[-1]
            self.y = data.iloc[:, -1]
        else:
            self.target_col = target_col
            self.y = data[target_col]
        self.data = data.reset_index(drop=True)
        self.X = data.drop(columns=self.target_col)
        self.N = len(data)

        seed = get_seed()

        # Decision Tree Classifier
        dtc = tree.DecisionTreeClassifier(min_samples_split=2, criterion='gini', random_state=seed)
        self.dtc = dtc.fit(self.X.values, self.y.values)

        # Decision Tree Classifier Pruned
        if ccp_alpha is None:
            parameters = {'ccp_alpha': np.linspace(0.001, 0.1, num=100)}
            dtc = tree.DecisionTreeClassifier(criterion='gini', random_state=seed)
            clf = GridSearchCV(dtc, parameters, n_jobs=-1)
            clf.fit(self.X.values, self.y.values)
            ccp_alpha = clf.best_params_['ccp_alpha']

        self.dtc_pruned = tree.DecisionTreeClassifier(criterion='gini', ccp_alpha=ccp_alpha, random_state=seed)
        self.dtc_pruned = self.dtc_pruned.fit(self.X.values, self.y.values)

        # Naive Bayes classifier
        n_c = self.y.nunique()
        priors = np.ones((n_c,)) / n_c

        nb = GaussianNB(priors=priors)
        self.calibrated_nb = CalibratedClassifierCV(base_estimator=nb, method='sigmoid',
                                                    cv=3, ensemble=False, n_jobs=-1)
        self.calibrated_nb.fit(self.X, self.y)

        # Gower distance matrix
        # self.dist_matrix_gower = gower.gower_matrix(self.X.values.copy())
        self.dist_matrix_gower = gower_distance(self.X)
        delta = np.diag(-np.ones(self.dist_matrix_gower.shape[0]))
        self.indices_gower = np.argsort(self.dist_matrix_gower + delta, axis=1)
        self.distances_gower = np.sort(self.dist_matrix_gower, axis=1)

        self.dot = None

    def k_disagreeing_neighbors(self, k: int = 10, distance: str = 'gower') -> np.ndarray:
        r"""
        k-Disagreeing Neighbors (kDN) gives the percentage of the :math:`k` nearest neighbors of :math:`\\mathbf x_i`
        which do not share its label.

        .. math::

            kDN(\mathbf{x_i}) = \frac{ \sharp \{\mathbf x_j | \mathbf x_j \in kNN(\mathbf x_i) \wedge y_j
            \neq y_i\}}{k}

        Args:
            k (int): number of neighbors
            distance (str): distance metric (default 'gower')

        Returns:
            array-like: :math:`kDN(\mathbf x_i)`
        """
        data = self.data.copy()
        if distance == 'gower':
            indices = self.indices_gower[:, :k + 1]
        else:
            nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm='auto').fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        kDN = []
        for i in range(0, len(data)):
            v = data.loc[indices[i]][self.target_col].values
            kDN.append(np.sum(v[1:] != v[0]) / k)
        return np.array(kDN)

    def disjunct_size(self) -> np.ndarray:
        data = self.data.copy()

        data['leaf_id'] = self.dtc.apply(self.X.values)
        df_count = data.groupby('leaf_id').count().iloc[:, 0].to_frame('count').subtract(1)
        data = data.join(df_count, on='leaf_id')
        DS = data['count'].divide(data['count'].max())

        return 1 - DS.values

    def disjunct_class_percentage(self) -> np.ndarray:
        r"""
        Disjunct Class Percentage (DCP) builds a decision tree using :math:`\mathcal{D}` and considers the percentage
        of instances in the disjunct of :math:`\mathbf x_i` which share the same label as :math:`\mathbf x_i`.
        The disjunct of an example corresponds to the leaf node where it is classified by the decision tree.

        .. math::

            DCP(\mathbf x_i) = 1- \frac{\sharp\{\mathbf x_j | \mathbf x_j \in Disjunct(\mathbf x_i) \wedge y_j = y_i\}}
            {\sharp\{\mathbf x_j|\mathbf x_j \in Disjunct(\mathbf x_i)\}}

        Returns:
            array-like: :math:`DCP(\mathbf x_i)`
        """
        data = self.data.copy()

        data['leaf_id'] = self.dtc_pruned.apply(self.X.values)
        dcp = []
        for index, row in data.iterrows():
            df_leaf = data[data['leaf_id'] == row['leaf_id']]
            dcp.append(len(df_leaf[df_leaf[self.target_col] == row[self.target_col]]) / len(df_leaf))

        return 1 - np.array(dcp)

    def tree_depth_unpruned(self) -> np.ndarray:
        r"""
        Tree Depth (TD) returns the depth of the leaf node that classifies :math:`\mathbf x_i` in a  decision tree,
        normalized by the maximum depth of the tree built from :math:`D`:

        .. math::

            TD(\mathbf x_i) = \frac{depth(\mathbf x_i)}{\max(depth(D))}

        There are two versions of this measure, using pruned (:math:`TD_P(\mathbf x_i)`)
        and unpruned (:math:`TD_U(\mathbf x_i)`) decision trees. Instances harder to classify tend to be placed
        at deeper levels of the trees and present higher :math:`TD` values.

        Returns:
            array-like: :math:`TD_U(\mathbf x_i)`
        """
        return self.X.apply(lambda x: self.dtc.decision_path([x]).sum() - 1,
                            axis=1, raw=True).values / self.dtc.get_depth()

    def tree_depth_pruned(self) -> np.ndarray:
        r"""
        Tree Depth (TD) returns the depth of the leaf node that classifies :math:`\mathbf x_i` in a  decision tree,
        normalized by the maximum depth of the tree built from :math:`D`:

        .. math::

            TD(\mathbf x_i) = \frac{depth(\mathbf x_i)}{\max(depth(D))}

        There are two versions of this measure, using pruned (:math:`TD_P(\mathbf x_i)`)
        and unpruned (:math:`TD_U(\mathbf x_i)`) decision trees. Instances harder to classify tend to be placed
        at deeper levels of the trees and present higher :math:`TD` values.

        Returns:
            array-like: :math:`TD_P(\mathbf x_i)`
        """
        return self.X.apply(lambda x: self.dtc_pruned.decision_path([x]).sum() - 1,
                            axis=1, raw=True).values / self.dtc_pruned.get_depth()

    def class_likeliood(self) -> np.ndarray:
        r"""
        Class Likelihood (CL) measures the likelihood that :math:`\mathbf x_i` belongs to its class:

        .. math::

            CL(\mathbf x_i) = 1 - P(\mathbf x_i|y_i)P(y_i)

        where :math:`P(\mathbf x_i|y_i)` represents the likelihood that :math:`\mathbf x_i` belongs to class
        :math:`y_i`, measured in :math:`D`, and :math:`P(y_i)` is the prior of class :math:`y_i`, which we set
        as :math:`\\frac{1}{n}` for all data instances. For ease of computation, the conditional probability
        :math:`P(\mathbf x_i|y_i)` can be estimated considering each of the input features independent from each other,
        as done in Naive Bayes classification. Larger class likelihood values are expected for easier instances,
        so we output the complement of this value.

        Returns:
            array-like: :math:`CL(\mathbf x_i)`
        """
        proba = self.calibrated_nb.predict_proba(self.X)

        y = self.y.values.reshape(-1, 1)
        classes = self.calibrated_nb.classes_.reshape((1, -1))
        CL = proba[np.equal(y, classes)]

        return 1 - CL

    def class_likeliood_diff(self) -> np.ndarray:
        r"""
        Class Likelihood Difference (CLD) takes the difference between the likelihood of :math:`\mathbf x_i` in
        relation to its class and the maximum likelihood it has to any other class.

        .. math::

            CLD(\mathbf x_i) = \frac{1 -\left (P(\mathbf x_i|y_i)P(y_i) - \max_{y_j \neq y_i}
            [P(\mathbf x_i |y_j)P(y_j)]\right )}{2}

        The difference in the class likelihood is larger for easier instances, because the confidence it belongs to its
        class is larger than that of any other class. We take the complement of the measure as indicated in the
        equation above.

        Returns:
            array-like: :math:`CLD(\mathbf x_i)`
        """
        proba = self.calibrated_nb.predict_proba(self.X)

        y = self.y.values.reshape(-1, 1)
        classes = self.calibrated_nb.classes_.reshape((1, -1))
        CL = proba[np.equal(y, classes)]
        CLD = CL - np.max(proba[~np.equal(y, classes)].reshape((self.N, -1)), axis=1)

        return (1 - CLD) / 2

    def minority_value(self) -> np.ndarray:
        r"""
        Also measures the skewness of :math:`\mathbf x_i`'s class, with an alternative formulation based on the
        imbalance ratio of the class the instance belongs to:

        .. math::

            MV(\mathbf x_i) = 1 - \frac{\sharp\{\mathbf x_j | y_j = y_i\}}{\max_{y_j \in \mathcal Y}
            \left\{\sharp\{\mathbf x_j|\mathbf x_j \in y_j\}\right\}}

        Returns:
            array-like: :math:`MV(\mathbf x_i)`
        """
        mv_class = self.data.groupby(self.target_col).count().iloc[:, 0]
        mv_class = mv_class.divide(mv_class.max())

        labels = self.y
        return labels.apply(lambda c: 1 - mv_class[c]).values

    def class_balance(self) -> np.ndarray:
        r"""
        Measures the skewness of :math:`\mathbf x_i`'s class as:

        .. math::

            CB(\mathbf x_i) = \left( 1 - \frac{ \sharp\{\mathbf x_j | y_j = y_i\}}{n} + \frac{1}{C} \right)
            \left( \frac{C}{C+1}\right)

        where :math:`n` is the number of instances in the dataset :math:`\mathcal D` and :math:`C` is the number of
        classes the problem has.

        Returns:
            array-like: :math:`CB(\mathbf x_i)`
        """
        cb_class = self.data.groupby(self.target_col).count().iloc[:, 0]
        cb_class = cb_class.divide(self.N) - 1 / len(self.y.unique())

        labels = self.y
        n_classes = self.y.nunique()
        return (1 - labels.apply(lambda c: cb_class[c]).values) * n_classes / (n_classes + 1)

    def borderline_points(self) -> np.ndarray:
        r"""
        Fraction of nearby instances of different classes (N1): in this measure, first a minimum spanning tree (MST) is
        built from :math:`D`. In this tree, each instance of the dataset :math:`D` corresponds to one vertex and nearby
        instances are connected according to their distances in the input space in order to obtain a tree of minimal
        cost concerning the sum of the edges' weights. :math:`N_1` gives the percentage of instances of different
        classes :math:`\mathbf x_i` is connected to in the MST.

        .. math::

            N_1(\mathbf x_i) = \frac{\sharp \{\mathbf x_j | (\mathbf x_i,\mathbf x_j) \in MST(D) \wedge y_i \neq y_j\}}
            {\sharp \{\mathbf x_j | (\mathbf x_i,\mathbf x_j) \in MST(D)\}}

        Larger values of :math:`N_1(\mathbf x_i)` indicate that :math:`\mathbf x_i` is close to examples of different
        classes, either because it is borderline or noisy, making it hard to classify.

        Returns:
            array-like: :math:`N_1(\mathbf x_i)`
        """
        y = self.y.values.copy()

        dist_matrix = self.dist_matrix_gower
        Tcsr = minimum_spanning_tree(dist_matrix)
        mst = Tcsr.toarray()
        mst = np.where(mst > 0, mst, np.inf)

        N1 = np.zeros(y.shape)
        for i in range(len(y)):
            idx = np.argwhere(np.minimum(mst[i, :], mst[:, i]) < np.inf)
            N1[i] = np.sum(y[idx[:, 0]] != y[i]) / len(y[idx[:, 0]])
        return N1

    def intra_extra_ratio(self, distance='gower') -> np.ndarray:
        r"""
        Ratio of the intra-class and extra-class distances (N2): first the ratio of the distance of :math:`\mathbf x_i`
        to the nearest example from its class to the distance it has to the nearest instance from a different class
        (aka nearest enemy) is computed:

        .. math::

            IntraInter(\mathbf x_i) = \frac{d(\mathbf x_i,NN(\mathbf x_i) \in y_i)}{d(\mathbf x_i, ne(\mathbf x_i))}

        where :math:`NN(\mathbf x_i)` represents a nearest neighbor of :math:`\mathbf x_i` and :math:`ne(\mathbf x_i)`
        is the nearest enemy of :math:`\mathbf x_i`:

        .. math::

            ne(\mathbf x_i) = NN(\mathbf x_i) \in y_j \neq y_i

        Then :math:`N_2` is taken as:

        .. math::

            N_2(\mathbf x_i) = 1 - \frac{1}{IntraInter(\mathbf x_i) + 1}

        Larger values of :math:`N2(\mathbf x_i)` indicate that the instance :math:`\mathbf x_i` is closer to an example
        from another class than to an example from its own class and is, therefore, harder to classify.

        Args:
            distance (str): the distance metric to use (default `'gower'`). See `this link
                <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
                #sklearn.neighbors.DistanceMetric>`_ for a list of available metrics.

        Returns:
            array-like: :math:`N_2(\mathbf x_i)`
        """
        y = self.y.copy()

        if distance == 'gower':
            indices = self.indices_gower
            distances = self.distances_gower
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=distance).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        N2 = np.zeros(y.values.shape)
        for i, label in y.items():
            nn = y.loc[indices[i, :]]
            intra = nn.eq(label)
            extra = nn.ne(label)
            assert np.all(np.diff(distances[i, intra]) >= 0)
            assert np.all(np.diff(distances[i, extra]) >= 0)
            N2[i] = distances[i, intra][1] / max(distances[i, extra][0], 1e-15)
        return 1 - 1 / (N2 + 1)

    def local_set_cardinality(self, distance='gower') -> np.ndarray:
        r"""
        Local Set Cardinality (LSC): the Local-Set (LS) of an instance :math:`\mathbf x_i` is the set of points from
        :math:`D` whose distances to :math:`\mathbf x_i` are smaller than the distance between :math:`\mathbf x_i` and
        :math:`\mathbf x_i`'s nearest enemy. :math:`LSC` outputs the relative cardinality of such set:

        .. math::

            LSC(\mathbf x_i) = 1 - \frac{|LS(\mathbf x_i)|}{\sharp\{\mathbf x_j|y_i=y_j\}}

            LS(\mathbf x_i) = \sharp\{\mathbf x_j | d(\mathbf x_i, \mathbf x_j) < d(\mathbf x_i, ne(\mathbf x_i))\}

        where :math:`ne(\mathbf x_i)` is the nearest enemy of :math:`\mathbf x_i`, that is, the example from another
        class that is closest to :math:`\mathbf x_i`. Larger local sets are obtained for easier examples, which are in
        dense regions surrounded by instances from their own classes.

        Args:
            distance (str): the distance metric to use (default `'gower'`). See `this link
                <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
                #sklearn.neighbors.DistanceMetric>`_ for a list of available metrics.

        Returns:
            array-like: :math:`LSC(\mathbf x_i)`
        """
        y = self.y.copy()

        if distance == 'gower':
            indices = self.indices_gower
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=distance).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        LSC = np.zeros(y.values.shape)
        n_class = y.value_counts()
        for i, label in y.items():
            nn = y.loc[indices[i, :]].values
            LSC[i] = np.argmax(nn != label) / n_class[label]
        return 1 - LSC

    def ls_radius(self, distance='gower') -> np.ndarray:
        r"""
        Local Set Radius (LSR) takes the normalized radius of the local set of :math:`\mathbf x_i`:

        .. math::

            LSR(\mathbf x_i) = 1 - \min \left \{1,\frac{d(\mathbf x_i, ne(\mathbf x_i))}{\max(d(\mathbf x_i,\mathbf x_j)
            |y_i=y_j)} \right \}

        Larger radiuses are expected for easier instances, so we take the complement of such measure.

        Args:
            distance (str): the distance metric to use (default `'gower'`). See `this link
                <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
                #sklearn.neighbors.DistanceMetric>`_ for a list of available metrics.

        Returns:
            array-like: :math:`LSR(\mathbf x_i)`
        """
        y = self.y.copy()

        if distance == 'gower':
            indices = self.indices_gower
            distances = self.distances_gower
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=distance).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        LSR = np.zeros(y.values.shape)
        for i, label in y.items():
            nn = y.loc[indices[i, :]].values
            aux = (nn == label)[::-1]
            ind_nn_max = len(aux) - np.argmax(aux) - 1
            LSR[i] = min(1.0, distances[i, np.argmax(nn != label)] / distances[i, ind_nn_max])
        return 1 - LSR

    def harmfulness(self, distance='gower') -> np.ndarray:
        r"""
        Harmfulness (H): number of instances having :math:`\mathbf x_i` as their nearest enemy.

        .. math::

            H(\mathbf x_i) = \frac{\sharp\{\mathbf x_j | ne(\mathbf x_j) = \mathbf x_i \}}{\sharp\{\mathbf x_j|y_i
            \neq y_j\}}

        If :math:`\mathbf x_i` is the nearest enemy of many instances, this indicates it is harder to classify and its
        harmfulness will be higher.

        Args:
            distance (str): the distance metric to use (default `'gower'`). See `this link
                <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
                #sklearn.neighbors.DistanceMetric>`_ for a list of available metrics.

        Returns:
            array-like: :math:`H(\mathbf x_i)`
        """
        y = self.y.values.copy()

        if distance == 'gower':
            indices = self.indices_gower
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=distance).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        ne_pos = np.argmax(y[indices] != y[:, None], axis=1)
        ne = indices[np.arange(len(indices)), ne_pos]
        n_class = self.y.value_counts()

        H = np.sum(np.reshape(np.arange(self.N), (self.N, -1)) == ne, axis=1)
        return H / (self.N - n_class[self.y].values)

    def usefulness(self, distance='gower') -> np.ndarray:
        r"""
        Usefulness (U) corresponds to the fraction of instances having :math:`\mathbf x_i` in their local sets .

        .. math::

            U(\mathbf x_i) = 1 - \frac{\sharp \{\mathbf x_j| d(\mathbf x_i,\mathbf x_j) < d(\mathbf x_j,
            ne(\mathbf x_j))\}}{{\sharp\{\mathbf x_j|y_i=y_j\}}}

        If :math:`\mathbf x_i` is easy to classify, it will be close to many examples from its class and therefore will
        be more useful. We take the complement of this measure as output.

        Args:
            distance (str): the distance metric to use (default `'gower'`). See `this link
                <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
                #sklearn.neighbors.DistanceMetric>`_ for a list of available metrics.

        Returns:
            array-like: :math:`U(\mathbf x_i)`
        """
        y = self.y.values.copy()

        if distance == 'gower':
            indices = self.indices_gower
        else:
            nbrs = NearestNeighbors(n_neighbors=len(self.y), algorithm='auto', metric=distance).fit(self.X)
            distances, indices = nbrs.kneighbors(self.X)

        ne_pos = np.argmax(y[indices] != y[:, None], axis=1)
        n_class = self.y.value_counts()

        u = np.zeros(y.shape)
        for i in range(self.N):
            ls = indices[i, 1:ne_pos[i]]
            u[ls] += 1
        return 1 - (u / n_class[self.y].values)

    def f1(self) -> np.ndarray:
        r"""
        Fraction of features in overlapping areas (F1) takes the percentage of features of the instance
        :math:`\mathbf x_i` whose values lie in an overlapping region of the classes as:

        .. math::

            F_1(\mathbf x_i) = \frac{\sum_{j=1}^{m_D}{I(x_{ij} \geq \textnormal{max_min} (\mathbf f_j)
            \wedge x_{ij} \leq \textnormal{min_max} (\mathbf f_j))}}{m_D},

        where :math:`I` is the indicator function, which returns 1 if its argument is true and 0 otherwise,
        :math:`\mathbf f_j` is the :math:`j`-th feature vector in :math:`D` and:

        .. math::

            \textnormal{min_max}(\mathbf f_j) = \min(\max(\mathbf f_j^{c_1}),\max(\mathbf f_j^{c_2}))
            \\
            \textnormal{max_min}(\mathbf f_j) = \max(\min(\mathbf f_j^{c_1}),\min(\mathbf f_j^{c_2}))

        The values :math:`\max(\mathbf f_j^{y_i})` and :math:`\min(\mathbf f_j^{y_i})` are the maximum and minimum
        values of :math:`\mathbf f_j` in a class :math:`y_i \in \{c_1, c_2\}`. According to the previous definition,
        the overlap for a feature :math:`\mathbf f_j` is measured according to the maximum and minimum values it assumes
        in the different classes and one may regard a feature as having overlap if it is not possible to separate the
        classes using a threshold on that feature's values. :math:`F_1` defines instance hardness according to whether
        the example is in one or more of the feature overlapping regions a dataset has. Larger values of :math:`F_1` are
        obtained for data instances which lie in overlapping regions for most of the features, implying they are harder
        according to the :math:`F_1` interpretation. Multiclass classification problems are first decomposed into
        multiple pairwise binary classification problems, whose results are averaged.

        Returns:
            array-like: :math:`F_1(\mathbf x_i)`
        """
        df = self.data.copy()
        features = self.X.columns.to_list()
        n_features = len(features)
        classes = self.y.unique().tolist()

        F1 = pd.Series(0, index=df.index)
        for p in itertools.combinations(classes, 2):
            sub_df = df[(self.y == p[0]) | (self.y == p[1])]
            indicator = pd.Series(0, index=sub_df.index)
            for f in features:
                m1 = maxmin(sub_df[f].values, sub_df[self.target_col].values)
                m2 = minmax(sub_df[f].values, sub_df[self.target_col].values)
                indicator += sub_df[f].between(m1, m2, inclusive='both') * 1
            F1 = F1.add(indicator.divide(n_features), fill_value=0)

        F1 = F1.divide(len(classes) - 1)
        return F1.values

    def do_t(self):
        df = self.data.copy()
        features = self.X.columns.to_list()
        classes = self.y.unique().tolist()

        dot = pd.DataFrame(0, columns=self.X.columns, index=self.X.index)
        for p in itertools.combinations(classes, 2):
            sub_df = df[(self.y == p[0]) | (self.y == p[1])]
            for f in features:
                m1 = maxmin(sub_df[f].values, sub_df[self.target_col].values)
                m2 = minmax(sub_df[f].values, sub_df[self.target_col].values)
                do = (m2 - sub_df[f]) / (m2 - m1)
                dot[f] = dot[f].add(1 / (1 + abs(0.5 - do)), fill_value=0)

        k = len(classes)
        dot = dot.div(k * (k - 1) / 2)
        return dot

    def f2(self) -> np.ndarray:
        if self.dot is None:
            self.dot = self.do_t()
        return self.dot.min(axis=1).values

    def f3(self) -> np.ndarray:
        if self.dot is None:
            self.dot = self.do_t()
        return self.dot.mean(axis=1).values

    def f4(self) -> np.ndarray:
        if self.dot is None:
            self.dot = self.do_t()
        return self.dot.max(axis=1).values


class RegressionMeasures(Measures):
    """
    Hardness measures for regression. It provides separate methods to compute each measure.

    Args:
        data (pd.DataFrame): a dataframe where each line is an instace and columns are features. One column should
            contain the target value. The name of the column with targets can be set with parameter `labels_col`
        target_col (str): name of the column that contains the labels of the instances (default None - uses the
            last column)
    """

    # measure_name : function_name
    _measures_dict = {
        'C4': 'collective_feature_efficiency',
        'L1': 'linear_absolute_error',
        'S1': 'output_distribution',
        'S2': 'input_distribution',
        'S3': 'error_nn_regressor',
        'FO': 'feature_outlier',
        'POT': 'target_outlier',
        'HB': 'histogram_bin',
        'EDS': 'stump_error',
        'EZR': 'zero_rule_error',
        'DS': 'disjunct_size',
        'TD_P': 'tree_depth_pruned',
        'TD_U': 'tree_depth_unpruned',
        'D': 'density',
        'CC': 'clustering_coefficient'
    }

    logger = logging.getLogger(__name__)

    def __init__(self, data: pd.DataFrame, target_col=None, ccp_alpha=None, eps=0.15):
        if target_col is None:
            self.target_col = data.columns[-1]
            self.y = data.iloc[:, -1].values
        else:
            self.target_col = target_col
            self.y = data[target_col].values

        self.data = data.reset_index(drop=True)
        self.X = data.drop(columns=self.target_col).values
        self.N, self.n_feat = self.X.shape

        # scaled data
        self.X_scaled = StandardScaler().fit_transform(self.X)
        self.y_scaled = (self.y - self.y.mean()) / self.y.std()

        self.dist_matrix_gower = gower_distance(data.drop(columns=self.target_col))
        # delta = np.diag(-np.ones(self.dist_matrix_gower.shape[0]))
        # self.indices_gower = np.argsort(self.dist_matrix_gower + delta, axis=1)
        # self.distances_gower = np.sort(self.dist_matrix_gower, axis=1)

        # use it for random_state
        seed = get_seed()

        # Decision Tree Regressor
        dtr = tree.DecisionTreeRegressor(min_samples_split=2, criterion='squared_error', random_state=seed)
        self.dtr = dtr.fit(self.X_scaled, self.y_scaled)

        # Decision Tree Regressor Pruned
        if ccp_alpha is None:
            parameters = {'ccp_alpha': np.linspace(0.001, 0.1, num=100)}
            dtr = tree.DecisionTreeRegressor(criterion='squared_error', random_state=seed)
            clf = GridSearchCV(dtr, parameters, n_jobs=-1)
            clf.fit(self.X_scaled, self.y_scaled)
            ccp_alpha = clf.best_params_['ccp_alpha']

        self.dtr_pruned = tree.DecisionTreeRegressor(criterion='squared_error', ccp_alpha=ccp_alpha, random_state=seed)
        self.dtr_pruned = self.dtr_pruned.fit(self.X_scaled, self.y_scaled)

        # Build adjacency matrix to generate graph dataset
        self.adjacency_matrix = np.where(self.dist_matrix_gower >= eps, 1, 0)
        np.fill_diagonal(self.adjacency_matrix, 0)

    def collective_feature_efficiency(self, epsilon: float = 0.1) -> np.ndarray:
        r"""
        This measure starts by identifying the feature with the highest correlation to the output in :math:`D`. All
        examples with a small residual value (:math:`|\varepsilon_i| \leq 0.1`) after a linear fit between this feature
        and the target attribute are removed. Then, the most correlated feature to the remaining data points is found
        and the previous process is repeated until all features have been analyzed or no example remains. For an
        instance :math:`\mathbf x_i`, we take the round :math:`l_i` where it is removed from the analysis, or output
        the value 1 if it remains.

        .. math::

            C_4(\mathbf x_i) = \frac{l_i}{m+1}

        if :math:`\mathbf x_i` is removed in one of the :math:`C_4` rounds. Otherwise, the :math:`l_i` value is set as
        :math:`m+1`. Higher :math:`C_4` values are obtained for harder instances, which require more features to get a
        linear fit. The :math:`C_4` values range in :math:`\left[\frac{1}{m+1},1\right]`.

        Args:
            epsilon (float): residual value threshold

        Returns:
            array-like: Collective feature efficiency values per instance.
        """
        C4 = np.ones(self.y.shape)

        for i in range(self.n_feat):
            x_feat = self.X_scaled[:, i].reshape(-1, 1)
            lr = LinearRegression(fit_intercept=False)
            lr.fit(x_feat, self.y_scaled)
            y_pred = lr.predict(x_feat)
            resid = np.abs(self.y_scaled - y_pred)
            mask = resid <= epsilon
            C4[mask] = (i + 1) / (self.n_feat + 1)

        return C4

    def linear_absolute_error(self) -> np.ndarray:
        r"""
        First a statistical model of a Multiple Linear Regression is fit to :math:`D`. For each :math:`\mathbf x_i`
        a residual or error :math:`\varepsilon_i` in relation to the actual output :math:`y_i` can be measure and
        :math:`L_1` is given as:

        .. math::

            L_1(\mathbf x_i) = |\varepsilon_i|.

        Larger values are attained for harder instances.

        Returns:
            array-like: Absolute error after linear fit values per instance.
        """
        lr = LinearRegression(fit_intercept=False)
        lr.fit(self.X_scaled, self.y_scaled)
        y_pred = lr.predict(self.X_scaled)
        L1 = np.abs(self.y_scaled - y_pred)
        L1_normalized = 1 - 1/(1 + L1)
        return L1_normalized

    def output_distribution(self) -> np.ndarray:
        r"""
        As in :math:`N_1` for classification, first a MST is generated from input data. Next :math:`S_1` monitors
        whether the instances joined in the MST have similar output values. An instance :math:`\mathbf x_i` can have
        multiple neighbors in the MST. So, take the average of the differences between their outputs:

        .. math::

            S_1(\mathbf x_i) = \frac{1}{n_i}\sum_{i:j \in MST} |y_i - y_j|

        where :math:`n_i` is the number of neighbors of :math:`\mathbf x_i` in the MST. Higher values will be obtained
        for harder instances, which are connected to examples with dissimilar outputs.

        Returns:
            array-like: Output distribution measure values per instance.
        """
        Tcsr = minimum_spanning_tree(self.dist_matrix_gower)  # noqa

        adjacency = Tcsr.maximum(Tcsr.T)
        S1 = adjacency.sum(axis=1) / np.sum(adjacency > 0, axis=1)
        S1 = np.squeeze(np.asarray(S1))

        return S1

    def input_distribution(self) -> np.ndarray:
        r"""
        :math:`S_2` first orders the data points according to their output values :math:`y_i` and then computes the
        Euclidean distance between pairs of examples that are neighbors. In the ordering, each element will have one or
        two neighbor examples. For two neighbors, the average should be taken. Otherwise, if the example is the first or
        the last in the ordering, the unique neighborhood difference is output. Given that
        :math:`y_1 \leq y_2 \leq \ldots \leq y_n`, that is, that the examples are already ordered according to their
        output values, we have:

        .. math::

            S_2(\mathbf x_i) = \frac{d(\mathbf x_i,\mathbf x_{i-1})+d(\mathbf x_i,\mathbf x_{i+1})}{2}

        for :math:`2<i<n-1`. For :math:`i=1`:

        .. math::

            S_2(\mathbf x_1) = d(\mathbf x_1,\mathbf x_2)

        And for :math:`i=n`:

        .. math::

            S_2(\mathbf x_n) = d(\mathbf x_n,\mathbf x_{n-1})

        Larger values are obtained for harder instances.

        Returns:
            array-like: Input distribution measure values per instance.
        """
        idx = np.argsort(self.y)
        y_ord = self.y_scaled[idx]
        X_ord = self.X_scaled[idx, :]

        d1 = np.linalg.norm(np.diff(X_ord, axis=0), ord=2, axis=1)
        d2 = np.linalg.norm(np.diff(X_ord[::-1, :], axis=0)[::-1, :], ord=2, axis=1)

        S2 = np.zeros(y_ord.shape[0])
        aux = np.zeros(y_ord.shape[0])
        aux[1:] += d1
        aux[:-1] += d2
        aux[1:-1] *= 1 / 2
        S2[idx] = aux

        return 1 - 1 / (1 + S2)

    def error_nn_regressor(self) -> np.ndarray:
        r"""
        Calculates the squared error (SE) of a *1-nearest neighbor regressor* (NN), using *leave-one-out*. The 1-NN
        regressor looks for the training example :math:`\mathbf x_i` most similar to the new example in the input space
        and assigns to it the same output :math:`y_i`.

        .. math::

            S_3(\mathbf x_i) = (NN(\mathbf x_i)-y_i)^2

        where :math:`NN(\mathbf x_i)` represents the 1-nearest neighbor prediction for :math:`\mathbf x_i`. Larger
        values are observed for harder instances.

        Returns:
            array-like: Squared error of 1-nearest neighbor values per instance.
        """
        nn = NearestNeighbors(n_neighbors=1, metric='precomputed').fit(self.dist_matrix_gower)
        nn_arr = nn.kneighbors_graph(mode='distance').toarray()
        _, neighs = np.nonzero(nn_arr)
        S3 = (self.y_scaled[neighs] - self.y_scaled) ** 2

        return 1 - np.exp(-S3 / S3.std())

    def feature_outlier(self) -> np.ndarray:
        IQR = iqr(self.X_scaled, axis=0)
        Q1 = np.quantile(self.X_scaled, 0.25, axis=0)
        Q3 = np.quantile(self.X_scaled, 0.75, axis=0)
        lbound = Q1 - 1.5 * IQR
        ubound = Q3 + 1.5 * IQR

        FO = np.mean((self.X_scaled < lbound) | (self.X_scaled > ubound), axis=1)
        return FO

    def target_outlier(self) -> np.ndarray:
        IQR_t = iqr(self.y)
        Q1_t = np.quantile(self.y, 0.25)
        Q3_t = np.quantile(self.y, 0.75)
        lbound_t = Q1_t - 1.5 * IQR_t
        ubound_t = Q3_t + 1.5 * IQR_t

        POT = (self.y < lbound_t) | (self.y > ubound_t)
        POT = POT * 1
        return POT

    def histogram_bin(self) -> np.ndarray:
        r"""
        First a histogram of the normalized values of :math:`\mathbf y` is taken. Next, we output the complement of the
        percentage of instances that have their labels placed in the same bin as :math:`\mathbf x_i`. Easy instances
        will tend to share labels with many other instances in :math:`D` than hard instances.

        Returns:
            array-like: Histogram bin measure values per instance.
        """
        n_bin, bins = np.histogram(self.y_scaled, density=False, bins='auto')
        bin_idx = np.digitize(self.y_scaled, bins=bins, right=False)
        HB = 1 - n_bin[np.clip(bin_idx, a_max=len(n_bin), a_min=None) - 1] / n_bin.sum()
        return HB

    def stump_error(self) -> np.ndarray:
        stump = tree.DecisionTreeRegressor(max_depth=1, criterion='squared_error').fit(self.X, self.y)
        EDS = (self.y - stump.predict(self.X)) ** 2
        return 1 - np.exp(-EDS / EDS.std())

    def zero_rule_error(self) -> np.ndarray:
        zero_r = (self.y - np.median(self.y)) ** 2
        return 1 - np.exp(-zero_r / zero_r.std())

    def disjunct_size(self) -> np.ndarray:
        data = self.data.copy()

        data['leaf_id'] = self.dtr.apply(self.X)
        df_count = data.groupby('leaf_id').count().iloc[:, 0].to_frame('count').subtract(1)
        data = data.join(df_count, on='leaf_id')
        DS = data['count'].divide(data['count'].max())

        return 1 - DS.values

    def tree_depth_unpruned(self) -> np.ndarray:
        r"""
        Tree Depth (TD) returns the depth of the leaf node that predicts :math:`\mathbf x_i` in a  decision tree,
        normalized by the maximum depth of the tree built from :math:`D`:

        .. math::

            TD(\mathbf x_i) = \frac{depth(\mathbf x_i)}{\max(depth(D))}

        There are two versions of this measure, using pruned (:math:`TD_P(\mathbf x_i)`)
        and unpruned (:math:`TD_U(\mathbf x_i)`) decision trees. Instances harder to predict tend to be placed
        at deeper levels of the trees and present higher :math:`TD` values.

        Returns:
            array-like: :math:`TD_U(\mathbf x_i)`
        """
        return pd.DataFrame(self.X_scaled).apply(lambda x: self.dtr.decision_path([x]).sum() - 1,
                                                 axis=1, raw=True).values / self.dtr.get_depth()

    def tree_depth_pruned(self) -> np.ndarray:
        r"""
        Tree Depth (TD) returns the depth of the leaf node that predicts :math:`\mathbf x_i` in a  decision tree,
        normalized by the maximum depth of the tree built from :math:`D`:

        .. math::

            TD(\mathbf x_i) = \frac{depth(\mathbf x_i)}{\max(depth(D))}

        There are two versions of this measure, using pruned (:math:`TD_P(\mathbf x_i)`)
        and unpruned (:math:`TD_U(\mathbf x_i)`) decision trees. Instances harder to predict tend to be placed
        at deeper levels of the trees and present higher :math:`TD` values.

        Returns:
            array-like: :math:`TD_P(\mathbf x_i)`
        """
        return pd.DataFrame(self.X_scaled).apply(lambda x: self.dtr_pruned.decision_path([x]).sum() - 1,
                                                 axis=1, raw=True).values / self.dtr_pruned.get_depth()

    def density(self) -> np.ndarray:
        nodes_degrees = np.sum(self.adjacency_matrix, axis=1)
        return nodes_degrees / (self.N - 1)

    def clustering_coefficient(self) -> np.ndarray:
        degrees = np.sum(self.adjacency_matrix, axis=1)
        unormalized = np.divide(2 * np.sum(self.adjacency_matrix * (degrees - 1), axis=1),
                                degrees * (degrees - 1))
        return 1 - np.divide(unormalized, self.N)
