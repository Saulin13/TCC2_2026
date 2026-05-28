import pytest
from cellular_automata.wa_tor import visualise
from cellular_automata.wa_tor import WaTor, Entity

def test_visualise_normal_case(capsys):
    wt = WaTor(3, 3)
    wt.set_planet([
        [Entity(True, coords=(0, 0)), Entity(False, coords=(0, 1)), None],
        [Entity(False, coords=(1, 0)), None, Entity(False, coords=(1, 2))],
        [None, Entity(True, coords=(2, 1)), None]
    ])
    visualise(wt, 0, colour=False)
    captured = capsys.readouterr()
    expected_output = (
        "#  x  . \n"
        "x  .  x \n"
        ".  #  . \n\n"
        " Iteration: 0 | Prey count: 2 | Predator count: 3 | \n"
    )
    assert captured.out == expected_output

def test_visualise_empty_planet(capsys):
    wt = WaTor(3, 3)
    wt.set_planet([
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ])
    visualise(wt, 1, colour=False)
    captured = capsys.readouterr()
    expected_output = (
        ".  .  . \n"
        ".  .  . \n"
        ".  .  . \n\n"
        " Iteration: 1 | Prey count: 0 | Predator count: 0 | \n"
    )
    assert captured.out == expected_output

def test_visualise_all_prey(capsys):
    wt = WaTor(2, 2)
    wt.set_planet([
        [Entity(True, coords=(0, 0)), Entity(True, coords=(0, 1))],
        [Entity(True, coords=(1, 0)), Entity(True, coords=(1, 1))]
    ])
    visualise(wt, 2, colour=False)
    captured = capsys.readouterr()
    expected_output = (
        "#  #  \n"
        "#  #  \n\n"
        " Iteration: 2 | Prey count: 4 | Predator count: 0 | \n"
    )
    assert captured.out == expected_output

def test_visualise_all_predators(capsys):
    wt = WaTor(2, 2)
    wt.set_planet([
        [Entity(False, coords=(0, 0)), Entity(False, coords=(0, 1))],
        [Entity(False, coords=(1, 0)), Entity(False, coords=(1, 1))]
    ])
    visualise(wt, 3, colour=False)
    captured = capsys.readouterr()
    expected_output = (
        "x  x  \n"
        "x  x  \n\n"
        " Iteration: 3 | Prey count: 0 | Predator count: 4 | \n"
    )
    assert captured.out == expected_output

def test_visualise_invalid_iter_number(capsys):
    wt = WaTor(2, 2)
    wt.set_planet([
        [Entity(True, coords=(0, 0)), None],
        [None, Entity(False, coords=(1, 1))]
    ])
    with pytest.raises(ValueError):
        visualise(wt, -1, colour=False)