# src/puzzle/search_agents/

<!-- Explorer: Fill in this section with architectural understanding -->

## Responsibility

<!-- What is this folder's job in the system? -->

## Design

<!-- Key patterns, abstractions, architectural decisions -->

## Flow

<!-- How does data/control flow through this module? -->

## Integration

<!-- How does it connect to other parts of the system? -->
# src/puzzle/search_agents/

## Responsibility
This package contains the core search-agent primitives for solving state-space problems in the puzzle domain. It defines a generic search node abstraction plus baseline graph-search algorithms (BFS, DFS, depth-limited DFS) that operate over any problem exposing neighbor generation and goal testing.

## Design Patterns
- **Protocol / Interface-based design**: `ProblemProtocol` lets search code depend on behavior rather than concrete puzzle types.
- **Generic types**: `Node`, `ProblemProtocol`, and the search functions are parameterized over state/action types.
- **Parent-linked tree nodes**: search results are represented as linked nodes so paths and action sequences can be reconstructed.
- **Queue/stack traversal**: BFS uses a queue, DFS and depth-limited DFS use a stack-like deque.

## Data & Control Flow
Search begins with an initial state wrapped in a `Node`. The algorithm repeatedly asks the problem for neighbors, filters out visited states, creates child nodes with parent/action/depth/path-cost metadata, and checks each generated state against the goal. When a goal is found, the terminal `Node` is returned; callers can then recover the full path via `Node.path()` or actions via `Node.solution()`. `return_nodes_expanded` optionally adds a search-effort count to the result.

## Integration Points
This package depends on puzzle/problem implementations elsewhere in the system to provide `get_neighbors()` and `is_goal()`, plus an `action_extractor` callback to translate state transitions into domain actions. It is likely consumed by higher-level solvers, CLI entrypoints, or evaluators that need generic search over puzzle states. The `Node` type is the main output contract shared with downstream code that reconstructs paths or displays solutions.
