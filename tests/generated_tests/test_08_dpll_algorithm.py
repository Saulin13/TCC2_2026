import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from other.davis_putnam_logemann_loveland import dpll_algorithm
import os
import sys




import pytest

def test_dpll_algorithm():
    # Mock classes and functions to simulate the environment
    class Clause:
        def __init__(self, literals):
            self.literals = literals

        def evaluate(self, model):
            # Simulate evaluation logic
            if all(lit in model and model[lit] is True for lit in self.literals):
                return True
            if any(lit in model and model[lit] is False for lit in self.literals):
                return False
            return None

    def find_pure_symbols(clauses, symbols, model):
        # Simulate finding pure symbols
        return [], {}

    def find_unit_clauses(clauses, model):
        # Simulate finding unit clauses
        return [], {}

    # Test case 1: Simple satisfiable formula
    clauses = [Clause(["A"]), Clause(["A", "B"])]
    symbols = ["A", "B"]
    model = {}
    soln, result_model = dpll_algorithm(clauses, symbols, model)
    assert soln is True
    assert result_model == {'A': True}

    # Test case 2: Simple unsatisfiable formula
    clauses = [Clause(["A"]), Clause(["A'"])]
    symbols = ["A"]
    model = {}
    soln, result_model = dpll_algorithm(clauses, symbols, model)
    assert soln is False
    assert result_model is None

    # Test case 3: Complex satisfiable formula
    clauses = [Clause(["A", "B"]), Clause(["A'", "B"]), Clause(["B'"])]
    symbols = ["A", "B"]
    model = {}
    soln, result_model = dpll_algorithm(clauses, symbols, model)
    assert soln is True
    assert result_model == {'A': False, 'B': False}

    # Test case 4: Complex unsatisfiable formula
    clauses = [Clause(["A", "B"]), Clause(["A'", "B'"]), Clause(["A", "B'"]), Clause(["A'", "B"])]
    symbols = ["A", "B"]
    model = {}
    soln, result_model = dpll_algorithm(clauses, symbols, model)
    assert soln is False
    assert result_model is None

    # Test case 5: Empty clauses
    clauses = []
    symbols = []
    model = {}
    soln, result_model = dpll_algorithm(clauses, symbols, model)
    assert soln is True
    assert result_model == {}

pytest.main()
