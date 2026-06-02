import pytest
import numpy as np
from sklearn.utils._param_validation import generate_invalid_param_val
from sklearn.utils._param_validation import (
    StrOptions, MissingValues, _VerboseHelper, HasMethods,
    _IterablesNotString, _CVObjects, Interval, Integral, Real, RealNotInt
)

def test_generate_invalid_param_val_str_options():
    constraint = StrOptions(options=["option1", "option2"])
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val == "not option1 or option2"

def test_generate_invalid_param_val_missing_values():
    constraint = MissingValues()
    invalid_val = generate_invalid_param_val(constraint)
    assert np.array_equal(invalid_val, np.array([1, 2, 3]))

def test_generate_invalid_param_val_verbose_helper():
    constraint = _VerboseHelper()
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val == -1

def test_generate_invalid_param_val_has_methods():
    constraint = HasMethods(methods=["fit", "transform"])
    invalid_val = generate_invalid_param_val(constraint)
    assert not hasattr(invalid_val, "fit")
    assert not hasattr(invalid_val, "transform")

def test_generate_invalid_param_val_iterables_not_string():
    constraint = _IterablesNotString()
    invalid_val = generate_invalid_param_val(constraint)
    assert isinstance(invalid_val, str)

def test_generate_invalid_param_val_cv_objects():
    constraint = _CVObjects()
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val == "not a cv object"

def test_generate_invalid_param_val_interval_integral():
    constraint = Interval(type=Integral, left=0, right=10)
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val == -1

def test_generate_invalid_param_val_interval_real():
    constraint = Interval(type=Real, left=0.0, right=10.0)
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val < 0.0

def test_generate_invalid_param_val_interval_real_not_int():
    constraint = Interval(type=RealNotInt, left=0.0, right=10.0)
    invalid_val = generate_invalid_param_val(constraint)
    assert invalid_val < 0.0

def test_generate_invalid_param_val_interval_no_bounds():
    constraint = Interval(type=Integral)
    with pytest.raises(NotImplementedError):
        generate_invalid_param_val(constraint)

def test_generate_invalid_param_val_interval_real_inf():
    constraint = Interval(type=Real, left=None, right=None, closed="both")
    invalid_val = generate_invalid_param_val(constraint)
    assert np.isnan(invalid_val)

def test_generate_invalid_param_val_not_implemented_error():
    class UnknownConstraint:
        pass

    constraint = UnknownConstraint()
    with pytest.raises(NotImplementedError):
        generate_invalid_param_val(constraint)