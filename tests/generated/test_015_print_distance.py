import pytest
from graphs.bellman_ford import print_distance

def test_print_distance_normal_case(capfd):
    distance = [0, 1.5, 3.2, 4.8]
    src = 0
    print_distance(distance, src)
    captured = capfd.readouterr()
    expected_output = (
        "Vertex\tShortest Distance from vertex 0\n"
        "0\t\t0\n"
        "1\t\t1.5\n"
        "2\t\t3.2\n"
        "3\t\t4.8\n"
    )
    assert captured.out == expected_output

def test_print_distance_edge_case_empty_list(capfd):
    distance = []
    src = 0
    print_distance(distance, src)
    captured = capfd.readouterr()
    expected_output = "Vertex\tShortest Distance from vertex 0\n"
    assert captured.out == expected_output

def test_print_distance_edge_case_single_element(capfd):
    distance = [7.5]
    src = 0
    print_distance(distance, src)
    captured = capfd.readouterr()
    expected_output = (
        "Vertex\tShortest Distance from vertex 0\n"
        "0\t\t7.5\n"
    )
    assert captured.out == expected_output

def test_print_distance_negative_distances(capfd):
    distance = [0, -1.5, -3.2, 4.8]
    src = 0
    print_distance(distance, src)
    captured = capfd.readouterr()
    expected_output = (
        "Vertex\tShortest Distance from vertex 0\n"
        "0\t\t0\n"
        "1\t\t-1.5\n"
        "2\t\t-3.2\n"
        "3\t\t4.8\n"
    )
    assert captured.out == expected_output

def test_print_distance_invalid_input_type():
    with pytest.raises(TypeError):
        print_distance("invalid input", 0)