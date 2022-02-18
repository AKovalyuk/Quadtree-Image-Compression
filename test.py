from pytest import mark
from tree import QuadTree

def test1():
    tree = QuadTree(union_rule=lambda a, b, c, d: a if a == b == c == d else None,
                    max_power=2)
    data = [
        [1, 1, 1, 2],
        [1, 1, 3, 4],
        [1, 2, 0, 0],
        [3, 4, 0, 0]
    ]
    for i in range(len(data)):
        for j in range(len(data[0])):
            tree.set(data[i][j], j, i)
    assert tree == [1, [1, 2, 3, 4], [1, 2, 3, 4], 0]

def test2():
    tree = QuadTree(union_rule=lambda a, b, c, d: a if a == b == c == d else None,
                    max_power=2)
    data = [
        [1, 1, 1, None],
        [1, 1, 1, None],
        [1, 1, 1, None],
        [None, None, None, None]
    ]
    for i in range(len(data)):
        for j in range(len(data[0])):
            tree.set(data[i][j], j, i)
    assert tree == [1, [1, None, 1, None], [1, 1, None, None], [1, None, None, None]]

def test3():
    tree = QuadTree(union_rule=lambda a, b, c, d: a if a == b == c == d else None,
                    max_power=1)
    data = [
        [1, 1],
        [1, 1]
    ]
    for i in range(len(data)):
        for j in range(len(data[0])):
            tree.set(data[i][j], j, i)
    assert tree == 1
