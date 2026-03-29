# src/

<!-- Explorer: Fill in this section with architectural understanding -->

## Responsibility

<!-- What is this folder's job in the system? -->

## Design

<!-- Key patterns, abstractions, architectural decisions -->

## Flow

<!-- How does data/control flow through this module? -->

## Integration

<!-- How does it connect to other parts of the system? -->
# src/

## Responsibility
Application source root for the 8-puzzle solver. It wires the CLI entry point to the Tkinter GUI and contains the core domain model, puzzle transition logic, search algorithms, and utility helpers used to validate and solve 8-puzzle states.

## Design Patterns
- Model/View-Controller style separation: `PuzzleState` and `PuzzleProblem` model the domain, `PuzzleGUI` renders and handles user interaction, and `algorithm.py` performs search.
- Generic search abstraction via `ProblemProtocol` and generic `Node` to keep BFS/DFS implementations reusable.
- State/value-object pattern in `PuzzleState` using frozen `attrs` for immutable board states.
- Template-like expansion flow: `Node.expand()` delegates neighbor generation to `PuzzleProblem` and action derivation to `action_extractor`.

## Data & Control Flow
1. `main.py` starts the app by calling `GUIloop()`.
2. `puzzle.gui.PuzzleGUI` initializes current/goal `PuzzleState` instances and builds the Tkinter interface.
3. User edits boards or shuffles the initial state; `PuzzleGUI` updates its local state and refreshes the grid widgets.
4. On solve, the GUI checks `is_solvable()`, constructs a `PuzzleProblem`, and dispatches to `bfs`, `dfs`, or `depth_limited_dfs`.
5. Search functions create `Node` chains while expanding states returned by `PuzzleProblem.get_neighbors()`.
6. When a goal is found, the GUI reconstructs the path from the goal node, updates benchmark stats, and animates the solution back through the board.

## Integration Points
- Depends on: `tkinter`, `time`, `tracemalloc`, and `attrs`/standard library utilities.
- Internal consumers:
  - `main.py` consumes `puzzle.gui.GUIloop`.
  - `puzzle/gui.py` consumes `puzzle.state`, `puzzle.problem`, `puzzle.utils`, and `puzzle.search_agents.algorithm`.
  - `puzzle/search_agents/algorithm.py` consumes `puzzle/search_agents/node.py`.
- External interface: package exports `GUIloop` from `puzzle.__init__` for convenient entry-point imports.
- Data dependencies: `PuzzleState` is the shared immutable representation used by GUI, problem definition, validation helpers, and search algorithms.
