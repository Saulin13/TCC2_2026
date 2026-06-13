import pytest
from multiprocessing import Pipe
from sorts.odd_even_transposition_parallel import oe_process


def test_oe_process_leftmost_position_even():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 0
    value = 5
    l_send = None
    r_send = Pipe()
    lr_cv = None
    rr_cv = Pipe()
    result_pipe = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if (i + position) % 2 == 0:
                neighbor_value = r_send[0].recv()
                rr_cv[1].send(3)
    
    import threading
    t = threading.Thread(target=right_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 3


def test_oe_process_rightmost_position_odd():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 1
    value = 2
    l_send = Pipe()
    r_send = None
    lr_cv = Pipe()
    rr_cv = None
    result_pipe = Pipe()
    
    def left_neighbor():
        for i in range(10):
            if (i + position) % 2 != 0:
                neighbor_value = l_send[0].recv()
                lr_cv[1].send(7)
    
    import threading
    t = threading.Thread(target=left_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 7


def test_oe_process_middle_position_exchanges_both_sides():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 1
    value = 5
    l_send = Pipe()
    r_send = Pipe()
    lr_cv = Pipe()
    rr_cv = Pipe()
    result_pipe = Pipe()
    
    def neighbors():
        for i in range(10):
            if (i + position) % 2 == 0:
                neighbor_value = r_send[0].recv()
                rr_cv[1].send(6)
            elif (i + position) % 2 != 0:
                neighbor_value = l_send[0].recv()
                lr_cv[1].send(4)
    
    import threading
    t = threading.Thread(target=neighbors)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 5


def test_oe_process_position_zero_keeps_minimum():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 0
    value = 10
    l_send = None
    r_send = Pipe()
    lr_cv = None
    rr_cv = Pipe()
    result_pipe = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if (i + position) % 2 == 0:
                neighbor_value = r_send[0].recv()
                rr_cv[1].send(20)
    
    import threading
    t = threading.Thread(target=right_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 10


def test_oe_process_position_one_keeps_maximum():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 1
    value = 15
    l_send = Pipe()
    r_send = None
    lr_cv = Pipe()
    rr_cv = None
    result_pipe = Pipe()
    
    def left_neighbor():
        for i in range(10):
            if (i + position) % 2 != 0:
                neighbor_value = l_send[0].recv()
                lr_cv[1].send(8)
    
    import threading
    t = threading.Thread(target=left_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 15


def test_oe_process_negative_values():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 0
    value = -5
    l_send = None
    r_send = Pipe()
    lr_cv = None
    rr_cv = Pipe()
    result_pipe = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if (i + position) % 2 == 0:
                neighbor_value = r_send[0].recv()
                rr_cv[1].send(-10)
    
    import threading
    t = threading.Thread(target=right_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == -10


def test_oe_process_equal_values():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 0
    value = 7
    l_send = None
    r_send = Pipe()
    lr_cv = None
    rr_cv = Pipe()
    result_pipe = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if (i + position) % 2 == 0:
                neighbor_value = r_send[0].recv()
                rr_cv[1].send(7)
    
    import threading
    t = threading.Thread(target=right_neighbor)
    t.start()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    t.join()
    result = result_pipe[0].recv()
    assert result == 7


def test_oe_process_single_element_no_neighbors():
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    
    position = 0
    value = 42
    l_send = None
    r_send = None
    lr_cv = None
    rr_cv = None
    result_pipe = Pipe()
    
    oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx)
    
    result = result_pipe[0].recv()
    assert result == 42