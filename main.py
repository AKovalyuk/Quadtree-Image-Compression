"""Main program"""

from typing import Tuple, Optional
from argparse import ArgumentParser
from time import time
import numpy as np
from PIL import Image, ImageDraw
from tree import QuadTree

def checker(arr: np.ndarray, x_min: int, x_max: int, y_min: int, y_max: int) -> Optional[Tuple[int, int, int]]:
    # Get average color
    red, green, blue = arr[y_min:y_max, x_min:x_max].mean((0, 1))
    size = x_max - x_min
    # Check detalisation
    if max(arr[y_min:y_max, x_min:x_max].max((0, 1)) - arr[y_min:y_max, x_min:x_max].min((0, 1))) < 256 // size:
        return round(red), round(green), round(blue)
    return None

def main():
    # CLI arguments handler
    parser = ArgumentParser(description='Image compression')
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', default=None, required=False, help='Output file, if none - shows image in window')
    parser.add_argument('--gif', action='store_true', required=False, help='needs to generate gif?')
    parser.add_argument('--level', required=False, default=8, type=int, help='Compression level')
    parser.add_argument('--threads', required=False, default=0, type=int, help='Max thread count')
    args = parser.parse_args()
    # Image load
    img = Image.open(args.input)
    draw = ImageDraw.Draw(img)
    x_size, y_size = img.size
    now = time()
    # Convert to numpy array
    arr = np.asarray(img.convert('RGB'))
    # Compressing using QuadTree
    tree = QuadTree(x_size, y_size, checker)
    tree.set(arr)
    # Get all quads
    quads = tree.get_quads()
    # Drawing quads
    for quad in quads:
        draw.rectangle((quad.x_min, quad.y_min, quad.x_max + 1, quad.y_max + 1), quad.data)
    print(f'Done in {time() - now} s\nQuads in tree: {len(quads)}')
    if args.output is None:
        img.show()
    else:
        img.save(args.output)

if __name__ == '__main__':
    main()
