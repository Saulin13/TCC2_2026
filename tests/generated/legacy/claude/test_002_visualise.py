import pytest
from unittest.mock import Mock, patch, call
from cellular_automata.wa_tor import visualise, WaTor, Entity


@pytest.fixture
def mock_wator():
    wt = Mock(spec=WaTor)
    wt.planet = []
    wt.get_entities = Mock(return_value=[])
    return wt


def test_visualise_empty_planet_no_colour(capsys, mock_wator):
    mock_wator.planet = [[None, None], [None, None]]
    mock_wator.get_entities.return_value = []
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 0, colour=False)
    
    captured = capsys.readouterr()
    assert " .  . " in captured.out
    assert "Iteration: 0" in captured.out
    assert "Prey count: 0" in captured.out
    assert "Predator count: 0" in captured.out


def test_visualise_with_prey_and_predators_no_colour(capsys, mock_wator):
    prey1 = Entity(True, coords=(0, 0))
    prey2 = Entity(True, coords=(2, 1))
    predator1 = Entity(False, coords=(0, 1))
    predator2 = Entity(False, coords=(1, 0))
    predator3 = Entity(False, coords=(1, 2))
    
    mock_wator.planet = [
        [prey1, predator1, None],
        [predator2, None, predator3],
        [None, prey2, None]
    ]
    mock_wator.get_entities.return_value = [prey1, predator1, predator2, predator3, prey2]
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 5, colour=False)
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert " #  x  . " in lines[0]
    assert " x  .  x " in lines[1]
    assert " .  #  . " in lines[2]
    assert "Iteration: 5" in captured.out
    assert "Prey count: 2" in captured.out
    assert "Predator count: 3" in captured.out


def test_visualise_only_prey_no_colour(capsys, mock_wator):
    prey1 = Entity(True, coords=(0, 0))
    prey2 = Entity(True, coords=(0, 1))
    
    mock_wator.planet = [[prey1, prey2]]
    mock_wator.get_entities.return_value = [prey1, prey2]
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 10, colour=False)
    
    captured = capsys.readouterr()
    assert " #  # " in captured.out
    assert "Iteration: 10" in captured.out
    assert "Prey count: 2" in captured.out
    assert "Predator count: 0" in captured.out


def test_visualise_only_predators_no_colour(capsys, mock_wator):
    predator1 = Entity(False, coords=(0, 0))
    predator2 = Entity(False, coords=(1, 0))
    
    mock_wator.planet = [[predator1], [predator2]]
    mock_wator.get_entities.return_value = [predator1, predator2]
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 99, colour=False)
    
    captured = capsys.readouterr()
    assert " x " in captured.out
    assert "Iteration: 99" in captured.out
    assert "Prey count: 0" in captured.out
    assert "Predator count: 2" in captured.out


def test_visualise_with_colour_enabled(capsys, mock_wator):
    prey = Entity(True, coords=(0, 0))
    predator = Entity(False, coords=(0, 1))
    
    mock_wator.planet = [[prey, predator]]
    mock_wator.get_entities.return_value = [prey, predator]
    
    with patch('cellular_automata.wa_tor.sleep'):
        with patch('os.system') as mock_system:
            visualise(mock_wator, 1, colour=True)
    
    captured = capsys.readouterr()
    assert "\x1b[38;2;96;241;151m" in captured.out  # Prey color
    assert "\x1b[38;2;255;255;15m" in captured.out  # Predator color
    assert "\x1b[0m" in captured.out  # Color end
    assert "\x1b[0;0H" in captured.out  # Cursor positioning
    assert "Iteration: 1" in captured.out
    assert "Prey count: 1" in captured.out
    assert "Predator count: 1" in captured.out
    mock_system.assert_called_once_with("")


def test_visualise_large_iteration_number(capsys, mock_wator):
    mock_wator.planet = [[None]]
    mock_wator.get_entities.return_value = []
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 999999, colour=False)
    
    captured = capsys.readouterr()
    assert "Iteration: 999999" in captured.out


def test_visualise_single_cell_planet(capsys, mock_wator):
    prey = Entity(True, coords=(0, 0))
    mock_wator.planet = [[prey]]
    mock_wator.get_entities.return_value = [prey]
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 0, colour=False)
    
    captured = capsys.readouterr()
    assert " # " in captured.out
    assert "Prey count: 1" in captured.out
    assert "Predator count: 0" in captured.out


def test_visualise_sleep_called(mock_wator):
    mock_wator.planet = [[None]]
    mock_wator.get_entities.return_value = []
    
    with patch('cellular_automata.wa_tor.sleep') as mock_sleep:
        visualise(mock_wator, 0, colour=False)
    
    mock_sleep.assert_called_once_with(0.05)


def test_visualise_mixed_large_planet(capsys, mock_wator):
    planet = []
    entities = []
    for i in range(5):
        row = []
        for j in range(5):
            if (i + j) % 3 == 0:
                entity = Entity(True, coords=(i, j))
                row.append(entity)
                entities.append(entity)
            elif (i + j) % 3 == 1:
                entity = Entity(False, coords=(i, j))
                row.append(entity)
                entities.append(entity)
            else:
                row.append(None)
        planet.append(row)
    
    mock_wator.planet = planet
    mock_wator.get_entities.return_value = entities
    
    with patch('cellular_automata.wa_tor.sleep'):
        visualise(mock_wator, 42, colour=False)
    
    captured = capsys.readouterr()
    assert "Iteration: 42" in captured.out
    prey_count = sum(1 for e in entities if e.prey)
    predator_count = len(entities) - prey_count
    assert f"Prey count: {prey_count}" in captured.out
    assert f"Predator count: {predator_count}" in captured.out