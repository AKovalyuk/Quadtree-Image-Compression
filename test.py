"""Module with tests"""

import numpy as np
from tree import QuadTree, Quad
from typing import Optional, Tuple

def simple_checker(arr: np.ndarray, x_min: int, x_max: int, y_min: int, y_max: int) -> Optional[Tuple[int, int, int]]:
    if arr[y_min:y_max, x_min:x_max].min((0, 1)) == arr[y_min:y_max, x_min:x_max].max((0, 1)):
        return arr[y_min][x_min]
    return None

def test1():
    arr = np.array([
        [0, 0, 1, 2],
        [0, 0, 3, 4],
        [1, 2, 1, 1],
        [3, 4, 1, 1],
    ])
    tree = QuadTree(4, 4, simple_checker)
    tree.set(arr)
    quads = tree.get_quads()
    assert quads == [
        Quad(0, 2, 0, 2, 0),
        Quad(2, 3, 0, 1, 1),
        Quad(3, 4, 0, 1, 2),
        Quad(2, 3, 1, 2, 3),
        Quad(3, 4, 1, 2, 4),
        Quad(0, 1, 2, 3, 1),
        Quad(1, 2, 2, 3, 2),
        Quad(0, 1, 3, 4, 3),
        Quad(1, 2, 3, 4, 4),
        Quad(2, 4, 2, 4, 1),
    ]

def test2():
    arr = np.array([
        [0, 0],
        [0, 0]
    ])
    tree = QuadTree(2, 2, simple_checker)
    tree.set(arr)
    quads = tree.get_quads()
    assert quads == [
        Quad(0, 2, 0, 2, 0),
    ]

def test3():
    arr = np.array([[1]])
    tree = QuadTree(1, 1, simple_checker)
    tree.set(arr)
    quads = tree.get_quads()
    assert quads == [Quad(0, 1, 0, 1, 1)]
