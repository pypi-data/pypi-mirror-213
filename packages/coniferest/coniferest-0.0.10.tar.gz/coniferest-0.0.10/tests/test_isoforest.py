import pytest

import numpy as np
from numpy.testing import assert_allclose, assert_equal

from coniferest.sklearn.isoforest import IsolationForestEvaluator
from coniferest.isoforest import IsolationForest
from sklearn.ensemble import IsolationForest as SkIsolationForest

from coniferest.datasets import MalanchevDataset


@pytest.fixture()
def isoforest_results():
    return IsoforestResults()


class IsoforestResults:
    def __init__(self):
        seed = 622341
        self.dataset = MalanchevDataset(inliers=1000,
                                        outliers=50,
                                        regions=[1, 1, -1],
                                        rng=seed)

        data = self.dataset.data
        trees = 1000

        forest = IsolationForest(n_trees=trees, random_seed=seed + 1)
        self.scores = self.calc_forest_scores(forest, data)
        self.forest = forest

        forest = SkIsolationForest(n_estimators=trees, random_state=seed + 2)
        self.skores0 = self.calc_forest_scores(forest, data)

        forest = SkIsolationForest(n_estimators=trees, random_state=seed + 3)
        self.skores1 = self.calc_forest_scores(forest, data)
        self.skores1_by_evaluator = IsolationForestEvaluator(forest).score_samples(data)

    @staticmethod
    def calc_forest_scores(forest, data):
        forest.fit(data)
        return forest.score_samples(data)


def test_sklearn_isolation_forest_evaluator(isoforest_results):
    """
    Does evaluator scores coinside with the ones computed by sklearn?
    """
    r = isoforest_results
    assert_allclose(r.skores1_by_evaluator, r.skores1, atol=1e-10, rtol=0,
                    err_msg='sklearn and our results nust be the same')


def test_isolation_forest(isoforest_results):
    """
    Does assigned scores by our isoforest are somewhere near assigned by sklearn's isoforest?
    """
    r = isoforest_results
    diff_sk_to_sk = np.max(np.abs(r.skores0 - r.skores1))
    diff_coni_to_sk = np.max(np.abs(r.skores0 - r.scores))
    assert diff_coni_to_sk < 1.5 * diff_sk_to_sk


def test_serialization(isoforest_results):
    """
    Does (de)serialization work correctly?
    """
    import pickle

    r = isoforest_results
    s = pickle.dumps(r.forest)
    reforest = pickle.loads(s)
    assert_allclose(reforest.score_samples(r.dataset.data), r.scores, atol=1e-12)


def forest_n_features(forest: IsolationForest):
    return forest.evaluator.selectors[0, 0].n_features


def assert_forest_scores(forest1: IsolationForest, forest2: IsolationForest, data=None, n_features=None):
    if data is None:
        if n_features is None:
            raise ValueError('Either data or n_features')
        data = np.random.standard_normal((1024, n_features))
    assert_equal(forest1.score_samples(data), forest2.score_samples(data))


def build_forest(n_features: int, random_seed: int) -> IsolationForest:
    n_trees = 100
    n_subsamples = 256

    rng = np.random.default_rng(random_seed)
    data = rng.standard_normal((n_trees * n_subsamples, n_features))

    forest = IsolationForest(n_trees=n_trees, n_subsamples=n_subsamples, max_depth=None, random_seed=random_seed)
    forest.fit(data)
    return forest


def test_reproducibility():
    n_features = 16
    random_seed = np.random.randint(1 << 16)
    forest1 = build_forest(n_features, random_seed)
    forest2 = build_forest(n_features, random_seed)
    assert_forest_scores(forest1, forest2, n_features=n_features)


@pytest.mark.regression
def test_regression(regression_data):
    random_seed = 0
    n_features = 16
    n_samples = 128
    rng = np.random.default_rng(random_seed)
    data = rng.standard_normal((n_samples, n_features))
    forest = build_forest(n_features=n_features, random_seed=random_seed)
    scores = forest.score_samples(data)
    regression_data.allclose(scores)
