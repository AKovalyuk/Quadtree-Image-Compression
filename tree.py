from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

@dataclass
class Node:
    data: Any = None
    child0: Any = None
    child1: Any = None
    child2: Any = None
    child3: Any = None

class QuadTree:
    def __init__(self, max_power: int, union_rule: Callable = lambda *args: None):
        if max_power <= 0:
            raise ValueError("Power can't be <= 0")
        self.max_power = max_power
        self.max_size = 2 ** max_power
        self.union_rule = union_rule
        self.root = Node()

    @staticmethod
    def _get(node: Node, x: int, y: int, x_max: int, x_min: int, y_max: int, y_min: int) -> Any:
        while not node.child0 is None:
            size = x_max - x_min
            half = size // 2
            if x < x_min + half:
                x_max -= half
                if y < y_min + half:
                    y_max -= half
                    node = node.child0
                else:
                    y_min += half
                    node = node.child2
            else:
                x_min += half
                if y < y_min + half:
                    y_max -= half
                    node = node.child1
                else:
                    y_min += half
                    node = node.child3
        return node.data
    
    def get(self, x: int, y: int) -> Any:
        # if not (x >= 0 and x < self.max_size and y >= 0 and y < self.max_size):
        #     raise ValueError("x and y must be in [0, max_size)")
        return self.__class__._get(self.root, x, y, self.max_size, 0, self.max_size, 0)
    
    @staticmethod
    def _set(data: Any, node: Node, x: int, y: int, x_max: int, x_min: int, y_max: int, y_min: int, rule: Callable) -> None:
        chain = []
        while x_max - x_min != 1:
            chain.append(node)
            size = x_max - x_min
            half = size // 2
            if node.child0 is None:
                node.child0 = Node()
                node.child1 = Node()
                node.child2 = Node()
                node.child3 = Node()
            if x < x_min + half:
                x_max -= half
                if y < y_min + half:
                    y_max -= half
                    node = node.child0
                else:
                    y_min += half
                    node = node.child2
            else:
                x_min += half
                if y < y_min + half:
                    y_max -= half
                    node = node.child1
                else:
                    y_min += half
                    node = node.child3
        node.child0 = node.child1 = node.child2 = node.child3 = None
        node.data = data
        for nod in reversed(chain):
            union = rule(nod.child0.data, nod.child1.data, nod.child2.data, nod.child3.data)
            if not union is None:
                nod.data = union
                nod.child0 = nod.child1 = nod.child2 = nod.child3 = None
            else:
                return

    def set(self, data: Any, x: int, y: int):
        # if not (x >= 0 and x < self.max_size and y >= 0 and y < self.max_size):
        #     raise ValueError("x and y must be in [0, max_size)")
        self.__class__._set(data, self.root, x, y, self.max_size, 0, self.max_size, 0, self.union_rule)
    
    @staticmethod
    def _subtree_eq(node: Node, lst: Union[list, Node]) -> bool:
        if not isinstance(lst, list):
            return node.child0 is None and node.child1 is None and \
                   node.child2 is None and node.child3 is None and \
                   lst == node.data
        else:
            return node.child0 is not None and node.child1 is not None and \
                   node.child2 is not None and node.child3 is not None and \
                   len(lst) == 4 and \
                   QuadTree._subtree_eq(node.child0, lst[0]) and \
                   QuadTree._subtree_eq(node.child1, lst[1]) and \
                   QuadTree._subtree_eq(node.child2, lst[2]) and \
                   QuadTree._subtree_eq(node.child3, lst[3])

    def __eq__(self, __o: object) -> bool:
        return self.__class__._subtree_eq(self.root, __o)
