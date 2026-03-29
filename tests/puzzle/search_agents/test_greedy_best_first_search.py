from puzzle.search_agents.algorithm import greedy_best_first_search


class GraphProblem:
    def __init__(self, graph: dict[str, list[str]], goal: str):
        self.graph = graph
        self.goal = goal

    def get_neighbors(self, state: str) -> list[str]:
        return self.graph.get(state, [])

    def is_goal(self, state: str) -> bool:
        return state == self.goal

    def get_goal(self, state: str) -> str:
        return self.goal

    def step_cost(self, from_state, to_state, action):
        return 1


def _action_extractor(src: str, dst: str) -> str:
    return f"{src}->{dst}"


def _heuristic_example(state: str, goal: str) -> int:
    # Simple heuristic: 0 if at goal, 1 otherwise
    return 0 if state == goal else 1


def test_greedy_best_first_search_finds_solution():
    # Shortest path from A to G is A -> C -> G (2 moves)
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
    }
    problem = GraphProblem(graph=graph, goal="G")

    result = greedy_best_first_search(
        problem, "A", "G", _action_extractor, _heuristic_example
    )

    assert result is not None
    # Unpack if it's a tuple (when return_nodes_expanded=True)
    if isinstance(result, tuple):
        node, _ = result
        assert node is not None, "Expected a node but got None in tuple"
    else:
        node = result

    assert node.state == "G"
    assert node.depth == 2
    assert node.path_cost == 2
    assert node.solution() == ["A->C", "C->G"]


def test_greedy_best_first_search_returns_none_when_goal_unreachable():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    problem = GraphProblem(graph=graph, goal="Z")

    result = greedy_best_first_search(
        problem, "A", "Z", _action_extractor, _heuristic_example
    )

    assert result is None


def test_greedy_best_first_search_with_nodes_expanded():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
    }
    problem = GraphProblem(graph=graph, goal="G")

    result = greedy_best_first_search(
        problem,
        "A",
        "G",
        _action_extractor,
        _heuristic_example,
        return_nodes_expanded=True,
    )

    assert result is not None
    assert isinstance(result, tuple)
    node, nodes_expanded = result
    assert node is not None
    assert node.state == "G"
    assert nodes_expanded >= 0  # Should have expanded some nodes
