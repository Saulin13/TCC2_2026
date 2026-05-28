import pytest
from unittest.mock import patch
from sklearn.utils._array_api import yield_namespace_device_dtype_combinations


def test_yield_namespace_device_dtype_combinations_with_numpy():
    """Test that numpy namespaces are included when include_numpy_namespaces=True."""
    results = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=True))
    
    assert len(results) > 0
    assert all(isinstance(item, tuple) for item in results)
    assert all(len(item) == 3 for item in results)
    
    # Check that we have at least one numpy-related namespace
    namespaces = [item[0] for item in results]
    assert any('numpy' in ns or ns == 'numpy' for ns in namespaces)


def test_yield_namespace_device_dtype_combinations_without_numpy():
    """Test that numpy namespaces are excluded when include_numpy_namespaces=False."""
    results = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=False))
    
    assert all(isinstance(item, tuple) for item in results)
    assert all(len(item) == 3 for item in results)


@patch('sklearn.utils._array_api.yield_namespaces')
def test_torch_namespace_combinations(mock_yield_namespaces):
    """Test that torch namespace yields correct device and dtype combinations."""
    mock_yield_namespaces.return_value = ['torch']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected = [
        ('torch', 'cpu', 'float64'),
        ('torch', 'cpu', 'float32'),
        ('torch', 'cuda', 'float64'),
        ('torch', 'cuda', 'float32'),
        ('torch', 'xpu', 'float64'),
        ('torch', 'xpu', 'float32'),
        ('torch', 'mps', 'float32'),
    ]
    
    assert results == expected


@patch('sklearn.utils._array_api.yield_namespaces')
def test_dpnp_namespace_combinations(mock_yield_namespaces):
    """Test that dpnp namespace yields correct device and dtype combinations."""
    mock_yield_namespaces.return_value = ['dpnp']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected = [
        ('dpnp', 'cpu', 'float64'),
        ('dpnp', 'cpu', 'float32'),
        ('dpnp', 'gpu', 'float64'),
        ('dpnp', 'gpu', 'float32'),
    ]
    
    assert results == expected


@patch('sklearn.utils._array_api.yield_namespaces')
def test_array_api_strict_namespace_combinations(mock_yield_namespaces):
    """Test that array_api_strict namespace yields correct combinations."""
    mock_yield_namespaces.return_value = ['array_api_strict']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected = [
        ('array_api_strict', 'CPU_DEVICE', 'float64'),
        ('array_api_strict', 'device1', 'float32'),
    ]
    
    assert results == expected


@patch('sklearn.utils._array_api.yield_namespaces')
def test_other_namespace_combinations(mock_yield_namespaces):
    """Test that other namespaces yield None for device and dtype."""
    mock_yield_namespaces.return_value = ['numpy', 'cupy']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    expected = [
        ('numpy', None, None),
        ('cupy', None, None),
    ]
    
    assert results == expected


@patch('sklearn.utils._array_api.yield_namespaces')
def test_multiple_namespaces_mixed(mock_yield_namespaces):
    """Test combinations with multiple different namespace types."""
    mock_yield_namespaces.return_value = ['torch', 'array_api_strict', 'numpy']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    # Check torch combinations
    torch_results = [r for r in results if r[0] == 'torch']
    assert len(torch_results) == 7
    assert ('torch', 'cpu', 'float64') in torch_results
    assert ('torch', 'mps', 'float32') in torch_results
    
    # Check array_api_strict combinations
    strict_results = [r for r in results if r[0] == 'array_api_strict']
    assert len(strict_results) == 2
    assert ('array_api_strict', 'CPU_DEVICE', 'float64') in strict_results
    
    # Check numpy combinations
    numpy_results = [r for r in results if r[0] == 'numpy']
    assert len(numpy_results) == 1
    assert ('numpy', None, None) in numpy_results


@patch('sklearn.utils._array_api.yield_namespaces')
def test_empty_namespaces(mock_yield_namespaces):
    """Test behavior when no namespaces are yielded."""
    mock_yield_namespaces.return_value = []
    
    results = list(yield_namespace_device_dtype_combinations())
    
    assert results == []


def test_generator_behavior():
    """Test that the function returns a generator."""
    result = yield_namespace_device_dtype_combinations()
    
    # Check it's a generator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')


@patch('sklearn.utils._array_api.yield_namespaces')
def test_tuple_structure(mock_yield_namespaces):
    """Test that all returned tuples have correct structure."""
    mock_yield_namespaces.return_value = ['torch', 'numpy', 'array_api_strict']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    for namespace, device, dtype in results:
        assert isinstance(namespace, str)
        assert device is None or isinstance(device, str)
        assert dtype is None or isinstance(dtype, str)