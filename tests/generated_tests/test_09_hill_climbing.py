import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from searches.hill_climbing import hill_climbing
import os
import sys




import pytest
import math
from unittest.mock import MagicMock

# Mocking the SearchProblem class
class MockSearchProblem:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self._score = score

    def score(self):
        return self._score

    def get_neighbors(self):
        # This should return a list of neighboring states
        return []

# Test cases for hill_climbing function
def test_hill_climbing_maximization():
    # Create a mock search problem
    initial_state = MockSearchProblem(0, 0, 0)
    
    # Mock the get_neighbors method to return a list of neighbors
    neighbor1 = MockSearchProblem(1, 0, 10)
    neighbor2 = MockSearchProblem(0, 1, 5)
    initial_state.get_neighbors = MagicMock(return_value=[neighbor1, neighbor2])
    
    # Run the hill climbing algorithm
    result = hill_climbing(initial_state, find_max=True, max_iter=10)
    
    # Check if the result is the neighbor with the highest score
    assert result == neighbor1

def test_hill_climbing_minimization():
    # Create a mock search problem
    initial_state = MockSearchProblem(0, 0, 10)
    
    # Mock the get_neighbors method to return a list of neighbors
    neighbor1 = MockSearchProblem(1, 0, 0)
    neighbor2 = MockSearchProblem(0, 1, 5)
    initial_state.get_neighbors = MagicMock(return_value=[neighbor1, neighbor2])
    
    # Run the hill climbing algorithm
    result = hill_climbing(initial_state, find_max=False, max_iter=10)
    
    # Check if the result is the neighbor with the lowest score
    assert result == neighbor1

def test_hill_climbing_no_improvement():
    # Create a mock search problem
    initial_state = MockSearchProblem(0, 0, 10)
    
    # Mock the get_neighbors method to return a list of neighbors with no improvement
    neighbor1 = MockSearchProblem(1, 0, 10)
    neighbor2 = MockSearchProblem(0, 1, 10)
    initial_state.get_neighbors = MagicMock(return_value=[neighbor1, neighbor2])
    
    # Run the hill climbing algorithm
    result = hill_climbing(initial_state, find_max=True, max_iter=10)
    
    # Check if the result is the initial state since no improvement is possible
    assert result == initial_state

def test_hill_climbing_with_bounds():
    # Create a mock search problem
    initial_state = MockSearchProblem(0, 0, 0)
    
    # Mock the get_neighbors method to return a list of neighbors
    neighbor1 = MockSearchProblem(1, 0, 10)
    neighbor2 = MockSearchProblem(0, 1, 5)
    initial_state.get_neighbors = MagicMock(return_value=[neighbor1, neighbor2])
    
    # Run the hill climbing algorithm with bounds
    result = hill_climbing(initial_state, find_max=True, max_x=0.5, max_iter=10)
    
    # Check if the result is the initial state since neighbors are out of bounds
    assert result == initial_state

