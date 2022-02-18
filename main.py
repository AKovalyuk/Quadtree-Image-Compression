from math import ceil
from typing import Tuple, Any, Callable
from PIL import Image, ImageDraw
from tree import QuadTree
from math import log2

from time import time

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

def union_rule(*args):
    if None in args:
        return None
    mn, mx = min(args), max(args)
    if mx - mn < 20:
        return (mn + mx) // 2

def main():
    img = Image.open(input())
    draw = ImageDraw.Draw(img)
    x_size, y_size = img.size
    max_power = int(ceil(log2(max(x_size, y_size))))
    print(max_power)
    tree = QuadTree(max_power=max_power, union_rule=pixel_union_rule(max_range=100))
    now = time()
    for x in range(x_size):
        for y in range(y_size):
            tree.set(img.getpixel((x, y)), x, y)
        print(x)
    print(time() - now)
    for x in range(x_size):
        for y in range(y_size):
            draw.point((x, y), tree.get(x, y))
        print(x)
    print(time() - now)
    img.show()



if __name__ == '__main__':
    main()
