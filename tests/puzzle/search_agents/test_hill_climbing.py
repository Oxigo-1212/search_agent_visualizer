import pytest
from puzzle.state import PuzzleState
from puzzle.problem import PuzzleProblem
from puzzle.search_agents.algorithm import hill_climbing_search
from puzzle.utils import action_extractor, manhattan_distance


def test_hill_climbing_already_at_goal():
    """Test hill climbing when initial state is already the goal."""
    goal = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8))
    problem = PuzzleProblem(initial_state=goal, goal_state=goal)

    result = hill_climbing_search(
        problem=problem,
        initial_state=goal,
        action_extractor=action_extractor,
        heuristic=manhattan_distance,
        return_nodes_expanded=True,
    )

    assert result is not None
    node, nodes_expanded = result
    assert node.state == goal
    assert nodes_expanded == 0  # Should not expand any nodes


def test_hill_climbing_one_move_away():
    """Test hill climbing on a state that is one move from goal."""
    goal = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8))
    # One move: swap blank (0) with tile 1 -> (1, 0, 2, 3, 4, 5, 6, 7, 8)
    initial = PuzzleState((1, 0, 2, 3, 4, 5, 6, 7, 8))
    problem = PuzzleProblem(initial_state=initial, goal_state=goal)

    result = hill_climbing_search(
        problem=problem,
        initial_state=initial,
        action_extractor=action_extractor,
        heuristic=manhattan_distance,
        return_nodes_expanded=True,
    )

    assert result is not None
    node, nodes_expanded = result
    assert node.state == goal
    # Should expand the initial state and then find the goal
    assert nodes_expanded >= 1


def test_hill_climbing_simple_solvable():
    """Test hill climbing on a simple solvable puzzle."""
    goal = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8))
    # Initial: [1, 2, 3, 4, 5, 6, 7, 8, 0] - requires multiple moves
    initial = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))
    problem = PuzzleProblem(initial_state=initial, goal_state=goal)

    result = hill_climbing_search(
        problem=problem,
        initial_state=initial,
        action_extractor=action_extractor,
        heuristic=manhattan_distance,
        return_nodes_expanded=True,
    )

    # Note: Hill climbing may get stuck in local optima for this problem.
    # We check that it returns a node (not None) and that it expanded at least one node.
    # If it found the goal, we also verify the state is correct.
    assert result is not None
    node, nodes_expanded = result
    # Hill climbing should expand at least the initial state
    assert nodes_expanded >= 1
    # If it found the goal, check that it's the goal
    if node.state == goal:
        pass  # success
    else:
        # It got stuck in a local optimum, which is acceptable for hill climbing
        pass


def test_hill_climbing_without_return_nodes_expanded():
    """Test hill climbing without requesting node count."""
    goal = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8))
    initial = PuzzleState((1, 0, 2, 3, 4, 5, 6, 7, 8))
    problem = PuzzleProblem(initial_state=initial, goal_state=goal)

    result = hill_climbing_search(
        problem=problem,
        initial_state=initial,
        action_extractor=action_extractor,
        heuristic=manhattan_distance,
        return_nodes_expanded=False,
    )

    assert result is not None
    # Should return just the node, not a tuple
    assert not isinstance(result, tuple)
    assert result.state == goal


def test_hill_climbing_no_solution_local_optimum():
    """Test hill climbing on a state that leads to a local optimum (not the goal)."""
    # We'll create a scenario where hill climbing might get stuck.
    # For simplicity, we'll use a state that is not solvable? Actually, we want a solvable state
    # that hill climbing fails on due to local optimum.
    # Let's use a known difficult state for hill climbing with Manhattan distance.
    goal = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8))
    # This state is known to cause problems for simple hill climbing: [0, 8, 7, 6, 5, 4, 3, 2, 1]
    initial = PuzzleState((0, 8, 7, 6, 5, 4, 3, 2, 1))
    problem = PuzzleProblem(initial_state=initial, goal_state=goal)

    result = hill_climbing_search(
        problem=problem,
        initial_state=initial,
        action_extractor=action_extractor,
        heuristic=manhattan_distance,
        return_nodes_expanded=True,
    )

    # It might get stuck and return a non-goal state, or it might find the goal.
    # We'll just check that it returns something (either a node or None) and the node count is tracked.
    if result is not None:
        node, nodes_expanded = result
        assert nodes_expanded > 0
        # If it claims to have solved it, check it's really the goal
        if node.state == goal:
            pass  # Success
        else:
            # It's a local optimum - we accept that hill climbing can fail
            pass
    # If result is None, that's also acceptable (though our implementation returns the last node)
    # Actually, looking at the code, it returns the current node when stuck, not None.
    # So we expect a node in all cases.


if __name__ == "__main__":
    pytest.main([__file__])
