import pytest
import numpy as np
from sklearn.utils._param_validation import generate_invalid_param_val
from sklearn.utils._param_validation import (
    StrOptions, MissingValues, _VerboseHelper, HasMethods, 
    _IterablesNotString, _CVObjects, Interval, Integral, Real, RealNotInt
)

def test_generate_invalid_param_val_str_options():
    constraint = StrOptions(options=["option1", "option2"])
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == "not option1 or option2"

def test_generate_invalid_param_val_missing_values():
    constraint = MissingValues()
    invalid_value = generate_invalid_param_val(constraint)
    assert np.array_equal(invalid_value, np.array([1, 2, 3]))

def test_generate_invalid_param_val_verbose_helper():
    constraint = _VerboseHelper()
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == -1

def test_generate_invalid_param_val_has_methods():
    constraint = HasMethods(methods=["fit", "predict"])
    invalid_value = generate_invalid_param_val(constraint)
    assert not hasattr(invalid_value, "fit")
    assert not hasattr(invalid_value, "predict")

def test_generate_invalid_param_val_iterables_not_string():
    constraint = _IterablesNotString()
    invalid_value = generate_invalid_param_val(constraint)
    assert isinstance(invalid_value, str)

def test_generate_invalid_param_val_cv_objects():
    constraint = _CVObjects()
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == "not a cv object"

def test_generate_invalid_param_val_interval_integral():
    constraint = Interval(type=Integral, left=0, right=10)
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == -1

def test_generate_invalid_param_val_interval_real():
    constraint = Interval(type=Real, left=0.0, right=10.0)
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == -1e-6

def test_generate_invalid_param_val_interval_real_not_int():
    constraint = Interval(type=RealNotInt, left=0.0, right=10.0)
    invalid_value = generate_invalid_param_val(constraint)
    assert invalid_value == -1e-6

def test_generate_invalid_param_val_interval_inf_bounds():
    constraint = Interval(type=Real, left=None, right=None, closed="both")
    invalid_value = generate_invalid_param_val(constraint)
    assert np.isnan(invalid_value)

def test_generate_invalid_param_val_not_implemented_error():
    constraint = Interval(type=Integral, left=None, right=None)
    with pytest.raises(NotImplementedError):
        generate_invalid_param_val(constraint)