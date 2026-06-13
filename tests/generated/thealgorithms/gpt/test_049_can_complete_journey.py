import pytest
from greedy_methods.gas_station import can_complete_journey

class GasStation:
    def __init__(self, gas_quantity, cost):
        self.gas_quantity = gas_quantity
        self.cost = cost

def get_gas_stations(gas_quantities, costs):
    return tuple(GasStation(g, c) for g, c in zip(gas_quantities, costs))

def test_can_complete_journey_normal_case():
    gas_stations = get_gas_stations([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    assert can_complete_journey(gas_stations) == 3

def test_can_complete_journey_no_solution():
    gas_stations = get_gas_stations([2, 3, 4], [3, 4, 3])
    assert can_complete_journey(gas_stations) == -1

def test_can_complete_journey_single_station_success():
    gas_stations = get_gas_stations([5], [4])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_single_station_failure():
    gas_stations = get_gas_stations([3], [4])
    assert can_complete_journey(gas_stations) == -1

def test_can_complete_journey_all_stations_same():
    gas_stations = get_gas_stations([1, 1, 1, 1], [1, 1, 1, 1])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_large_input():
    gas_stations = get_gas_stations([10] * 1000, [9] * 1000)
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_edge_case_empty():
    gas_stations = get_gas_stations([], [])
    assert can_complete_journey(gas_stations) == -1

def test_can_complete_journey_exact_gas():
    gas_stations = get_gas_stations([3, 1, 2], [2, 2, 2])
    assert can_complete_journey(gas_stations) == 0