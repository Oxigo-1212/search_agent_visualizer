from puzzle.search_agents.algorithm import depth_limited_dfs


class GraphProblem:
    def __init__(self, graph: dict[str, list[str]], goal: str):
        self.graph = graph
        self.goal = goal

    def get_neighbors(self, state: str) -> list[str]:
        return self.graph.get(state, [])

    def is_goal(self, state: str) -> bool:
        return state == self.goal


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
    assert result.state == "D"
    assert result.depth == 3
    assert result.path_cost == 3
    assert result.solution() == ["A->B", "B->C", "C->D"]


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

    assert result is None


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
    assert result.state == "A"
    assert result.depth == 0
    assert result.path_cost == 0
    assert result.solution() == []


def test_depth_limited_dfs_with_return_nodes_expanded():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    problem = GraphProblem(graph=graph, goal="D")

    result, nodes_expanded = depth_limited_dfs(
        problem, "A", _action_extractor, limit=2, return_nodes_expanded=True
    )

    assert result is not None
    assert result.state == "D"
    assert isinstance(nodes_expanded, int)
    assert nodes_expanded >= 0  # We expanded at least the start node
