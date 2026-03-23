from __future__ import annotations

from collections import deque
from typing import Callable, List, Optional, Protocol, TypeVar, runtime_checkable

from .node import Node

StateType = TypeVar("StateType")
ActionType = TypeVar("ActionType")


@runtime_checkable
class ProblemProtocol(Protocol[StateType, ActionType]):
    def get_neighbors(self, state: StateType) -> List[StateType]: ...
    def is_goal(self, state: StateType) -> bool: ...


def bfs(
    problem: ProblemProtocol[StateType, ActionType],
    initial_state: StateType,
    action_extractor: Callable[[StateType, StateType], ActionType],
    return_nodes_expanded: bool = False,
) -> (
    Optional[Node[StateType, ActionType]]
    | tuple[Optional[Node[StateType, ActionType]], int]
):
    start_node = Node(state=initial_state, path_cost=0, depth=0)
    if problem.is_goal(initial_state):
        return (start_node, 0) if return_nodes_expanded else start_node

    queue = deque([start_node])
    visited = {initial_state}
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        for neighbor in problem.get_neighbors(current.state):
            if neighbor not in visited:
                child = Node(
                    state=neighbor,
                    parent=current,
                    action=action_extractor(current.state, neighbor),
                    path_cost=current.path_cost + 1,
                    depth=current.depth + 1,
                )
                if problem.is_goal(neighbor):
                    return (child, nodes_expanded) if return_nodes_expanded else child
                visited.add(neighbor)
                queue.append(child)

    return (None, nodes_expanded) if return_nodes_expanded else None


def dfs(
    problem: ProblemProtocol[StateType, ActionType],
    initial_state: StateType,
    action_extractor: Callable[[StateType, StateType], ActionType],
    return_nodes_expanded: bool = False,
) -> (
    Optional[Node[StateType, ActionType]]
    | tuple[Optional[Node[StateType, ActionType]], int]
):
    start_node = Node(state=initial_state, path_cost=0, depth=0)
    if problem.is_goal(initial_state):
        return (start_node, 0) if return_nodes_expanded else start_node
    stack = deque([start_node])
    visited = {initial_state}
    nodes_expanded = 0

    while stack:
        current_state = stack.pop()
        nodes_expanded += 1

        for neighbor in problem.get_neighbors(current_state.state):
            if neighbor not in visited:
                child = Node(
                    state=neighbor,
                    parent=current_state,
                    action=action_extractor(current_state.state, neighbor),
                    path_cost=current_state.path_cost + 1,
                    depth=current_state.depth + 1,
                )
                if problem.is_goal(neighbor):
                    return (child, nodes_expanded) if return_nodes_expanded else child
                visited.add(neighbor)
                stack.append(child)
    return (None, nodes_expanded) if return_nodes_expanded else None


def depth_limited_dfs(
    problem: ProblemProtocol[StateType, ActionType],
    initial_state: StateType,
    action_extractor: Callable[[StateType, StateType], ActionType],
    limit: int,
    return_nodes_expanded: bool = False,
) -> (
    Optional[Node[StateType, ActionType]]
    | tuple[Optional[Node[StateType, ActionType]], int]
):
    start_node = Node(state=initial_state, path_cost=0, depth=0)
    if problem.is_goal(initial_state):
        return (start_node, 0) if return_nodes_expanded else start_node
    stack = deque([start_node])
    visited = {initial_state}
    nodes_expanded = 0
    while stack:
        current_state = stack.pop()
        nodes_expanded += 1
        if current_state.depth >= limit:
            continue
        for neighbor in problem.get_neighbors(current_state.state):
            if neighbor not in visited:
                child = Node(
                    state=neighbor,
                    parent=current_state,
                    action=action_extractor(current_state.state, neighbor),
                    path_cost=current_state.path_cost + 1,
                    depth=current_state.depth + 1,
                )
                if problem.is_goal(neighbor):
                    return (child, nodes_expanded) if return_nodes_expanded else child
                visited.add(neighbor)
                stack.append(child)
    return (None, nodes_expanded) if return_nodes_expanded else None
