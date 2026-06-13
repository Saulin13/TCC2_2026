import pytest
from unittest.mock import patch, MagicMock
from cellular_automata.wa_tor import visualise, WaTor, Entity


@pytest.fixture
def simple_wator():
    wt = WaTor(3, 3)
    wt.set_planet([
        [Entity(True, coords=(0, 0)), Entity(False, coords=(0, 1)), None],
        [Entity(False, coords=(1, 0)), None, Entity(False, coords=(1, 2))],
        [None, Entity(True, coords=(2, 1)), None]
    ])
    return wt


@pytest.fixture
def empty_wator():
    wt = WaTor(2, 2)
    wt.set_planet([
        [None, None],
        [None, None]
    ])
    return wt


@pytest.fixture
def all_prey_wator():
    wt = WaTor(2, 2)
    wt.set_planet([
        [Entity(True, coords=(0, 0)), Entity(True, coords=(0, 1))],
        [Entity(True, coords=(1, 0)), Entity(True, coords=(1, 1))]
    ])
    return wt


@pytest.fixture
def all_predator_wator():
    wt = WaTor(2, 2)
    wt.set_planet([
        [Entity(False, coords=(0, 0)), Entity(False, coords=(0, 1))],
        [Entity(False, coords=(1, 0)), Entity(False, coords=(1, 1))]
    ])
    return wt


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_without_colour(mock_sleep, mock_print, simple_wator):
    visualise(simple_wator, 0, colour=False)
    
    mock_sleep.assert_called_once_with(0.05)
    assert mock_print.call_count == 1
    
    output = mock_print.call_args[0][0]
    assert " #  x  . " in output
    assert " x  .  x " in output
    assert " .  #  . " in output
    assert "Iteration: 0" in output
    assert "Prey count: 2" in output
    assert "Predator count: 3" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_with_colour(mock_sleep, mock_print, simple_wator):
    with patch('os.system') as mock_system:
        visualise(simple_wator, 5, colour=True)
    
    mock_system.assert_called_once_with("")
    mock_sleep.assert_called_once_with(0.05)
    assert mock_print.call_count == 2
    
    second_call_output = mock_print.call_args[0][0]
    assert "Iteration: 5" in second_call_output
    assert "Prey count: 2" in second_call_output
    assert "Predator count: 3" in second_call_output
    assert "\x1b[0;0H" in second_call_output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_empty_planet(mock_sleep, mock_print, empty_wator):
    visualise(empty_wator, 10, colour=False)
    
    output = mock_print.call_args[0][0]
    assert " .  . " in output
    assert "Iteration: 10" in output
    assert "Prey count: 0" in output
    assert "Predator count: 0" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_all_prey(mock_sleep, mock_print, all_prey_wator):
    visualise(all_prey_wator, 3, colour=False)
    
    output = mock_print.call_args[0][0]
    assert " #  # " in output
    assert "Prey count: 4" in output
    assert "Predator count: 0" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_all_predators(mock_sleep, mock_print, all_predator_wator):
    visualise(all_predator_wator, 7, colour=False)
    
    output = mock_print.call_args[0][0]
    assert " x  x " in output
    assert "Prey count: 0" in output
    assert "Predator count: 4" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_large_iteration_number(mock_sleep, mock_print, simple_wator):
    visualise(simple_wator, 999999, colour=False)
    
    output = mock_print.call_args[0][0]
    assert "Iteration: 999999" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_negative_iteration_number(mock_sleep, mock_print, simple_wator):
    visualise(simple_wator, -5, colour=False)
    
    output = mock_print.call_args[0][0]
    assert "Iteration: -5" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_single_cell_planet(mock_sleep, mock_print):
    wt = WaTor(1, 1)
    wt.set_planet([[Entity(True, coords=(0, 0))]])
    
    visualise(wt, 0, colour=False)
    
    output = mock_print.call_args[0][0]
    assert " # " in output
    assert "Prey count: 1" in output
    assert "Predator count: 0" in output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_colour_codes_present(mock_sleep, mock_print, simple_wator):
    with patch('os.system'):
        visualise(simple_wator, 0, colour=True)
    
    second_call_output = mock_print.call_args[0][0]
    assert "\x1b[0m" in second_call_output
    assert "\x1b[0;0H" in second_call_output


@patch('builtins.print')
@patch('cellular_automata.wa_tor.sleep')
def test_visualise_sleep_called(mock_sleep, mock_print, simple_wator):
    visualise(simple_wator, 0, colour=False)
    
    mock_sleep.assert_called_once_with(0.05)