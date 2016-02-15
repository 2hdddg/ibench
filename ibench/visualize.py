from PIL import Image
from definitions import Size, BlockRGB, BlocksRGB
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


_visualizers = {
    BlockRGB.__name__: rgb_block_to_image,
    BlocksRGB.__name__: rgb_blocks_to_image
}


def get_visualizer(buf, get_custom_visualizer=None):
    visualizer = get_custom_visualizer(buf) if get_custom_visualizer else None
    if not visualizer:
        visualizer = _visualizers.get(buf.__class__.__name__)

    return visualizer


def it(buf, get_custom_visualizer=None):
    visualizer = get_visualizer(buf, get_custom_visualizer)
    if not visualizer:
        raise Exception("Visualizer for buffer: '%s' not found." % buf)

    return visualizer(buf)
