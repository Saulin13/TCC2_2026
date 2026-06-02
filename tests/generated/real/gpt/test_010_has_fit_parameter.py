import pytest
from sklearn.utils.validation import has_fit_parameter
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

def test_has_fit_parameter_true():
    estimator = SVC()
    assert has_fit_parameter(estimator, "sample_weight") is True

def test_has_fit_parameter_false():
    estimator = SVC()
    assert has_fit_parameter(estimator, "non_existent_param") is False

def test_has_fit_parameter_no_fit_method():
    class NoFitEstimator:
        pass

    estimator = NoFitEstimator()
    assert has_fit_parameter(estimator, "any_param") is False

def test_has_fit_parameter_linear_regression():
    estimator = LinearRegression()
    assert has_fit_parameter(estimator, "sample_weight") is True

def test_has_fit_parameter_kmeans():
    estimator = KMeans()
    assert has_fit_parameter(estimator, "sample_weight") is False

def test_has_fit_parameter_edge_case_empty_string():
    estimator = SVC()
    assert has_fit_parameter(estimator, "") is False

def test_has_fit_parameter_edge_case_none():
    estimator = SVC()
    with pytest.raises(TypeError):
        has_fit_parameter(estimator, None)