from math import ceil
from typing import Tuple, Any, Callable
from PIL import Image
from tree import QuadTree
from math import log2

def pixel_union_rule(max_range: int) -> Callable:
    def wrapped(*args: Tuple) -> Any:
        if None in args:
            return None
        max_values = [0] * len(args[0])
        min_values = [255] * len(args[0])
        for pixel in args:
            for i in range(len(pixel)):
                max_values[i] = max(max_values[i], pixel[i])
                min_values[i] = min(min_values[i], pixel[i])
        _range = sum([max_values[i] - min_values[i] for i in range(len(max_values))])
        if _range > max_range:
            return None
        return tuple([(max_values[i] + min_values[i]) // 2 for i in range(len(max_values))])
    return wrapped



def main():
    img = Image.open(input())
    x_size, y_size = img.size
    max_power = int(ceil(log2(max(x_size, y_size))))
    print(max_power)
    tree = QuadTree(max_power=max_power, union_rule=pixel_union_rule(max_range=20))
    for x in range(x_size):
        for y in range(y_size):
            tree.set(img.getpixel((x, y)), x, y)
            print(f'set {x}, {y}')
    for x in range(x_size):
        for y in range(y_size):
            img.putpixel((x, y), tree.get(x, y))
            print(f'get {x}, {y}')
    img.show()



if __name__ == '__main__':
    main()
