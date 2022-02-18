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
        # При достижении листовой вершины (без потомков) - возвращаем ее данные
        if node.child0 is None or node.child1 is None or node.child2 is None or node.child3 is None:
            return node.data
        # Размер текущего квадранта
        size = x_max - x_min
        # Половина размера (для удобства вычислений)
        half = size // 2
        # Рекурсивный поиск и вычисление по координатам
        if x < x_min + half and y < y_min + half:
            # x и y в левом верхнем квадранте
            return QuadTree._get(node.child0, x, y, x_max - half, x_min, y_max - half, y_min)
        elif x >= x_min + half and y < y_min + half:
            # x и y в правом верхнем квадранте
            return QuadTree._get(node.child1, x, y, x_max, x_min + half, y_max - half, y_min)
        elif x < x_min + half and y >= y_min + half:
            # x и y в левом нижнем квадранте
            return QuadTree._get(node.child2, x, y, x_max - half, x_min, y_max, y_min + half)
        else:
            # x и y в правом нижнем квадранте
            return QuadTree._get(node.child3, x, y, x_max, x_min + half, y_max, y_min + half)
    
    def get(self, x: int, y: int) -> Any:
        if not (x >= 0 and x < self.max_size and y >= 0 and y < self.max_size):
            raise ValueError("x and y must be in [0, max_size)")
        return self.__class__._get(self.root, x, y, self.max_size, 0, self.max_size, 0)
    
    @staticmethod
    def _set(data: Any, node: Node, x: int, y: int, x_max: int, x_min: int, y_max: int, y_min: int, rule: Callable) -> None:
        # При достижении квадранта размером 1 - установка данных
        if x_max - x_min == 1:
            # Установка потомков в None
            node.child0 = node.child1 = node.child2 = node.child3 = None
            # Установка данных
            node.data = data
            return
        # Если встречено еще не разделенное поддерево
        if node.child0 is None:
            # Добавление пустых узлов-потомков
            node.child0 = Node()
            node.child1 = Node()
            node.child2 = Node()
            node.child3 = Node()
        # Размер текущего квадранта
        size = x_max - x_min
        half = size // 2
        # Рекурсивный поиск в потомках
        if x < x_min + half and y < y_min + half:
            QuadTree._set(data, node.child0, x, y, x_max - half, x_min, y_max - half, y_min, rule)
        elif x >= x_min + half and y < y_min + half:
            QuadTree._set(data, node.child1, x, y, x_max, x_min + half, y_max - half, y_min, rule)
        elif x < x_min + half and y >= y_min + half:
            QuadTree._set(data, node.child2, x, y, x_max - half, x_min, y_max, y_min + half, rule)
        else:
            QuadTree._set(data, node.child3, x, y, x_max, x_min + half, y_max, y_min + half, rule)
        # Попытка объединить данные в квадрантах-потомках
        union = rule(node.child0.data, node.child1.data, node.child2.data, node.child3.data)
        if not union is None:
            # Установить в узел объединенные данные
            node.data = union
            # Очистить потомков
            node.child0 = node.child1 = node.child2 = node.child3 = None

    def set(self, data: Any, x: int, y: int):
        if not (x >= 0 and x < self.max_size and y >= 0 and y < self.max_size):
            raise ValueError("x and y must be in [0, max_size)")
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
