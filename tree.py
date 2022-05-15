"""QuadTree module"""

from dataclasses import dataclass
from typing import Any, Callable, List, Union, Tuple
from math import log2, ceil
from threading import Thread


@dataclass
class Node:
    """QuadTree node"""
    # Quad (data on leaf nodes)
    quad: Union['Quad', None] = None
    # Child nodes
    children: Union[Tuple['Quad'], None] = None

@dataclass
class Quad:
    """Quad for data in leaf nodes"""
    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    data: Any = None

def quads(x_min, x_max, y_min, y_max, half):
    return [
        (x_min, x_max - half, y_min, y_max - half),
        (x_min + half, x_max, y_min, y_max - half),
        (x_min, x_max - half, y_min + half, y_max),
        (x_min + half, x_max, y_min + half, y_max),
    ]

class QuadTree:
    """QuadTree for compressing array like objects (images)"""
    def __init__(self, width: int, height: int,
    checker: Callable[[List[List[Any]], int, int, int, int], Any] = lambda *args: None, multitrhead: bool = False):
        """
        QuadTree constructor

        :param int width: image width
        :param int height: image height
        :param int max_threads: max threads count
        :param function checker: compression functions, returns none, if it can't union
        """
        self.width = width
        self.height = height
        self.checker = checker
        self.max_power = ceil(log2(max(width, height)))
        self.multitrhead = multitrhead
        self.max_size = 2 ** self.max_power
        self.root = Node()

    def set(self, data: List[List[Any]]) -> None:
        """
        Set method compresses data and saves in tree

        :raises ValueError: uncorrect size of data or len(data[i]) != len(data[j]) for some i, j
        """
        # Check bounds
        if len(data) != self.height:
            raise ValueError('Uncorrect size')
        for line in data:
            if len(line) != self.width:
                raise ValueError('Uncorrect size')
        # Recursion set call
        self.__set(self.root, data, 0, self.max_size, 0, self.max_size)

    def __set(self, node: Node, data: List[List[Any]], x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        """
        Recursive function to set data submatrix in node

        :param Node node: current node
        :param data: data matrix (image)
        :param
        """
        # Quad out of bounds
        if x_min >= self.width and y_min >= self.height:
            node.quad = Quad(x_min, x_max, y_min, y_max, None)
        # Quad partialy out of bounds or section has more details - needs to subdivide
        check_result = None
        if (x_max > self.width or y_max > self.height or
        (check_result := self.checker(data, x_min, x_max, y_min, y_max)) is None) and x_max - x_min > 1:
            # If children is none - create empty child nodes
            if node.children is None:
                node.children = (Node(), Node(), Node(), Node())
            half = (x_max - x_min) // 2
            quads_ = quads(x_min, x_max, y_min, y_max, half)
            if self.multitrhead and self.max_size == x_max - x_min:
                threads = []
                for i in range(4):
                    threads.append(Thread(target=self.__set, args=(
                        node.children[i], data, *quads_[i]
                    )))
                for i in range(4):
                    threads[i].start()
                for i in range(4):
                    threads[i].join()
            # Recursive subdivide image
            else:
                for i in range(4):
                    self.__set(node.children[i], data, *quads_[i])
        else:
            # if compression can be performed - make this node a leaf
            node.quad = Quad(x_min, x_max, y_min, y_max, check_result)

    def get(self, x: int, y: int) -> Any:
        """
        Get method - gets data on (x, y) coordinates

        :param int x: x coordinate
        :param int y: y coordinate
        :raises ValueError: x or y out of bounds
        :rtype: Any
        :return: data on this coordinates
        """
        if x >= self.width or y >= self.height:
            raise ValueError('point out of width or height')
        # Recursive get
        return self.__get(self.root, x, y, 0, self.max_size, 0, self.max_size)

    def __get(self, node: Node, x :int, y :int, x_min :int, x_max :int, y_min :int, y_max :int) -> Any:
        # Check (is leaf?)
        if not node.quad is None:
            return node.quad.data
        half = (x_max - x_min) // 2
        quads_ = quads(x_min, x_max, y_min, y_max, half)
        # Check branch
        if x < x_min + half:
            if y < y_min + half:
                return self.__get(node.children[0], x, y, *quads[0])
            else:
                return self.__get(node.children[2], x, y, *quads[1])
        else:
            if y < y_min + half:
                return self.__get(node.children[1], x, y, *quads[2])
            else:
                return self.__get(node.children[3], x, y, *quads[3])

    def get_quads(self) -> List[Quad]:
        """
        Get all quads of tree
        Order: DFS child0 (top left), child1 (top right) child2 (bottom left) child3 (bottom right)

        :return: list of quads
        :rtype: list
        """
        container = []
        # Recursive get
        self.__get_quads(self.root, container)
        return container

    def __get_quads(self, node: Node, container: List[Node]) -> None:
        """Recursive get function"""
        if not node.quad is None:
            container.append(node.quad)
        else:
            for i in range(4):
                self.__get_quads(node.children[i], container)
