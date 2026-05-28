import pytest
from unittest.mock import patch
from sklearn.utils._array_api import yield_namespace_device_dtype_combinations


def test_yield_namespace_device_dtype_combinations_with_numpy():
    """Test that numpy namespaces are included when include_numpy_namespaces=True."""
    results = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=True))
    
    assert len(results) > 0
    assert all(len(item) == 3 for item in results)
    
    # Check that at least one numpy-related namespace is present
    namespaces = [item[0] for item in results]
    assert any('numpy' in ns for ns in namespaces)


def test_yield_namespace_device_dtype_combinations_without_numpy():
    """Test that numpy namespaces are excluded when include_numpy_namespaces=False."""
    results = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=False))
    
    assert all(len(item) == 3 for item in results)
    
    # Check that numpy is not in the namespaces
    namespaces = [item[0] for item in results]
    assert not any(ns == 'numpy' for ns in namespaces)


@patch('sklearn.utils._array_api.yield_namespaces')
def test_torch_namespace_combinations(mock_yield_namespaces):
    """Test that torch namespace yields correct device and dtype combinations."""
    mock_yield_namespaces.return_value = ['torch']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected_combinations = [
        ('torch', 'cpu', 'float64'),
        ('torch', 'cpu', 'float32'),
        ('torch', 'cuda', 'float64'),
        ('torch', 'cuda', 'float32'),
        ('torch', 'xpu', 'float64'),
        ('torch', 'xpu', 'float32'),
        ('torch', 'mps', 'float32'),
    ]
    
    assert results == expected_combinations


@patch('sklearn.utils._array_api.yield_namespaces')
def test_dpnp_namespace_combinations(mock_yield_namespaces):
    """Test that dpnp namespace yields correct device and dtype combinations."""
    mock_yield_namespaces.return_value = ['dpnp']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected_combinations = [
        ('dpnp', 'cpu', 'float64'),
        ('dpnp', 'cpu', 'float32'),
        ('dpnp', 'gpu', 'float64'),
        ('dpnp', 'gpu', 'float32'),
    ]
    
    assert results == expected_combinations


@patch('sklearn.utils._array_api.yield_namespaces')
def test_array_api_strict_namespace_combinations(mock_yield_namespaces):
    """Test that array_api_strict namespace yields correct combinations."""
    mock_yield_namespaces.return_value = ['array_api_strict']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected_combinations = [
        ('array_api_strict', 'CPU_DEVICE', 'float64'),
        ('array_api_strict', 'device1', 'float32'),
    ]
    
    assert results == expected_combinations


@patch('sklearn.utils._array_api.yield_namespaces')
def test_other_namespace_combinations(mock_yield_namespaces):
    """Test that other namespaces yield None for device and dtype."""
    mock_yield_namespaces.return_value = ['cupy', 'jax.numpy']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected_combinations = [
        ('cupy', None, None),
        ('jax.numpy', None, None),
    ]
    
    assert results == expected_combinations


@patch('sklearn.utils._array_api.yield_namespaces')
def test_mixed_namespaces(mock_yield_namespaces):
    """Test with a mix of different namespace types."""
    mock_yield_namespaces.return_value = ['torch', 'array_api_strict', 'cupy']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    # Check torch combinations are present
    torch_results = [r for r in results if r[0] == 'torch']
    assert len(torch_results) == 7
    
    # Check array_api_strict combinations are present
    strict_results = [r for r in results if r[0] == 'array_api_strict']
    assert len(strict_results) == 2
    
    # Check cupy combinations are present
    cupy_results = [r for r in results if r[0] == 'cupy']
    assert cupy_results == [('cupy', None, None)]


@patch('sklearn.utils._array_api.yield_namespaces')
def test_empty_namespaces(mock_yield_namespaces):
    """Test with no namespaces available."""
    mock_yield_namespaces.return_value = []
    
    results = list(yield_namespace_device_dtype_combinations())
    
    assert results == []


def test_return_type_is_generator():
    """Test that the function returns a generator."""
    result = yield_namespace_device_dtype_combinations()
    
    # Check it's a generator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')


@patch('sklearn.utils._array_api.yield_namespaces')
def test_tuple_structure(mock_yield_namespaces):
    """Test that all returned items are 3-tuples with correct types."""
    mock_yield_namespaces.return_value = ['torch', 'cupy', 'array_api_strict']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    for namespace, device, dtype in results:
        assert isinstance(namespace, str)
        assert device is None or isinstance(device, str)
        assert dtype is None or isinstance(dtype, str)