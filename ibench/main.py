from __future__ import print_function
import os

import source
import slice
import visualize
from definitions import Size, Area


def _get_source_from_file():
    path_to_root = os.path.split(os.path.split(__file__)[0])[0]
    path_to_image = os.path.join(path_to_root, "images", "dog.jpg")
    return source.from_file(path_to_image)


if __name__ == "__main__":
    image_source = _get_source_from_file()

    # Pipeline start
    rgb_blocks = slice.source(image_source, Size(16, 16, 'pixel'), Area(25, 8, 20, 20, 'block'))
    rgb_block = rgb_blocks.rows[2][9]
    visualize.it(rgb_blocks).show()
    visualize.it(rgb_block).show()
