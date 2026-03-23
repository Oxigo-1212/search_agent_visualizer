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


def is_solvable(state: PuzzleState, goal_state: PuzzleState) -> bool:
    def inversions(seq: Tuple[int, ...]) -> int:
        inv = 0
        n = len(seq)
        for i in range(n):
            if seq[i] == 0:
                continue
            for j in range(i + 1, n):
                if seq[j] == 0:
                    continue
                if seq[i] > seq[j]:
                    inv += 1
        return inv

    width = int(len(state.tiles) ** 0.5)

    inv_start = inversions(state.tiles)
    inv_goal = inversions(goal_state.tiles)

    if width % 2 == 1:
        return (inv_start % 2) == (inv_goal % 2)

    blank_idx = state.tiles.index(0)
    blank_row = blank_idx // width
    blank_row_from_bottom = (width - 1) - blank_row

    blank_goal_idx = goal_state.tiles.index(0)
    blank_goal_row = blank_goal_idx // width
    blank_row_from_bottom_goal = (width - 1) - blank_goal_row

    return (inv_start + blank_row_from_bottom) % 2 == (
        inv_goal + blank_row_from_bottom_goal
    ) % 2
