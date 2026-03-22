from puzzle.search_agents.node import Node


class GraphProblem:
    def __init__(self, graph: dict[str, list[str]]):
        self.graph = graph

    def get_neighbors(self, state: str) -> list[str]:
        return self.graph.get(state, [])


def _action_extractor(src: str, dst: str) -> str:
    return f"{src}->{dst}"


def test_node_expand_sets_parent_depth_cost_and_actions():
    graph = {
        "A": ["B", "C"],
        "B": [],
        "C": [],
    }
    problem = GraphProblem(graph=graph)
    root = Node(state="A", path_cost=3, depth=2)

    children = root.expand(problem, _action_extractor)

    assert [child.state for child in children] == ["B", "C"]
    assert [child.parent for child in children] == [root, root]
    assert [child.action for child in children] == ["A->B", "A->C"]
    assert [child.depth for child in children] == [3, 3]
    assert [child.path_cost for child in children] == [4, 4]
