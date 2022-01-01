import unittest

from vertex import Vertex
from graph import QuokkaMaze


def should_be_equal(got, expected, func, message="Incorrect result returned"):
    """
    Simple Assert Helper Function
    """

    assert expected == got, \
        f"[{func}] MSG: {message} [Expected: {expected}, got: {got}]"


def should_be_true(got, func, message="Incorrect result returned"):
    """
    Simple assert helper
    """

    assert got is not None, \
        f"[{func}] MSG: {message} [Expected True, but got {got}]"

    assert got is True, \
        f"[{func}] MSG: {message} [Expected True, but got {got}]"


def should_be_false(got, func, message="Incorrect result returned"):
    """
    Simple false checker
    """

    assert got is not None, \
        f"[{func}] MSG: {message} [Expected False, but got {got}]"

    assert got is False, \
        f"[{func}] MSG: {message} [Expected False, but got {got}]"


def check_edges(
    u,
    v,
    exists
):
    if exists:
        assert u in v.edges, "Vertex not found in edge list"
        assert v in u.edges, "Vertex not found in edge list"
    else:
        assert u not in v.edges, "Vertex found in edge list when it shouldn't"
        assert v not in u.edges, "Vertex found in edge list when it shouldn't"


def check_path_should_match(
    got,
    expected,
    func="maze.find_path",
    message="Returned incorrect path"
):
    """
    Checks the equality of the path returned.
    """

    # Check length
    assert got is not None, "Returned a `None` response when it shouldn't be."

    should_be_equal(
        len(got),
        len(expected),
        func,
        "Path length did not match expected!"
    )

    # For each vertex, check path matches
    for idx in range(len(expected)):
        should_be_equal(
            got[idx],
            expected[idx],
            func,
            message + f"(index: {idx} failed)"
        )


def check_vertices_lists(
    got,
    expected,
    x,
    func,
    message="Vertices did not match expected ones"
):

    assert got is not None, \
        f"[{func}] You returned None when it should not be."

    assert len(got) <= x, \
        f"[{func}] Length returned > x! (Expected={x}; Got={len(got)})"

    for i in got:
        assert i in expected, \
            f"[{func}] A vertex location you returned was incorrect."


class TestSampleAdvancedThings(unittest.TestCase):

    def test_find_location_sample(self):
        """
        Can we do the example from find_location?
        """

        #                     *
        # A -- B -- C -- D -- E

        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(False)
        D = Vertex(False)
        E = Vertex(True)

        m = QuokkaMaze()

        m.add_vertex(A)
        m.add_vertex(B)
        m.add_vertex(C)
        m.add_vertex(D)
        m.add_vertex(E)

        m.fix_edge(A, B)
        m.fix_edge(B, C)
        m.fix_edge(C, D)
        m.fix_edge(D, E)

        # Example 1
        should_be_true(
            m.find_location_of_extra_food(A, E, 2, 0) is None,
            "maze.find_location_of_extra_food",
            "Expected None"
        )

        # Example 2
        check_vertices_lists(
            m.find_location_of_extra_food(A, E, 2, 1),
            [C],
            1,
            "maze.find_location_of_extra_food"
        )

        # Example 3
        check_vertices_lists(
            m.find_location_of_extra_food(A, E, 1, 6),
            [A, B, C, D],
            6,
            "maze.find_location_of_extra_food"
        )

    def test_minimize_extra_example(self):
        """
        Can we do the example minimize from the comments?
        """

        #                     *
        # A -- B -- C -- D -- E

        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(False)
        D = Vertex(False)
        E = Vertex(True)

        m = QuokkaMaze()

        m.add_vertex(A)
        m.add_vertex(B)
        m.add_vertex(C)
        m.add_vertex(D)
        m.add_vertex(E)

        m.fix_edge(A, B)
        m.fix_edge(B, C)
        m.fix_edge(C, D)
        m.fix_edge(D, E)

        # Example 1
        check_vertices_lists(
            m.minimize_extra_food(
                A, E, 2
            ),
            [C],
            1,
            "maze.minimize_extra_food"
        )

        # Example 2
        check_vertices_lists(
            m.minimize_extra_food(
                A, E, 1
            ),
            [B, C, D],
            3,
            "maze.minimize_extra_food"
        )

        check_vertices_lists(
            m.minimize_extra_food(
                A, A, 0
            ),
            [],
            0,
            "maze.minimize_extra_food"
        )
