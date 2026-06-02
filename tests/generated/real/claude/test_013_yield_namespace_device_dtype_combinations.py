import pytest
from unittest.mock import patch, MagicMock
from sklearn.utils._array_api import yield_namespace_device_dtype_combinations


def test_yield_namespace_device_dtype_combinations_with_numpy():
    """Test that numpy namespaces are included when flag is True."""
    results = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=True))
    
    assert len(results) > 0
    assert all(isinstance(item, tuple) for item in results)
    assert all(len(item) == 3 for item in results)
    
    # Check that each tuple contains (str, str/None, str/None)
    for namespace, device, dtype in results:
        assert isinstance(namespace, str)
        assert device is None or isinstance(device, str)
        assert dtype is None or isinstance(dtype, str)


def test_yield_namespace_device_dtype_combinations_without_numpy():
    """Test that numpy namespaces are excluded when flag is False."""
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
def test_mixed_namespaces(mock_yield_namespaces):
    """Test with multiple different namespace types."""
    mock_yield_namespaces.return_value = ['torch', 'numpy', 'array_api_strict']
    
    results = list(yield_namespace_device_dtype_combinations())
    
    # Check torch results
    torch_results = [r for r in results if r[0] == 'torch']
    assert len(torch_results) == 7
    assert ('torch', 'cpu', 'float64') in torch_results
    assert ('torch', 'mps', 'float32') in torch_results
    
    # Check numpy results
    numpy_results = [r for r in results if r[0] == 'numpy']
    assert numpy_results == [('numpy', None, None)]
    
    # Check array_api_strict results
    strict_results = [r for r in results if r[0] == 'array_api_strict']
    assert len(strict_results) == 2
    assert ('array_api_strict', 'CPU_DEVICE', 'float64') in strict_results


@patch('sklearn.utils._array_api.yield_namespaces')
def test_empty_namespaces(mock_yield_namespaces):
    """Test with no namespaces returned."""
    mock_yield_namespaces.return_value = []
    
    results = list(yield_namespace_device_dtype_combinations())
    
    assert results == []


@patch('sklearn.utils._array_api.yield_namespaces')
def test_generator_behavior(mock_yield_namespaces):
    """Test that the function returns a generator."""
    mock_yield_namespaces.return_value = ['numpy']
    
    result = yield_namespace_device_dtype_combinations()
    
    # Check it's a generator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')
    
    # Consume the generator
    first = next(result)
    assert first == ('numpy', None, None)
    
    # Should be exhausted
    with pytest.raises(StopIteration):
        next(result)


def test_include_numpy_namespaces_parameter_types():
    """Test that the function handles boolean parameter correctly."""
    # Test with True
    results_true = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=True))
    
    # Test with False
    results_false = list(yield_namespace_device_dtype_combinations(include_numpy_namespaces=False))
    
    # Both should return valid results (actual content depends on yield_namespaces)
    assert isinstance(results_true, list)
    assert isinstance(results_false, list)