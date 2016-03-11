from __future__ import print_function
import os

from definitions import Size, Area
import source
import slice
import visualize
import colorspace
import subsample


def _get_source_from_file():
    path_to_root = os.path.split(os.path.split(__file__)[0])[0]
    path_to_image = os.path.join(path_to_root, "images", "dog.jpg")
    return source.from_file(path_to_image)


if __name__ == "__main__":
    image_source = _get_source_from_file()

    # Pipeline start
    rgb_blocks = slice.source(image_source, Size(16, 16, 'pixel'), Area(25, 8, 20, 20, 'block'))
    rgb_block = rgb_blocks.rows[2][9]
    ycbcr_plane = colorspace.blockRgb_to_planeYCbCr(rgb_block)
    ycbcr_plane_420 = subsample.planeYCbCr_to_planeYCbCr420(ycbcr_plane)
    visualize.ycbcr_420_plane_to_image(ycbcr_plane_420, zoom=9).show()
    #visualize.ycbcr_plane_to_image(ycbcr_plane, zoom=9).show()
