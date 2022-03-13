from PIL import Image
import numpy as np
from time import time

def dynamic_avg(array: np.ndarray, radius: int) -> np.ndarray:
    height, width = array.shape[:2]
    radius = max(1, radius)
    # Prefix sum
    prefix = array.cumsum(axis=0).cumsum(axis=1)
    avg = np.zeros(array.shape, dtype=np.int32)
    # Center
    avg[radius + 1:height - radius, radius + 1:width - radius] = \
        (prefix[2 * radius + 1:, 2 * radius + 1:] + \
            prefix[:height - 2 * radius - 1, :width - 2 * radius - 1] - \
                prefix[2 * radius + 1:, :width - 2 * radius - 1] - \
                    prefix[:height - 2 * radius - 1, 2 * radius + 1:]) // (2 * radius + 1) ** 2
    # Corners
    # Top left
    avg[:radius + 1, :radius + 1, :] = prefix[radius + 1][radius + 1] // (radius + 1) ** 2
    # Bottom right
    avg[height - radius:, width - radius:, :] = (prefix[-1][-1] + \
        prefix[-radius - 1][-radius - 1] - prefix[-1][-radius - 1] - prefix[-radius - 1][-1]) // (radius) ** 2
    avg[:radius + 1, width - radius:, :] = (prefix[radius + 1][-1] - \
        prefix[radius + 1][-radius - 1]) // (radius * (radius + 1))
    avg[height - radius:, :radius + 1] = (prefix[-1][radius + 1] - \
        prefix[-radius - 1][radius + 1]) // (radius * (radius + 1))
    # Edges
    # Top
    avg[:radius + 1, radius + 1:-radius] = (prefix[radius, 2 * radius + 1:] - \
        prefix[radius, :-2 * radius - 1]) // ((2 * radius + 1) * (radius + 1))
    # Bottom
    avg[-radius:, radius + 1:-radius] = (prefix[-1, 2 * radius + 1:] - \
        prefix[-1, :-2 * radius - 1] - prefix[-radius - 1, 2 * radius + 1:] + \
            prefix[-radius - 1, :-2 * radius - 1]) // ((2 * radius + 1) * radius)
    # Left
    avg[radius + 1:-radius, :radius + 1] = (prefix[2 * radius + 1:, radius:radius + 1] - \
        prefix[:-2 * radius - 1, radius:radius + 1]) // ((2 * radius + 1) * radius)
    # right
    avg[radius + 1:-radius, -radius:] = (prefix[2 * radius + 1:, -1:] - \
        prefix[:-2 * radius - 1, -1:] + \
            prefix[:-2 * radius - 1, -radius - 1:-radius] -\
                prefix[2 * radius + 1:, -radius - 1:-radius]) // ((2 * radius + 1) * radius)
    return avg

def sumvar(array: np.array, avg_array: np.array):
    diffs = np.abs(array - avg_array)
    return np.sum(diffs, axis=2).cumsum(axis=0).cumsum(axis=1)

def sum_query(prefix_array: np.array, x_min, x_max, y_min, y_max):
    sm = prefix_array[y_max - 1][x_max - 1]
    if 0 < x_min and 0 < y_min:
        return sm + prefix_array[y_min - 1][x_min - 1] - prefix_array[y_min - 1][x_max - 1] - prefix_array[y_max - 1][x_min - 1]
    if y_min > 0:
        return sm - prefix_array[y_min - 1][x_max - 1]
    if x_min > 0:
        return sm - prefix_array[y_max - 1][x_min - 1]
    return sm

class Checker:
    def __init__(self, img: Image, radius: int = 15, delta: int = 100) -> None:
        img_array = np.array(img.convert('RGB'), dtype=np.int32)
        self.cummulitives = img_array.cumsum(axis=0).cumsum(axis=1)
        self.var = sumvar(img_array, dynamic_avg(img_array, radius))
        print(self.var, self.var.shape)
        self.delta = delta
    
    def __call__(self, ignored: np.ndarray, x_min: int, x_max: int, y_min: int, y_max: int):
        delta = sum_query(self.var, x_min, x_max, y_min, y_max) // ((x_max - x_min) ** 2)
        if delta <= self.delta:
            return tuple(
                sum_query(self.cummulitives, x_min, x_max, y_min, y_max) // ((x_max - x_min) ** 2)
            )
        return None

def main():
    img = Image.open(input())
    arr = np.asarray(img.convert('RGB'))
    level = int(input())
    now = time()
    avg = dynamic_avg(arr, level).astype('uint8')
    print(f'Done in {time() - now}')
    Image.fromarray(avg.astype('uint8')).show()

if __name__ == '__main__':
    main()