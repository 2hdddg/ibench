from PIL import Image
from definitions import Size
from layout import fixed_grid, compose_image
from colorspace import y_to_rgb, cb_to_rgb, cr_to_rgb


def _zoom_size(size, zoom):
    return Size(
        size.cx * zoom , size.cy * zoom, size.unit)

def _build_x_to_image(size, rows, x_to_rgb, zoom):
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

    def zoom_x_to_image():
        output = []
        pixels = bytearray()
        zoomed_size = _zoom_size(size, zoom)

        for row in rows:
            for x in row:
                rgb = x_to_rgb(x)
                output.extend(rgb * zoom)

            pixels.extend(output * zoom)
            output = []

        image = Image.frombytes(
            'RGB', (zoomed_size.cx, zoomed_size.cy), buffer(pixels))

        return image

    if zoom == 1:
        return x_to_image

    if zoom > 1:
        return zoom_x_to_image

    raise("Unknown options")


def rgb_block_to_image(block, zoom=1):
    return _build_x_to_image(
        block.size, block.rows, lambda x: x, zoom)()


def rgb_blocks_to_image(blocks):
    def get_cell_renderer(row, col):
        block = blocks.rows[row][col]
        return _build_x_to_image(
                block.size, block.rows, lambda x: x, zoom=1)

    padding = Size(5, 5, 'pixel')
    cell_size = blocks.rows[0][0].size
    grid_composition = fixed_grid(
        blocks.size, padding, cell_size, get_cell_renderer)

    image = compose_image(grid_composition)

    return image


def ycbcr_plane_to_image(plane, zoom=1):
    renderers = [
        _build_x_to_image(plane.size, plane.y, y_to_rgb, zoom),
        _build_x_to_image(plane.size, plane.cb, cb_to_rgb, zoom),
        _build_x_to_image(plane.size, plane.cr, cr_to_rgb, zoom)
    ]

    def get_cell_renderer(row, col):
        return renderers[col]

    padding = Size(10, 10, 'pixel')
    grid_size = Size(3, 1, 'pixel')
    cell_size = _zoom_size(plane.size, zoom)
    composition = fixed_grid(
        grid_size, padding, cell_size, get_cell_renderer)

    return compose_image(composition)
