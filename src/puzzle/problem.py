from __future__ import annotations

from itertools import batched
from typing import List
from .state import PuzzleState


class PuzzleProblem:
    def __init__(self,
                 initial_state: PuzzleState,
                 goal_state: PuzzleState) -> None:
        self.initial_state = initial_state
        self.goal_state = goal_state

    def is_goal(self, state: PuzzleState) -> bool:
        return state == self.goal_state

    def get_neighbors(self, state: PuzzleState) -> List[PuzzleState]:
        grid = [list(chunk) for chunk in batched(state.tiles, 3)]
        empty_r, empty_c = next(
            ((r, c) for r in range(3)
             for c in range(3) if grid[r][c] == 0), (-1, -1)
        )
        neighbors: List[PuzzleState] = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = empty_r + dr, empty_c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_grid = [row[:]
                            for row in grid]  # Make a clone of the 2D grid
                new_grid[empty_r][empty_c], new_grid[nr][nc] = (
                    new_grid[nr][nc],
                    new_grid[empty_r][empty_c],
                )  # swap operation
                new_tiles = tuple(cell for row in new_grid for cell in row)
                neighbors.append(PuzzleState(new_tiles))
        return neighbors
