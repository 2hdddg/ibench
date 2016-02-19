from PIL import Image
from definitions import Size, BlockRGB, BlocksRGB, PlaneYCbCr
from layout import LazyRenderer, fixed_grid, compose_image


def rgb_block_to_bytes(block):
    """Converts a two-dimensional array of
    RGB pixels to a one-dimensional bytearray
    """
    size = block.size
    size_in_bytes = size.cy * size.cx * 3
    pixels = bytearray(size_in_bytes)

    i = 0
    for row in block.rows:
        for pixel in row:
            pixels[i] = pixel.r
            i = i + 1
            pixels[i] = pixel.g
            i = i + 1
            pixels[i] = pixel.b
            i = i + 1
    return pixels


def rgb_block_to_image(block):
    pixels = rgb_block_to_bytes(block)
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


def y_to_image(plane):
    size = plane.size
    size_in_bytes = size.cy * size.cx * 3
    pixels = bytearray(size_in_bytes)

    i = 0
    for row in plane.y:
        for y in row:
            pixels[i] = int(y * 255)
            i = i + 1
            pixels[i] = int(y * 255)
            i = i + 1
            pixels[i] = int(y * 255)
            i = i + 1

    image = Image.frombytes(
        'RGB', (plane.size.cx, plane.size.cy), buffer(pixels))

    return image


def cb_to_image(plane):
    return y_to_image(plane)


def cr_to_image(plane):
    return y_to_image(plane)


def ycbcr_plane_to_image(plane):
    renderers = [
        LazyRenderer(state=plane, fn=y_to_image),
        LazyRenderer(state=plane, fn=cb_to_image),
        LazyRenderer(state=plane, fn=cr_to_image)
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


def get_visualizer(buf, get_custom_visualizer=None):
    visualizer = get_custom_visualizer(buf) if get_custom_visualizer else None
    if not visualizer:
        visualizer = _visualizers.get(buf.__class__.__name__)

    return visualizer


def it(buf, get_custom_visualizer=None):
    visualizer = get_visualizer(buf, get_custom_visualizer)
    if not visualizer:
        raise Exception("Visualizer for: '%s' not found." % str(buf.__class__))

    return visualizer(buf)
