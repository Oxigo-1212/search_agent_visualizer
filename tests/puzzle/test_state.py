import pytest
import attrs
from puzzle.state import PuzzleState


# pytest fixtures for reusable test data


@pytest.fixture
def solved_state() -> PuzzleState:
    return PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))


@pytest.fixture
def scrambled_state() -> PuzzleState:
    return PuzzleState((1, 2, 3, 4, 0, 5, 7, 8, 6))


def test_valid_permutaion_accepts(solved_state: PuzzleState):
    assert solved_state.tiles == (1, 2, 3, 4, 5, 6, 7, 8, 0)


def test_invalid_duplicate_raises():
    with pytest.raises(ValueError, match="Tiles must be a permutation"):
        PuzzleState(tiles=(0, 0, 1, 2, 3, 4, 5, 6, 7))  # duplicate 0


def test_invalid_out_of_range_raises():
    with pytest.raises(ValueError, match="Tiles must be a permutation"):
        # 9 is out of 0‑8 range
        PuzzleState(tiles=(0, 1, 2, 3, 4, 5, 6, 7, 9))


def test_immutable_state(solved_state):
    with pytest.raises(attrs.exceptions.FrozenInstanceError):
        # assignment should fail
        solved_state.tiles = (1, 2, 3, 4, 5, 6, 7, 8, 0)
