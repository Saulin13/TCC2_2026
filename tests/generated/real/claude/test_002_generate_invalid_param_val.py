import pytest
import numpy as np
from sklearn.utils._param_validation import (
    generate_invalid_param_val,
    StrOptions,
    MissingValues,
    _VerboseHelper,
    HasMethods,
    _IterablesNotString,
    _CVObjects,
    Interval,
)
from numbers import Integral, Real


class RealNotInt(Real):
    """Mock RealNotInt class for testing."""
    pass


def test_generate_invalid_param_val_str_options():
    constraint = StrOptions({"option1", "option2", "option3"})
    result = generate_invalid_param_val(constraint)
    assert isinstance(result, str)
    assert "not" in result
    assert "option1" in result or "option2" in result or "option3" in result


def test_generate_invalid_param_val_missing_values():
    constraint = MissingValues()
    result = generate_invalid_param_val(constraint)
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, np.array([1, 2, 3]))


def test_generate_invalid_param_val_verbose_helper():
    constraint = _VerboseHelper()
    result = generate_invalid_param_val(constraint)
    assert result == -1


def test_generate_invalid_param_val_has_methods():
    constraint = HasMethods(["method1", "method2"])
    result = generate_invalid_param_val(constraint)
    assert not hasattr(result, "method1")
    assert not hasattr(result, "method2")


def test_generate_invalid_param_val_iterables_not_string():
    constraint = _IterablesNotString()
    result = generate_invalid_param_val(constraint)
    assert result == "a string"
    assert isinstance(result, str)


def test_generate_invalid_param_val_cv_objects():
    constraint = _CVObjects()
    result = generate_invalid_param_val(constraint)
    assert result == "not a cv object"


def test_generate_invalid_param_val_interval_integral_left_bound():
    constraint = Interval(Integral, 5, None, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result == 4


def test_generate_invalid_param_val_interval_integral_right_bound():
    constraint = Interval(Integral, None, 10, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result == 11


def test_generate_invalid_param_val_interval_integral_both_bounds():
    constraint = Interval(Integral, 5, 10, closed="both")
    result = generate_invalid_param_val(constraint)
    assert result == 4


def test_generate_invalid_param_val_interval_real_left_bound():
    constraint = Interval(Real, 5.0, None, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result < 5.0
    assert abs(result - (5.0 - 1e-6)) < 1e-10


def test_generate_invalid_param_val_interval_real_right_bound():
    constraint = Interval(Real, None, 10.0, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result > 10.0
    assert abs(result - (10.0 + 1e-6)) < 1e-10


def test_generate_invalid_param_val_interval_real_both_bounds():
    constraint = Interval(Real, 5.0, 10.0, closed="both")
    result = generate_invalid_param_val(constraint)
    assert result < 5.0


def test_generate_invalid_param_val_interval_real_inf_closed_right():
    constraint = Interval(Real, -np.inf, np.inf, closed="right")
    result = generate_invalid_param_val(constraint)
    assert result == -np.inf


def test_generate_invalid_param_val_interval_real_inf_closed_left():
    constraint = Interval(Real, -np.inf, np.inf, closed="left")
    result = generate_invalid_param_val(constraint)
    assert result == np.inf


def test_generate_invalid_param_val_interval_real_inf_closed_neither():
    constraint = Interval(Real, -np.inf, np.inf, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result == -np.inf


def test_generate_invalid_param_val_interval_real_inf_closed_both():
    constraint = Interval(Real, -np.inf, np.inf, closed="both")
    result = generate_invalid_param_val(constraint)
    assert np.isnan(result)


def test_generate_invalid_param_val_interval_real_not_int():
    constraint = Interval(RealNotInt, 5.0, None, closed="neither")
    result = generate_invalid_param_val(constraint)
    assert result < 5.0


def test_generate_invalid_param_val_interval_integral_no_bounds_raises():
    constraint = Interval(Integral, -np.inf, np.inf, closed="both")
    with pytest.raises(NotImplementedError):
        generate_invalid_param_val(constraint)


def test_generate_invalid_param_val_unknown_constraint_raises():
    class UnknownConstraint:
        pass
    
    constraint = UnknownConstraint()
    with pytest.raises(NotImplementedError):
        generate_invalid_param_val(constraint)