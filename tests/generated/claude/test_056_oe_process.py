import pytest
from multiprocessing import Pipe
from sorts.odd_even_transposition_parallel import oe_process
import multiprocessing


@pytest.fixture
def mp_context():
    return multiprocessing.get_context('spawn')


def test_oe_process_leftmost_position_even_swap(mp_context):
    """Test leftmost element (position 0) with even swaps."""
    result_pipe = Pipe()
    r_send = Pipe()
    rr_cv = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if i % 2 == 0:
                val = r_send[0].recv()
                rr_cv[1].send(3)
    
    p = mp_context.Process(target=right_neighbor)
    p.start()
    
    oe_process(
        position=0,
        value=5,
        l_send=None,
        r_send=r_send,
        lr_cv=None,
        rr_cv=rr_cv,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 3


def test_oe_process_rightmost_position_odd_swap(mp_context):
    """Test rightmost element (no right neighbor) with odd swaps."""
    result_pipe = Pipe()
    l_send = Pipe()
    lr_cv = Pipe()
    
    def left_neighbor():
        for i in range(10):
            if (i + 1) % 2 != 0:
                val = l_send[0].recv()
                lr_cv[1].send(2)
    
    p = mp_context.Process(target=left_neighbor)
    p.start()
    
    oe_process(
        position=1,
        value=4,
        l_send=l_send,
        r_send=None,
        lr_cv=lr_cv,
        rr_cv=None,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 4


def test_oe_process_middle_position_both_swaps(mp_context):
    """Test middle element that swaps with both neighbors."""
    result_pipe = Pipe()
    l_send = Pipe()
    lr_cv = Pipe()
    r_send = Pipe()
    rr_cv = Pipe()
    
    def neighbors():
        for i in range(10):
            if (i + 2) % 2 == 0:
                val = r_send[0].recv()
                rr_cv[1].send(7)
            elif (i + 2) % 2 != 0:
                val = l_send[0].recv()
                lr_cv[1].send(1)
    
    p = mp_context.Process(target=neighbors)
    p.start()
    
    oe_process(
        position=2,
        value=5,
        l_send=l_send,
        r_send=r_send,
        lr_cv=lr_cv,
        rr_cv=rr_cv,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 5


def test_oe_process_takes_minimum_on_left(mp_context):
    """Test that left position takes minimum value."""
    result_pipe = Pipe()
    r_send = Pipe()
    rr_cv = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if i % 2 == 0:
                val = r_send[0].recv()
                rr_cv[1].send(10)
    
    p = mp_context.Process(target=right_neighbor)
    p.start()
    
    oe_process(
        position=0,
        value=2,
        l_send=None,
        r_send=r_send,
        lr_cv=None,
        rr_cv=rr_cv,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 2


def test_oe_process_takes_maximum_on_right(mp_context):
    """Test that right position takes maximum value."""
    result_pipe = Pipe()
    l_send = Pipe()
    lr_cv = Pipe()
    
    def left_neighbor():
        for i in range(10):
            if (i + 1) % 2 != 0:
                val = l_send[0].recv()
                lr_cv[1].send(15)
    
    p = mp_context.Process(target=left_neighbor)
    p.start()
    
    oe_process(
        position=1,
        value=8,
        l_send=l_send,
        r_send=None,
        lr_cv=lr_cv,
        rr_cv=None,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 15


def test_oe_process_negative_values(mp_context):
    """Test with negative values."""
    result_pipe = Pipe()
    r_send = Pipe()
    rr_cv = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if i % 2 == 0:
                val = r_send[0].recv()
                rr_cv[1].send(-5)
    
    p = mp_context.Process(target=right_neighbor)
    p.start()
    
    oe_process(
        position=0,
        value=-10,
        l_send=None,
        r_send=r_send,
        lr_cv=None,
        rr_cv=rr_cv,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == -10


def test_oe_process_equal_values(mp_context):
    """Test with equal values."""
    result_pipe = Pipe()
    r_send = Pipe()
    rr_cv = Pipe()
    
    def right_neighbor():
        for i in range(10):
            if i % 2 == 0:
                val = r_send[0].recv()
                rr_cv[1].send(5)
    
    p = mp_context.Process(target=right_neighbor)
    p.start()
    
    oe_process(
        position=0,
        value=5,
        l_send=None,
        r_send=r_send,
        lr_cv=None,
        rr_cv=rr_cv,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    p.join()
    assert result == 5


def test_oe_process_single_element_no_neighbors(mp_context):
    """Test single element with no neighbors."""
    result_pipe = Pipe()
    
    oe_process(
        position=0,
        value=42,
        l_send=None,
        r_send=None,
        lr_cv=None,
        rr_cv=None,
        result_pipe=result_pipe,
        multiprocessing_context=mp_context
    )
    
    result = result_pipe[0].recv()
    assert result == 42