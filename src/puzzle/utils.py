from typing import Tuple
from puzzle.state import PuzzleState


def action_extractor(state: PuzzleState, neighbor: PuzzleState) -> Tuple[int, int]:
    blank_pos = state.tiles.index(0)
    n_blank_pos = neighbor.tiles.index(0)

    # Convert the 1D tuple to the 2D grid coordinates
    s_row, s_col = divmod(blank_pos, 3)
    n_row, n_col = divmod(n_blank_pos, 3)

    # Return the change in position
    return (n_row - s_row, n_col - s_col)
