from __future__ import annotations
import heapq
from collections import deque
from typing import Callable, List, Optional, Protocol, TypeVar, runtime_checkable

from .node import Node

StateType = TypeVar("StateType")
ActionType = TypeVar("ActionType")


@runtime_checkable
class ProblemProtocol(Protocol[StateType, ActionType]):
    def get_neighbors(self, state: StateType) -> List[StateType]: ...
    def is_goal(self, state: StateType) -> bool: ...
    def get_goal(self, state: StateType) -> StateType: ...
    def step_cost(self, from_state: StateType,
                  to_state: StateType, action: ActionType) -> int: ...


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
                    path_cost=current.path_cost +
                    problem.step_cost(current.state, neighbor,
                                      action_extractor(current.state, neighbor)),
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
                    path_cost=current_state.path_cost +
                    problem.step_cost(current_state.state, neighbor,
                                      action_extractor(current_state.state, neighbor)),
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
                    path_cost=current_state.path_cost + problem.step_cost(
                        current_state.state, neighbor, action_extractor(current_state.state, neighbor)),
                    depth=current_state.depth + 1,
                )
                if problem.is_goal(neighbor):
                    return (child, nodes_expanded) if return_nodes_expanded else child
                visited.add(neighbor)
                stack.append(child)
    return (None, nodes_expanded) if return_nodes_expanded else None


def greedy_best_first_search(
    problem: ProblemProtocol[StateType, ActionType],
    initial_state: StateType,
    goal_state: StateType,
    action_extractor: Callable[[StateType, StateType], ActionType],
    heuristic: Callable[[StateType, StateType], int],
    return_nodes_expanded: bool = False,
) -> (
    Optional[Node[StateType, ActionType]]
    | tuple[Optional[Node[StateType, ActionType]], int]
):
    start_node = Node(state=initial_state, path_cost=0, depth=0)
    nodes_expanded = 0
    if problem.is_goal(initial_state):
        return (start_node, 0) if return_nodes_expanded else start_node
    frontier = []
    visited = {initial_state}
    heapq.heappush(frontier, (heuristic(
        initial_state, goal_state), start_node))
    while frontier:
        current_node = heapq.heappop(frontier)
        nodes_expanded += 1
        if problem.is_goal(current_node.state):
            return (current_node, nodes_expanded) if return_nodes_expanded else current_node
        for neighbor in problem.get_neighbors(current_node.state):
            if neighbor not in visited:
                visited.add(neighbor)
                child = Node(
                    state=neighbor,
                    parent=current_node,
                    action=action_extractor(current_node.state, neighbor),
                    path_cost=current_node.path_cost + problem.step_cost(
                        current_node.state, neighbor, action_extractor*(current_node.state, neighbor)),
                    depth=current_node.depth + 1,
                )
                heapq.heappush(
                    frontier, (heuristic(neighbor, goal_state), child))
    return (None, nodes_expanded) if return_nodes_expanded else None
