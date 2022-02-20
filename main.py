"""Main program"""

from typing import Tuple, Optional
from argparse import ArgumentParser
from time import time
import numpy as np
from PIL import Image, ImageDraw
from tree import QuadTree

class UnionLevel:
    """Level represents union level"""
    level = 0

    @staticmethod
    def set_level(level: int):
        UnionLevel.level = level

    @staticmethod
    def get_level() -> int:
        return UnionLevel.level

class Recorder:
    """Class for recording compression process"""
    recorder = {}
    active = False

    @staticmethod
    def set_active(active):
        Recorder.active = active

    @staticmethod
    def is_active() -> bool:
        return Recorder.active

def checker(arr: np.ndarray, x_min: int, x_max: int, y_min: int, y_max: int) -> Optional[Tuple[int, int, int]]:
    # Get average color
    red, green, blue = arr[y_min:y_max, x_min:x_max].mean((0, 1))
    # Check detalisation
    if Recorder.is_active():
        Recorder.recorder[x_max - x_min] = Recorder.recorder.get(x_max - x_min, []) + \
            [((round(red), round(green), round(blue)), x_min, x_max, y_min, y_max)]
    if max(arr[y_min:y_max, x_min:x_max].max((0, 1)) - arr[y_min:y_max, x_min:x_max].min((0, 1))) < UnionLevel.get_level():
        return round(red), round(green), round(blue)
    return None

def main():
    # CLI arguments handler
    parser = ArgumentParser(description='Image compression')
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', default=None, required=False, help='Output file, if none - shows image in window')
    parser.add_argument('--gif', action='store_true', required=False, help='needs to generate gif?')
    parser.add_argument('--level', required=False, default=16, type=int, help='Compression level')
    parser.add_argument('--multithread', action='store_true', required=False, help='Max thread count')
    args = parser.parse_args()
    UnionLevel.set_level(max(0, args.level))
    Recorder.set_active(args.gif)
    # Image load
    img = Image.open(args.input)
    # Source image, first gif frame
    source = img.copy()
    draw = ImageDraw.Draw(img)
    x_size, y_size = img.size
    now = time()
    # Convert to numpy array
    arr = np.asarray(img.convert('RGB'))
    # Compressing using QuadTree
    tree = QuadTree(x_size, y_size, checker, args.multithread)
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
    if args.gif:
        frames = [source.copy()]
        source_drawer = ImageDraw.Draw(source)
        for key in sorted(Recorder.recorder.keys(), reverse=True):
            for quad in Recorder.recorder[key]:
                source_drawer.rectangle((quad[1], quad[3], quad[2], quad[4]),
                fill=quad[0], outline=(255, 0, 0), width=1)
            frames.append(source.copy())
        frames[0].save('gif.gif', save_all=True, optimize=True,
        append_images=frames[1:], duration=300, loop=True)

if __name__ == '__main__':
    main()
