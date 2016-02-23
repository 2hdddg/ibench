from PIL import Image
from definitions import Size, BlockRGB, BlocksRGB, PlaneYCbCr
from layout import LazyRenderer, fixed_grid, compose_image
from colorspace import y_to_rgb, cb_to_rgb, cr_to_rgb


def _rgb_block_to_bytes(block):
    """Converts a two-dimensional array of
    RGB pixels to a one-dimensional bytearray
    """
    pixels = bytearray()

    for row in block.rows:
        for pixel in row:
            pixels.extend(pixel)
    return pixels


def rgb_block_to_image(block):
    pixels = _rgb_block_to_bytes(block)
    image = Image.frombytes(
        'RGB', (block.size.cx, block.size.cy), buffer(pixels))

    return image


def rgb_blocks_to_image(blocks):
    def get_cell_renderer(row, col):
        block = blocks.rows[row][col]
        return LazyRenderer(state=block, fn=rgb_block_to_image)

    padding = Size(5, 5, 'pixel')
    cell_size = blocks.rows[0][0].size
    grid_composition = fixed_grid(
        blocks.size, padding, cell_size, get_cell_renderer)

    image = compose_image(grid_composition)

    return image


def _build_x_to_image(size, rows, x_to_rgb):

    def x_to_image():
        pixels = bytearray()
        for row in rows:
            for x in row:
                rgb = x_to_rgb(x)
                pixels.extend(rgb)

        image = Image.frombytes(
            'RGB', (size.cx, size.cy), buffer(pixels))

        return image

    return x_to_image


def ycbcr_plane_to_image(plane):
    renderers = [
        _build_x_to_image(plane.size, plane.y, y_to_rgb),
        _build_x_to_image(plane.size, plane.cb, cb_to_rgb),
        _build_x_to_image(plane.size, plane.cr, cr_to_rgb)
    ]

    def get_cell_renderer(row, col):
        return renderers[col]

    padding = Size(10, 10, 'pixel')
    grid_size = Size(3, 1, 'pixel')
    composition = fixed_grid(
        grid_size, padding, plane.size, get_cell_renderer)

    return compose_image(composition)


_visualizers = {
    BlockRGB.__name__: rgb_block_to_image,
    BlocksRGB.__name__: rgb_blocks_to_image,
    PlaneYCbCr.__name__: ycbcr_plane_to_image
}


def _get_visualizer(buf):
    return _visualizers.get(buf.__class__.__name__)


def it(buf, get_custom_visualizer=None):
    visualizer = get_custom_visualizer(buf) if get_custom_visualizer else _get_visualizer(buf)
    if not visualizer:
        raise Exception("Visualizer for: '%s' not found." % str(buf.__class__))

    return visualizer(buf)
