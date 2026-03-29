# src/puzzle/

## Responsibility

Implements the core 8-puzzle domain model, solvability utilities, and the Tkinter-based user interface for configuring states and running search algorithms.

## Design Patterns

Immutable value object (`PuzzleState`) for board state, a simple problem/domain object (`PuzzleProblem`) for successor generation and goal checks, and a GUI controller/view class (`PuzzleGUI`) that orchestrates user input, algorithm selection, and animation. The search algorithms are injected via function imports, making the UI a thin dispatcher over interchangeable strategies.

## Data & Control Flow

User edits or shuffles `PuzzleState` instances in `gui.py`; `PuzzleProblem.get_neighbors()` produces successor states for shuffling and search; `utils.is_solvable()` gates solving before execution. When Solve is pressed, the GUI builds a `PuzzleProblem`, selects BFS/DFS/depth-limited DFS, passes `action_extractor`, measures time/memory, then animates the returned path back into the board widgets.

## Integration Points

Depends on `puzzle.search_agents.algorithm` for search routines, and on sibling modules `state.py`, `problem.py`, and `utils.py` for the domain model and helper functions. It is the package entry point via `__init__.py` exporting `GUIloop`, and is meant to be launched directly as a script or imported by higher-level application code.
