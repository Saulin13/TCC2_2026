import pytest
from divide_and_conquer.max_subarray import plot_runtimes
import matplotlib.pyplot as plt

def mock_time_max_subarray(input_size):
    # Mock function to simulate time taken for different input sizes
    return input_size * 0.0001  # Simulate a linear time complexity

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    # Mock the time_max_subarray function
    monkeypatch.setattr('divide_and_conquer.max_subarray.time_max_subarray', mock_time_max_subarray)

def test_plot_runtimes_normal_case(mocker):
    # Mock plt.show to prevent the plot from displaying during tests
    mock_show = mocker.patch('matplotlib.pyplot.show')

    # Call the function
    plot_runtimes()

    # Check if plt.plot was called with expected arguments
    expected_input_sizes = [10, 100, 1000, 10000, 50000, 100000, 200000, 300000, 400000, 500000]
    expected_runtimes = [mock_time_max_subarray(size) for size in expected_input_sizes]
    plt.plot.assert_called_once_with(expected_input_sizes, expected_runtimes)

    # Check if plt.show was called once
    mock_show.assert_called_once()

def test_plot_runtimes_edge_case_empty_input(mocker):
    # Mock plt.show to prevent the plot from displaying during tests
    mock_show = mocker.patch('matplotlib.pyplot.show')

    # Mock input_sizes to simulate an edge case with empty input
    mocker.patch('divide_and_conquer.max_subarray.plot_runtimes.input_sizes', [])

    # Call the function
    plot_runtimes()

    # Check if plt.plot was called with empty lists
    plt.plot.assert_called_once_with([], [])

    # Check if plt.show was called once
    mock_show.assert_called_once()

def test_plot_runtimes_failure_case(mocker):
    # Mock plt.show to prevent the plot from displaying during tests
    mock_show = mocker.patch('matplotlib.pyplot.show')

    # Mock time_max_subarray to raise an exception
    mocker.patch('divide_and_conquer.max_subarray.time_max_subarray', side_effect=Exception("Test Exception"))

    # Call the function and expect it to handle the exception
    with pytest.raises(Exception, match="Test Exception"):
        plot_runtimes()

    # Ensure plt.show was not called due to the exception
    mock_show.assert_not_called()