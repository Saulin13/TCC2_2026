import pytest
from greedy_methods.gas_station import can_complete_journey, get_gas_stations


def test_can_complete_journey_normal_case():
    gas_stations = get_gas_stations([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    assert can_complete_journey(gas_stations) == 3


def test_can_complete_journey_impossible():
    gas_stations = get_gas_stations([2, 3, 4], [3, 4, 3])
    assert can_complete_journey(gas_stations) == -1


def test_can_complete_journey_start_at_zero():
    gas_stations = get_gas_stations([5, 1, 2, 3, 4], [1, 2, 3, 4, 5])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_single_station_possible():
    gas_stations = get_gas_stations([5], [3])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_single_station_impossible():
    gas_stations = get_gas_stations([2], [5])
    assert can_complete_journey(gas_stations) == -1


def test_can_complete_journey_exact_match():
    gas_stations = get_gas_stations([3, 3, 3], [3, 3, 3])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_all_surplus():
    gas_stations = get_gas_stations([10, 10, 10], [1, 1, 1])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_last_station():
    gas_stations = get_gas_stations([1, 1, 10], [5, 5, 1])
    assert can_complete_journey(gas_stations) == 2


def test_can_complete_journey_multiple_resets():
    gas_stations = get_gas_stations([1, 5, 1, 5, 1], [2, 1, 2, 1, 2])
    assert can_complete_journey(gas_stations) == 1


def test_can_complete_journey_empty_tuple():
    gas_stations = get_gas_stations([], [])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_two_stations_possible():
    gas_stations = get_gas_stations([3, 2], [2, 1])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_two_stations_impossible():
    gas_stations = get_gas_stations([1, 1], [2, 2])
    assert can_complete_journey(gas_stations) == -1


def test_can_complete_journey_large_numbers():
    gas_stations = get_gas_stations([1000, 500, 2000], [800, 900, 1500])
    assert can_complete_journey(gas_stations) == 0


def test_can_complete_journey_barely_possible():
    gas_stations = get_gas_stations([2, 3, 1], [3, 1, 2])
    assert can_complete_journey(gas_stations) == 1


def test_can_complete_journey_zero_gas_and_cost():
    gas_stations = get_gas_stations([0, 0, 5], [0, 0, 5])
    assert can_complete_journey(gas_stations) == 0