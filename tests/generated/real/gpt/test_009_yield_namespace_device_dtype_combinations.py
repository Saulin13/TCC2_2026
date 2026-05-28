import pytest
from sklearn.utils._array_api import yield_namespace_device_dtype_combinations

def test_yield_namespace_device_dtype_combinations_default():
    combinations = list(yield_namespace_device_dtype_combinations())
    assert len(combinations) > 0  # Ensure that combinations are generated
    for namespace, device, dtype in combinations:
        assert isinstance(namespace, str)
        assert device is None or isinstance(device, str)
        assert dtype is None or isinstance(dtype, str)

def test_yield_namespace_device_dtype_combinations_no_numpy():
    combinations = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=False))
    assert len(combinations) > 0  # Ensure that combinations are generated
    for namespace, device, dtype in combinations:
        assert isinstance(namespace, str)
        assert device is None or isinstance(device, str)
        assert dtype is None or isinstance(dtype, str)
    assert all(namespace != "numpy" for namespace, _, _ in combinations)

def test_yield_namespace_device_dtype_combinations_torch():
    combinations = list(yield_namespace_device_dtype_combinations())
    torch_combinations = [c for c in combinations if c[0] == "torch"]
    expected_devices = {"cpu", "cuda", "xpu", "mps"}
    expected_dtypes = {"float64", "float32"}
    for _, device, dtype in torch_combinations:
        assert device in expected_devices
        assert dtype in expected_dtypes

def test_yield_namespace_device_dtype_combinations_array_api_strict():
    combinations = list(yield_namespace_device_dtype_combinations())
    strict_combinations = [c for c in combinations if c[0] == "array_api_strict"]
    expected_combinations = [
        ("array_api_strict", "CPU_DEVICE", "float64"),
        ("array_api_strict", "device1", "float32"),
    ]
    assert all(c in strict_combinations for c in expected_combinations)

def test_yield_namespace_device_dtype_combinations_invalid_namespace():
    with pytest.raises(ValueError):
        # Assuming yield_namespaces raises ValueError for invalid namespaces
        list(yield_namespace_device_dtype_combinations(include_numpy_namespaces="invalid"))