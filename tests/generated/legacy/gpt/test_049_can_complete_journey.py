import pytest
from greedy_methods.gas_station import can_complete_journey

class GasStation:
    def __init__(self, gas_quantity, cost):
        self.gas_quantity = gas_quantity
        self.cost = cost

def get_gas_stations(gas_quantities, costs):
    return tuple(GasStation(gq, c) for gq, c in zip(gas_quantities, costs))

def test_can_complete_journey_normal_case():
    gas_stations = get_gas_stations([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    assert can_complete_journey(gas_stations) == 3

def test_can_complete_journey_no_solution():
    gas_stations = get_gas_stations([2, 3, 4], [3, 4, 3])
    assert can_complete_journey(gas_stations) == -1

def test_can_complete_journey_exact_gas():
    gas_stations = get_gas_stations([1, 2, 3], [1, 2, 3])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_single_station():
    gas_stations = get_gas_stations([5], [4])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_single_station_insufficient():
    gas_stations = get_gas_stations([3], [4])
    assert can_complete_journey(gas_stations) == -1

def test_can_complete_journey_all_zero():
    gas_stations = get_gas_stations([0, 0, 0], [0, 0, 0])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_large_numbers():
    gas_stations = get_gas_stations([1000000, 2000000, 3000000], [3000000, 2000000, 1000000])
    assert can_complete_journey(gas_stations) == 2

def test_can_complete_journey_negative_gas():
    gas_stations = get_gas_stations([-1, -2, -3], [-1, -2, -3])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_negative_cost():
    gas_stations = get_gas_stations([1, 2, 3], [-1, -2, -3])
    assert can_complete_journey(gas_stations) == 0

def test_can_complete_journey_mixed_signs():
    gas_stations = get_gas_stations([1, -2, 3], [1, 2, -3])
    assert can_complete_journey(gas_stations) == 0