from __future__ import print_function
import os

import source
import slice
import visualize
from definitions import Size


def _get_source_from_file():
    path_to_root = os.path.split(os.path.split(__file__)[0])[0]
    path_to_image = os.path.join(path_to_root, "images", "dog.jpg")
    return source.from_file(path_to_image)


if __name__ == "__main__":
    image_source = _get_source_from_file()

    # Pipeline start
    sliced = slice.source(image_source, Size(16, 16, 'pixel'))
    image = visualize.buf(sliced)
    image.show()

