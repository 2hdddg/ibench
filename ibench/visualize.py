from PIL import Image
from definitions import Size, BlockRGB, BlocksRGB, PlaneYCbCr
from layout import fixed_grid, compose_image
from colorspace import y_to_rgb, cb_to_rgb, cr_to_rgb


def _build_x_to_image(size, rows, x_to_rgb):
    """ Returns a function that can build an
    image using x_to_rgb conversion function.
    Returned function is bound to params and
    needs no params itself.
    """
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


def rgb_block_to_image(block):
    return _build_x_to_image(
        block.size, block.rows, lambda x: x)()


def rgb_blocks_to_image(blocks):
    def get_cell_renderer(row, col):
        block = blocks.rows[row][col]
        return _build_x_to_image(
                block.size, block.rows, lambda x: x)

    padding = Size(5, 5, 'pixel')
    cell_size = blocks.rows[0][0].size
    grid_composition = fixed_grid(
        blocks.size, padding, cell_size, get_cell_renderer)

    image = compose_image(grid_composition)

    return image


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
