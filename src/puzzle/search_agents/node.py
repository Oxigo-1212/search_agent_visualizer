from typing import Generic, TypeVar, List, Optional

StateType = TypeVar("StateType")
ActionType = TypeVar("ActionType")


class Node(Generic[StateType, ActionType]):
    def __init__(
        self,
        state: StateType,
        parent: Optional["Node[StateType, ActionType]"] = None,
        action: Optional[ActionType] = None,
        path_cost: float = 0,
        depth: int = 0,
    ):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def expand(self, problem, action_extractor) -> List["Node[StateType, ActionType]"]:
        neighbors = problem.get_neighbors(self.state)
        children = []
        for neighbor in neighbors:
            action = action_extractor(self.state, neighbor)
            child_node = Node(
                state=neighbor,
                parent=self,
                action=action,
                path_cost=self.path_cost + 1,
                depth=self.depth + 1,
            )
            children.append(child_node)
        return children

    def path(self) -> List["Node[StateType, ActionType]"]:
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))

    def solution(self) -> List[ActionType]:
        return [node.action for node in self.path() if node.action is not None]
