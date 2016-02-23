from random import randint, random

from ibench.definitions import RGB, Size, BlockRGB, BlocksRGB, PlaneYCbCr


random_rgb_block = BlockRGB(
    Size(4, 4, 'pixel'),
    [[RGB(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(4)] for _ in range(4)])

random_rgb_blocks = BlocksRGB(
    Size(3, 3, 'block'),
    [[random_rgb_block for _ in range(3)] for _ in range(3)])

random_ycbcr_plane = PlaneYCbCr(
    Size(4, 4, 'pixel'),
    y=[[random() for _ in range(4)] for _ in range(4)],
    cb=[[random() - .5 for _ in range(4)] for _ in range(4)],
    cr=[[random() - .5 for _ in range(4)] for _ in range(4)])
