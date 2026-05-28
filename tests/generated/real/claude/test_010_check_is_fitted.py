import pytest
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class DummyEstimator:
    """A simple estimator for testing."""
    def fit(self, X, y=None):
        self.fitted_ = True
        return self


class DummyEstimatorMultipleAttrs:
    """Estimator with multiple fitted attributes."""
    def fit(self, X, y=None):
        self.coef_ = [1, 2, 3]
        self.intercept_ = 0.5
        self.n_iter_ = 10
        return self


class DummyEstimatorNoFit:
    """Not an estimator - no fit method."""
    pass


class DummyEstimatorWithSklearnIsFitted:
    """Estimator using __sklearn_is_fitted__ method."""
    def __init__(self):
        self._is_fitted = False
    
    def fit(self, X, y=None):
        self._is_fitted = True
        return self
    
    def __sklearn_is_fitted__(self):
        return self._is_fitted


def test_check_is_fitted_with_fitted_estimator():
    """Test that check passes for a fitted estimator."""
    est = DummyEstimator()
    est.fit([[1, 2], [3, 4]])
    check_is_fitted(est)


def test_check_is_fitted_with_unfitted_estimator():
    """Test that NotFittedError is raised for unfitted estimator."""
    est = DummyEstimator()
    with pytest.raises(NotFittedError, match="This DummyEstimator instance is not fitted yet"):
        check_is_fitted(est)


def test_check_is_fitted_with_specific_attribute():
    """Test checking for a specific attribute."""
    est = DummyEstimatorMultipleAttrs()
    est.fit([[1, 2], [3, 4]])
    check_is_fitted(est, attributes="coef_")


def test_check_is_fitted_with_multiple_attributes_all():
    """Test checking for multiple attributes with all_or_any=all."""
    est = DummyEstimatorMultipleAttrs()
    est.fit([[1, 2], [3, 4]])
    check_is_fitted(est, attributes=["coef_", "intercept_", "n_iter_"], all_or_any=all)


def test_check_is_fitted_with_multiple_attributes_any():
    """Test checking for multiple attributes with all_or_any=any."""
    est = DummyEstimatorMultipleAttrs()
    est.fit([[1, 2], [3, 4]])
    est.coef_ = [1, 2, 3]
    check_is_fitted(est, attributes=["coef_", "missing_attr_"], all_or_any=any)


def test_check_is_fitted_missing_specific_attribute():
    """Test that NotFittedError is raised when specific attribute is missing."""
    est = DummyEstimator()
    est.fit([[1, 2], [3, 4]])
    with pytest.raises(NotFittedError):
        check_is_fitted(est, attributes="missing_attr_")


def test_check_is_fitted_missing_all_attributes():
    """Test that NotFittedError is raised when all attributes are missing."""
    est = DummyEstimatorMultipleAttrs()
    est.fit([[1, 2], [3, 4]])
    delattr(est, "coef_")
    with pytest.raises(NotFittedError):
        check_is_fitted(est, attributes=["coef_", "missing_"], all_or_any=all)


def test_check_is_fitted_custom_message():
    """Test custom error message."""
    est = DummyEstimator()
    custom_msg = "Estimator %(name)s must be fitted first"
    with pytest.raises(NotFittedError, match="Estimator DummyEstimator must be fitted first"):
        check_is_fitted(est, msg=custom_msg)


def test_check_is_fitted_with_class_raises_typeerror():
    """Test that TypeError is raised when passing a class instead of instance."""
    with pytest.raises(TypeError, match="is a class, not an instance"):
        check_is_fitted(DummyEstimator)


def test_check_is_fitted_with_non_estimator_raises_typeerror():
    """Test that TypeError is raised for non-estimator objects."""
    obj = DummyEstimatorNoFit()
    with pytest.raises(TypeError, match="is not an estimator instance"):
        check_is_fitted(obj)


def test_check_is_fitted_with_sklearn_estimator():
    """Test with real sklearn estimator."""
    lr = LogisticRegression()
    with pytest.raises(NotFittedError):
        check_is_fitted(lr)
    
    lr.fit([[1, 2], [3, 4]], [0, 1])
    check_is_fitted(lr)


def test_check_is_fitted_with_sklearn_estimator_specific_attrs():
    """Test with real sklearn estimator checking specific attributes."""
    lr = LogisticRegression()
    lr.fit([[1, 2], [3, 4]], [0, 1])
    check_is_fitted(lr, attributes=["coef_", "intercept_"])


def test_check_is_fitted_with_tuple_attributes():
    """Test with attributes passed as tuple."""
    est = DummyEstimatorMultipleAttrs()
    est.fit([[1, 2], [3, 4]])
    check_is_fitted(est, attributes=("coef_", "intercept_"))


def test_check_is_fitted_with_sklearn_is_fitted_method():
    """Test with estimator using __sklearn_is_fitted__ method."""
    est = DummyEstimatorWithSklearnIsFitted()
    with pytest.raises(NotFittedError):
        check_is_fitted(est)
    
    est.fit([[1, 2], [3, 4]])
    check_is_fitted(est)


def test_check_is_fitted_with_transformer():
    """Test with sklearn transformer."""
    scaler = StandardScaler()
    with pytest.raises(NotFittedError):
        check_is_fitted(scaler)
    
    scaler.fit([[1, 2], [3, 4]])
    check_is_fitted(scaler)
    check_is_fitted(scaler, attributes="mean_")


def test_check_is_fitted_any_with_one_present():
    """Test all_or_any=any when only one attribute is present."""
    est = DummyEstimator()
    est.fitted_ = True
    check_is_fitted(est, attributes=["fitted_", "nonexistent_"], all_or_any=any)


def test_check_is_fitted_any_with_none_present():
    """Test all_or_any=any when no attributes are present."""
    est = DummyEstimator()
    with pytest.raises(NotFittedError):
        check_is_fitted(est, attributes=["missing1_", "missing2_"], all_or_any=any)