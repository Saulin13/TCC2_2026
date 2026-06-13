import pytest
from multiprocessing import Pipe, get_context
from sorts.odd_even_transposition_parallel import oe_process

@pytest.fixture
def setup_pipes():
    # Setup pipes for communication
    l_send, l_recv = Pipe()
    r_send, r_recv = Pipe()
    result_send, result_recv = Pipe()
    return (l_send, l_recv), (r_send, r_recv), (result_send, result_recv)

def test_oe_process_normal_case(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Test with a simple case where the process is in the middle
    position = 1
    value = 5
    l_send[0].send(3)  # Simulate left neighbor sending 3
    r_send[0].send(7)  # Simulate right neighbor sending 7
    
    oe_process(position, value, l_send, r_send, l_send, r_send, result_pipe, multiprocessing_context)
    
    # Expect the process to take the higher value from the left and send it back
    assert result_pipe[0].recv() == 5

def test_oe_process_edge_case_leftmost(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Test with the leftmost process
    position = 0
    value = 2
    r_send[0].send(1)  # Simulate right neighbor sending 1
    
    oe_process(position, value, None, r_send, None, r_send, result_pipe, multiprocessing_context)
    
    # Expect the process to take the lower value from itself and send it back
    assert result_pipe[0].recv() == 1

def test_oe_process_edge_case_rightmost(setup_pipes):
    l_send, r_send, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Test with the rightmost process
    position = 9
    value = 8
    l_send[0].send(9)  # Simulate left neighbor sending 9
    
    oe_process(position, value, l_send, None, l_send, None, result_pipe, multiprocessing_context)
    
    # Expect the process to take the higher value from the left and send it back
    assert result_pipe[0].recv() == 9

def test_oe_process_failure_case_no_neighbors(setup_pipes):
    _, _, result_pipe = setup_pipes
    multiprocessing_context = get_context('spawn')
    
    # Test with a process having no neighbors
    position = 5
    value = 10
    
    # This should not raise an exception and should return the same value
    oe_process(position, value, None, None, None, None, result_pipe, multiprocessing_context)
    
    assert result_pipe[0].recv() == 10