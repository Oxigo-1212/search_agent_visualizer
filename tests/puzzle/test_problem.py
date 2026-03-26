import pytest
from puzzle.state import PuzzleState
from puzzle.problem import PuzzleProblem


@pytest.fixture
def goal_state() -> PuzzleState:
    return PuzzleState(tiles=(0, 1, 2, 3, 4, 5, 6, 7, 8))


@pytest.fixture
def start_state() -> PuzzleState:
    return PuzzleState(tiles=(1, 2, 3, 4, 0, 5, 6, 7, 8))


@pytest.fixture
def problem(start_state: PuzzleState, goal_state: PuzzleState) -> PuzzleProblem:
    return PuzzleProblem(initial_state=start_state, goal_state=goal_state)


@pytest.fixture
def problem_factory(start_state: PuzzleState, goal_state: PuzzleState):
    def _create(cost_function=None) -> PuzzleProblem:
        return PuzzleProblem(
            initial_state=start_state,
            goal_state=goal_state,
            cost_function=cost_function,
        )

    return _create


def test_is_goal_false(problem: PuzzleProblem, start_state: PuzzleState):
    assert not problem.is_goal(start_state)


def test_is_goal_true(problem: PuzzleProblem, goal_state: PuzzleState):
    assert problem.is_goal(goal_state)


@pytest.mark.parametrize(
    "tiles, expected_count",
    [
        ((0, 1, 2, 3, 4, 5, 6, 7, 8), 2),  # corner
        ((1, 0, 2, 3, 4, 5, 6, 7, 8), 3),  # edge
        ((1, 2, 3, 4, 0, 5, 6, 7, 8), 4),  # centre
    ],
)
def test_neighbor_counts(problem, tiles, expected_count):
    state = PuzzleState(tiles=tiles)
    neighbours = problem.get_neighbors(state)
    assert len(neighbours) == expected_count


def test_neighbors_are_valid(problem, start_state):
    for nb in problem.get_neighbors(start_state):
        assert isinstance(nb, PuzzleState)


def test_neighbors_are_reversible(problem, start_state):
    for nb in problem.get_neighbors(start_state):
        assert start_state in problem.get_neighbors(nb)


def test_goal_is_reachable_within_few_moves(problem, start_state, goal_state):
    """BFS confirms goal is reachable (minimum 14 moves for this start config)."""
    frontier = [(start_state, 0)]
    visited = {start_state}
    while frontier:
        state, depth = frontier.pop(0)
        if problem.is_goal(state):
            assert depth <= 20
            return
        if depth >= 20:
            continue
        for nb in problem.get_neighbors(state):
            if nb not in visited:
                visited.add(nb)
                frontier.append((nb, depth + 1))
    pytest.fail("Goal not found within depth 20")


def test_step_cost_uniform(problem: PuzzleProblem, start_state: PuzzleState):
    for neighbour in problem.get_neighbors(start_state):
        assert problem.step_cost(start_state, neighbour, action=None) == 1


def test_step_cost_non_uniform(
    problem_factory, start_state: PuzzleState, goal_state: PuzzleState
):
    def cost_function(
        from_state: PuzzleState, to_state: PuzzleState, action: object
    ) -> int:
        return 7 if to_state == goal_state else 3

    custom_problem = problem_factory(cost_function=cost_function)
    assert custom_problem.step_cost(start_state, goal_state, action="move") == 7

    neighbour = custom_problem.get_neighbors(start_state)[0]
    assert custom_problem.step_cost(start_state, neighbour, action="move") == 3
