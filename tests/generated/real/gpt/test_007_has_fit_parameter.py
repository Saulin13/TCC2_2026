import pytest
from sklearn.utils.validation import has_fit_parameter
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

def test_has_fit_parameter_true():
    estimator = SVC()
    assert has_fit_parameter(estimator, "sample_weight") == True

def test_has_fit_parameter_false():
    estimator = LinearRegression()
    assert has_fit_parameter(estimator, "sample_weight") == False

def test_has_fit_parameter_no_fit_method():
    class NoFitEstimator:
        pass

    estimator = NoFitEstimator()
    assert has_fit_parameter(estimator, "sample_weight") == False

def test_has_fit_parameter_empty_string():
    estimator = KMeans()
    assert has_fit_parameter(estimator, "") == False

def test_has_fit_parameter_non_existent_parameter():
    estimator = SVC()
    assert has_fit_parameter(estimator, "non_existent_param") == False

def test_has_fit_parameter_edge_case():
    class CustomEstimator:
        def fit(self, x, y, custom_param=None):
            pass

    estimator = CustomEstimator()
    assert has_fit_parameter(estimator, "custom_param") == True

def test_has_fit_parameter_invalid_estimator():
    with pytest.raises(AttributeError):
        has_fit_parameter(None, "sample_weight")