from puzzle.search_agents.algorithm import bfs


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


def test_bfs_finds_shortest_solution_path():
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

    result = bfs(problem, "A", _action_extractor)

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


def test_bfs_returns_none_when_goal_unreachable():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    problem = GraphProblem(graph=graph, goal="Z")

    result = bfs(problem, "A", _action_extractor)

    assert result is None
