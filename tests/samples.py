from random import randint, random

import PIL

from ibench.definitions import RGB, Size, Offset, BlockRGB, BlocksRGB, PlaneYCbCr
from ibench.layout import Composition, Part


def _rand_rgb():
    return RGB(randint(0, 255), randint(0, 255), randint(0, 255))


def _rand_y():
    return random()


def _rand_cb_cr():
    return random() - .5


def _x_of_size(size, get_x):
    return [[get_x() for _ in range(size.cx)] for _ in range(size.cy)]


def _get_random_rgb(size):
    return _x_of_size(size, _rand_rgb)


_4x4_pixels = Size(4, 4, 'pixel')
_3x3_blocks = Size(3, 3, 'block')

random_rgb_block = BlockRGB(_4x4_pixels, _get_random_rgb(_4x4_pixels))

random_rgb_blocks = BlocksRGB(
    _3x3_blocks,
    _x_of_size(_3x3_blocks, lambda: random_rgb_block))

random_ycbcr_plane = PlaneYCbCr(
    _4x4_pixels,
    y=_x_of_size(_4x4_pixels, _rand_y),
    cb=_x_of_size(_4x4_pixels, _rand_cb_cr),
    cr=_x_of_size(_4x4_pixels, _rand_cb_cr))


def _get_image():
    return PIL.Image.new('RGB', (5, 5))


composition_of_two_parts = Composition(
    Size(10, 10, 'pixel'),
    [
        Part(Size(5, 5, 'pixel'), Offset(3, 3), _get_image),
        Part(Size(5, 5, 'pixel'), Offset(3, 3), _get_image)
    ])


class RandomSource(object):
    def __init__(self, size):
        self._size = size
        self.pixels = _get_random_rgb(size)

    def get_size_in_pixels(self):
        return self._size

    def get_rgb_pixels(self, x, y, size):
        rows = []
        for y in range(y, y+size.cy):
            rows.append(self.pixels[y][x:(x+size.cx)])
        return rows
