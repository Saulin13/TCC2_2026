import pytest
from multiprocessing import Pipe, get_context
from sorts.odd_even_transposition_parallel import oe_process

@pytest.fixture
def setup_pipes():
    l_send, l_recv = Pipe()
    r_send, r_recv = Pipe()
    result_send, result_recv = Pipe()
    return (l_send, l_recv), (r_send, r_recv), (result_send, result_recv)

def test_oe_process_normal_case(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Simulate a process with position 0, value 5, and right neighbor with value 3
    r_send[0].send(3)
    oe_process(0, 5, l_send, r_send, l_send, r_send, result_pipe, multiprocessing_context)
    
    # Expect the process to take the minimum value, which is 3
    assert result_pipe[0].recv() == 3

def test_oe_process_edge_case_no_neighbors(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Simulate a process with position 0, value 5, and no neighbors
    oe_process(0, 5, None, None, l_send, r_send, result_pipe, multiprocessing_context)
    
    # Expect the process to retain its original value, which is 5
    assert result_pipe[0].recv() == 5

def test_oe_process_edge_case_single_swap(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Simulate a process with position 1, value 7, and left neighbor with value 10
    l_send[0].send(10)
    oe_process(1, 7, l_send, r_send, l_send, r_send, result_pipe, multiprocessing_context)
    
    # Expect the process to take the maximum value, which is 10
    assert result_pipe[0].recv() == 10

def test_oe_process_failure_invalid_pipe(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Simulate a process with position 0, value 5, and invalid pipe
    with pytest.raises(OSError):
        oe_process(0, 5, l_send, None, l_send, r_send, result_pipe, multiprocessing_context)