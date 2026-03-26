from puzzle.search_agents.algorithm import depth_limited_dfs


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


def test_depth_limited_dfs_finds_solution_within_limit():
    # Graph: A -> B -> C -> D (goal)
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": [],
    }
    problem = GraphProblem(graph=graph, goal="D")

    # With limit 3, we can reach D (A->B->C->D, depth 3)
    result = depth_limited_dfs(problem, "A", _action_extractor, limit=3)

    assert result is not None
    # Unpack if it's a tuple (when return_nodes_expanded=True)
    if isinstance(result, tuple):
        node, _ = result
        assert node is not None, "Expected a node but got None in tuple"
    else:
        node = result

    assert node.state == "D"
    assert node.depth == 3
    assert node.path_cost == 3
    assert node.solution() == ["A->B", "B->C", "C->D"]


def test_depth_limited_dfs_returns_none_when_goal_beyond_limit():
    # Graph: A -> B -> C -> D (goal)
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": [],
    }
    problem = GraphProblem(graph=graph, goal="D")

    # With limit 2, we cannot reach D (requires depth 3)
    result = depth_limited_dfs(problem, "A", _action_extractor, limit=2)

    # The function may return a tuple (node, nodes_expanded) or just node
    if isinstance(result, tuple):
        node, _ = result
    else:
        node = result

    assert node is None


def test_depth_limited_dfs_returns_none_when_goal_unreachable():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    problem = GraphProblem(graph=graph, goal="Z")

    result = depth_limited_dfs(problem, "A", _action_extractor, limit=10)

    assert result is None


def test_depth_limited_dfs_returns_none_when_initial_state_is_goal_and_limit_zero():
    # Edge case: initial state is goal, but limit is 0 -> should return the start node
    graph = {
        "A": ["B"],
        "B": [],
    }
    problem = GraphProblem(graph=graph, goal="A")

    result = depth_limited_dfs(problem, "A", _action_extractor, limit=0)

    assert result is not None
    if isinstance(result, tuple):
        node, _ = result
        assert node is not None, "Expected a node but got None in tuple"
    else:
        node = result

    assert node.state == "A"
    assert node.depth == 0
    assert node.path_cost == 0
    assert node.solution() == []


def test_depth_limited_dfs_with_return_nodes_expanded():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    problem = GraphProblem(graph=graph, goal="D")

    result = depth_limited_dfs(
        problem, "A", _action_extractor, limit=2, return_nodes_expanded=True
    )

    assert result is not None
    # When return_nodes_expanded=True, result is a tuple (node, nodes_expanded)
    assert isinstance(result, tuple)
    node, nodes_expanded = result
    assert node is not None
    assert node.state == "D"
    assert isinstance(nodes_expanded, int)
    assert nodes_expanded >= 0  # We expanded at least the start node
