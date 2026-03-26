import pytest

from puzzle.state import PuzzleState
from puzzle.utils import action_extractor, is_solvable, manhattan_distance


@pytest.fixture
def goal_state() -> PuzzleState:
    return PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))


@pytest.fixture
def solved_state(goal_state: PuzzleState) -> PuzzleState:
    return goal_state


@pytest.mark.parametrize(
    "tiles, expected_distance",
    [
        ((1, 2, 3, 4, 5, 6, 7, 8, 0), 0),
        ((1, 2, 3, 4, 5, 6, 7, 0, 8), 1),
        ((1, 2, 3, 4, 5, 6, 0, 7, 8), 2),
        ((1, 2, 3, 4, 5, 6, 8, 7, 0), 2),
        ((0, 1, 2, 3, 4, 5, 6, 7, 8), 12),
        ((8, 7, 6, 5, 4, 3, 2, 1, 0), 16),
    ],
)
def test_manhattan_distance_known_values(
    goal_state: PuzzleState,
    tiles: tuple[int, ...],
    expected_distance: int,
):
    state = PuzzleState(tiles)

    assert manhattan_distance(state, goal_state) == expected_distance


def test_manhattan_distance_solved_state_is_zero(
    solved_state: PuzzleState, goal_state: PuzzleState
):
    assert manhattan_distance(solved_state, goal_state) == 0


def test_manhattan_distance_counts_only_numbered_tile_after_blank_move(
    goal_state: PuzzleState,
):
    state = PuzzleState((1, 2, 3, 4, 5, 6, 7, 0, 8))

    # Blank and tile 8 swap positions; only tile 8 contributes to the distance.
    assert manhattan_distance(state, goal_state) == 1


def test_manhattan_distance_matches_sum_of_individual_tile_moves(
    goal_state: PuzzleState,
):
    # 1 at index 1 -> goal index 0 (1 move)
    # 2 at index 2 -> goal index 1 (1 move)
    # 3 at index 5 -> goal index 2 (1 move)
    # 4 at index 3 -> goal index 3 (0 moves)
    # 5 at index 4 -> goal index 4 (0 moves)
    # 6 at index 8 -> goal index 5 (1 move)
    # 7 at index 6 -> goal index 6 (0 moves)
    # 8 at index 7 -> goal index 7 (0 moves)
    # total = 4
    state = PuzzleState((0, 1, 2, 4, 5, 3, 7, 8, 6))

    assert manhattan_distance(state, goal_state) == 4


@pytest.mark.parametrize(
    "state_tiles, neighbor_tiles, expected_action",
    [
        ((1, 2, 3, 4, 0, 5, 6, 7, 8), (1, 0, 3, 4, 2, 5, 6, 7, 8), (-1, 0)),
        ((1, 2, 3, 4, 0, 5, 6, 7, 8), (1, 2, 3, 4, 7, 5, 6, 0, 8), (1, 0)),
        ((1, 2, 3, 4, 0, 5, 6, 7, 8), (1, 2, 3, 0, 4, 5, 6, 7, 8), (0, -1)),
        ((1, 2, 3, 4, 0, 5, 6, 7, 8), (1, 2, 3, 4, 5, 0, 6, 7, 8), (0, 1)),
    ],
)
def test_action_extractor_returns_blank_position_delta(
    state_tiles: tuple[int, ...],
    neighbor_tiles: tuple[int, ...],
    expected_action: tuple[int, int],
):
    state = PuzzleState(state_tiles)
    neighbor = PuzzleState(neighbor_tiles)

    assert action_extractor(state, neighbor) == expected_action


def test_action_extractor_returns_zero_delta_for_identical_state():
    state = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))

    assert action_extractor(state, state) == (0, 0)


@pytest.mark.parametrize(
    "state_tiles, expected",
    [
        ((1, 2, 3, 4, 5, 6, 7, 8, 0), True),
        ((1, 2, 3, 4, 5, 6, 7, 0, 8), True),
        ((1, 2, 3, 4, 5, 6, 8, 7, 0), False),
    ],
)
def test_is_solvable_for_common_3x3_configurations(
    goal_state: PuzzleState,
    state_tiles: tuple[int, ...],
    expected: bool,
):
    state = PuzzleState(state_tiles)

    assert is_solvable(state, goal_state) is expected


def test_is_solvable_respects_goal_parity_with_nonstandard_goal():
    goal_state = PuzzleState((1, 2, 3, 4, 5, 6, 8, 7, 0))

    assert is_solvable(PuzzleState((1, 2, 3, 4, 5, 6, 8, 7, 0)), goal_state) is True
    assert is_solvable(PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0)), goal_state) is False
