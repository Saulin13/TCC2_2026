import pytest
import numpy as np
from sklearn.metrics._scorer import check_scoring
from sklearn.metrics import accuracy_score, make_scorer, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification, make_regression


class DummyEstimatorWithScore:
    def fit(self, X, y):
        return self
    
    def score(self, X, y):
        return 0.95


class DummyEstimatorWithoutScore:
    def fit(self, X, y):
        return self


def dummy_scorer(estimator, X, y):
    return 0.85


def test_check_scoring_with_string_scorer():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring='accuracy')
    score = scorer(clf, X, y)
    
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_check_scoring_with_callable_scorer():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring=dummy_scorer)
    score = scorer(clf, X, y)
    
    assert score == 0.85


def test_check_scoring_with_make_scorer():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    custom_scorer = make_scorer(accuracy_score)
    scorer = check_scoring(clf, scoring=custom_scorer)
    score = scorer(clf, X, y)
    
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_check_scoring_with_none_and_estimator_with_score():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring=None)
    score = scorer(clf, X, y)
    
    assert isinstance(score, float)


def test_check_scoring_with_none_and_dummy_estimator_with_score():
    estimator = DummyEstimatorWithScore()
    
    scorer = check_scoring(estimator, scoring=None)
    score = scorer(estimator, None, None)
    
    assert score == 0.95


def test_check_scoring_with_none_allow_none_true():
    estimator = DummyEstimatorWithoutScore()
    
    result = check_scoring(estimator, scoring=None, allow_none=True)
    
    assert result is None


def test_check_scoring_with_list_of_scorers():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring=['accuracy', 'precision'])
    scores = scorer(clf, X, y)
    
    assert isinstance(scores, dict)
    assert 'accuracy' in scores
    assert 'precision' in scores
    assert isinstance(scores['accuracy'], float)
    assert isinstance(scores['precision'], float)


def test_check_scoring_with_tuple_of_scorers():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring=('accuracy', 'recall'))
    scores = scorer(clf, X, y)
    
    assert isinstance(scores, dict)
    assert 'accuracy' in scores
    assert 'recall' in scores


def test_check_scoring_with_set_of_scorers():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring={'accuracy', 'f1'})
    scores = scorer(clf, X, y)
    
    assert isinstance(scores, dict)
    assert 'accuracy' in scores
    assert 'f1' in scores


def test_check_scoring_with_dict_of_scorers():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scoring_dict = {
        'acc': make_scorer(accuracy_score),
        'custom': dummy_scorer
    }
    scorer = check_scoring(clf, scoring=scoring_dict)
    scores = scorer(clf, X, y)
    
    assert isinstance(scores, dict)
    assert 'acc' in scores
    assert 'custom' in scores
    assert scores['custom'] == 0.85


def test_check_scoring_with_none_estimator_and_string_scorer():
    scorer = check_scoring(estimator=None, scoring='accuracy')
    
    assert callable(scorer)


def test_check_scoring_raises_typeerror_without_score_method():
    estimator = DummyEstimatorWithoutScore()
    
    with pytest.raises(TypeError, match="If no scoring is specified"):
        check_scoring(estimator, scoring=None, allow_none=False)


def test_check_scoring_raises_valueerror_for_metric_function():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    with pytest.raises(ValueError, match="looks like it is a metric function"):
        check_scoring(clf, scoring=accuracy_score)


def test_check_scoring_multimetric_with_raise_exc_false():
    X, y = make_regression(n_samples=100, n_features=20, random_state=42)
    y = np.abs(y)
    reg = LinearRegression().fit(X, y)
    
    scoring_dict = {
        'mse': make_scorer(mean_squared_error),
        'custom': dummy_scorer
    }
    scorer = check_scoring(reg, scoring=scoring_dict, raise_exc=False)
    scores = scorer(reg, X, y)
    
    assert isinstance(scores, dict)
    assert 'mse' in scores
    assert 'custom' in scores


def test_check_scoring_with_regression_scorer():
    X, y = make_regression(n_samples=100, n_features=20, random_state=42)
    reg = LinearRegression().fit(X, y)
    
    scorer = check_scoring(reg, scoring='r2')
    score = scorer(reg, X, y)
    
    assert isinstance(score, float)


def test_check_scoring_edge_case_empty_dict():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = LogisticRegression(random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring={})
    scores = scorer(clf, X, y)
    
    assert isinstance(scores, dict)
    assert len(scores) == 0


def test_check_scoring_with_decision_tree():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    clf = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X, y)
    
    scorer = check_scoring(clf, scoring='accuracy')
    score = scorer(clf, X, y)
    
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0