import pytest
from divide_and_conquer.max_subarray import plot_runtimes
import matplotlib.pyplot as plt

def mock_time_max_subarray(input_size):
    # Mock function to simulate runtime based on input size
    return input_size * 0.0001  # Simulate a linear time complexity

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    # Mock the time_max_subarray function
    monkeypatch.setattr('divide_and_conquer.max_subarray.time_max_subarray', mock_time_max_subarray)

def test_plot_runtimes_normal_case(monkeypatch):
    # Mock plt.show to prevent it from blocking the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    # Capture the printed output
    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output

    plot_runtimes()

    # Reset redirect.
    sys.stdout = sys.__stdout__

    # Check if the output contains expected strings
    output = captured_output.getvalue()
    assert "No of Inputs\t\tTime Taken" in output
    assert "10 \t\t 0.001" in output
    assert "100000 \t\t 10.0" in output
    assert "500000 \t\t 50.0" in output

def test_plot_runtimes_edge_case_empty_input_sizes(monkeypatch):
    # Mock plt.show to prevent it from blocking the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    # Mock input_sizes to be empty
    monkeypatch.setattr('divide_and_conquer.max_subarray.plot_runtimes', lambda: None)

    # Capture the printed output
    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output

    # Call the function with empty input_sizes
    plot_runtimes()

    # Reset redirect.
    sys.stdout = sys.__stdout__

    # Check if the output is empty or contains specific message
    output = captured_output.getvalue()
    assert output == "" or "No of Inputs\t\tTime Taken" not in output

def test_plot_runtimes_failure_case_invalid_runtime(monkeypatch):
    # Mock plt.show to prevent it from blocking the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    # Mock time_max_subarray to return an invalid runtime
    def mock_invalid_time_max_subarray(input_size):
        if input_size == 1000:
            return -1  # Invalid runtime
        return input_size * 0.0001

    monkeypatch.setattr('divide_and_conquer.max_subarray.time_max_subarray', mock_invalid_time_max_subarray)

    # Capture the printed output
    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output

    plot_runtimes()

    # Reset redirect.
    sys.stdout = sys.__stdout__

    # Check if the output contains the invalid runtime
    output = captured_output.getvalue()
    assert "1000 \t\t -1" in output