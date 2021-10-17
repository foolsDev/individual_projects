from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional, Protocol

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self)-> None:
        self._container: List[T] = []

    @property
    def empty(self)-> bool:
        return not self._container
    def push(self, item: T)-> None:
        return self._container.append(item)
    def pop(self)-> T:
        return self._container.pop()
    def __repr__(self)-> str:
        return repr(self._container)

class Node(Generic[T]):
    def __init__(self, state: T, parent : Optional[Node], cost: float = 0.0, heuristic: float = 0.0)-> None:
        self.state: T = state
        self.parent:Optional[Node] = parent
        self.cost: float = cost
        self.heurictic: float = heuristic

    def __lt__(self, other: Node)-> bool:
        return (self.cost + self.heurictic) < (other.cost + other.heurictic)

class Compartable(Protocol):
    def __gt__(self, other: Any)-> bool:
        return (not self < other) and self != other
    def __le__(self, other: Any)-> bool:
        return self < other or self == other
    def __ge__(self, other: Any)-> bool:
        return not self < other

def linear_contains(iterable: Iterable[T], key: T)-> bool:
    for item in iterable:
        if item == key:
            return True

C = TypeVar("C", bound="Compartable")

def binary_contains(sequence: Sequence[C], key: C)-> bool:
    low:int = 0
    high:int = len(sequence) - 1
    while low <= high:
        mid:int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False

def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]])->Optional[Node[T]]:
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node[child, current_node])
    return None

def node_to_path(node: Node[T])->List[T]:
    path: List[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


if __name__ == '__main__':
    print(linear_contains([1,3,2,5,64,233,4,6,8], 5))
    print(binary_contains(['a','b','c','d','e''f'], 'c'))
    print(binary_contains([1,4,7,12,24,55,100], 20))