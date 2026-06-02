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


class TestGenerateInvalidParamVal:
    def test_str_options_single(self):
        constraint = StrOptions({"option1"})
        result = generate_invalid_param_val(constraint)
        assert result == "not option1"
        assert result not in constraint.options

    def test_str_options_multiple(self):
        constraint = StrOptions({"option1", "option2", "option3"})
        result = generate_invalid_param_val(constraint)
        assert "not" in result
        assert result not in constraint.options

    def test_missing_values(self):
        constraint = MissingValues()
        result = generate_invalid_param_val(constraint)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, np.array([1, 2, 3]))

    def test_verbose_helper(self):
        constraint = _VerboseHelper()
        result = generate_invalid_param_val(constraint)
        assert result == -1

    def test_has_methods(self):
        constraint = HasMethods(["fit", "predict"])
        result = generate_invalid_param_val(constraint)
        assert not hasattr(result, "fit")
        assert not hasattr(result, "predict")

    def test_iterables_not_string(self):
        constraint = _IterablesNotString()
        result = generate_invalid_param_val(constraint)
        assert result == "a string"
        assert isinstance(result, str)

    def test_cv_objects(self):
        constraint = _CVObjects()
        result = generate_invalid_param_val(constraint)
        assert result == "not a cv object"

    def test_interval_integral_with_left_bound(self):
        constraint = Interval(Integral, 5, None, closed="left")
        result = generate_invalid_param_val(constraint)
        assert result == 4
        assert result < constraint.left

    def test_interval_integral_with_right_bound(self):
        constraint = Interval(Integral, None, 10, closed="right")
        result = generate_invalid_param_val(constraint)
        assert result == 11
        assert result > constraint.right

    def test_interval_integral_with_both_bounds(self):
        constraint = Interval(Integral, 0, 100, closed="both")
        result = generate_invalid_param_val(constraint)
        assert result == -1
        assert result < constraint.left

    def test_interval_real_with_left_bound(self):
        constraint = Interval(Real, 0.5, None, closed="left")
        result = generate_invalid_param_val(constraint)
        assert result == 0.5 - 1e-6
        assert result < constraint.left

    def test_interval_real_with_right_bound(self):
        constraint = Interval(Real, None, 1.0, closed="right")
        result = generate_invalid_param_val(constraint)
        assert result == 1.0 + 1e-6
        assert result > constraint.right

    def test_interval_real_with_both_bounds(self):
        constraint = Interval(Real, -1.0, 1.0, closed="both")
        result = generate_invalid_param_val(constraint)
        assert result == -1.0 - 1e-6
        assert result < constraint.left

    def test_interval_real_infinite_closed_right(self):
        constraint = Interval(Real, None, None, closed="right")
        result = generate_invalid_param_val(constraint)
        assert result == -np.inf

    def test_interval_real_infinite_closed_left(self):
        constraint = Interval(Real, None, None, closed="left")
        result = generate_invalid_param_val(constraint)
        assert result == np.inf

    def test_interval_real_infinite_closed_neither(self):
        constraint = Interval(Real, None, None, closed="neither")
        result = generate_invalid_param_val(constraint)
        assert result == -np.inf

    def test_interval_real_infinite_closed_both(self):
        constraint = Interval(Real, None, None, closed="both")
        result = generate_invalid_param_val(constraint)
        assert np.isnan(result)

    def test_interval_integral_infinite_raises(self):
        constraint = Interval(Integral, None, None, closed="both")
        with pytest.raises(NotImplementedError):
            generate_invalid_param_val(constraint)

    def test_unsupported_constraint_raises(self):
        class UnsupportedConstraint:
            pass
        
        constraint = UnsupportedConstraint()
        with pytest.raises(NotImplementedError):
            generate_invalid_param_val(constraint)