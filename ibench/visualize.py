from collections import namedtuple
from PIL import Image
from definitions import Offset, Size, BlockRGB, BlocksRGB


Composition = namedtuple('Composition', ['size', 'parts'])
Part = namedtuple('Part', ['size', 'offset', 'get_image'])


class LazyRenderer(object):
    """A keeper of state and
    the actual to make in the future
    to render an image.
    Just to reduce amount of memory
    used simultanously
    """
    def __init__(self, state, fn):
        self._state = state
        self._fn = fn

    def __call__(self):
        return self._fn(self._state)


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


def compose_image(composition):
    image_size = (composition.size.cx, composition.size.cy)
    image = Image.new('RGB', image_size)

    for part in composition.parts:
        part_image = part.get_image()
        part_box = (part.offset.x, part.offset.y)
        image.paste(part_image, part_box)

    return image


def rgb_blocks_to_image(blocks):
    padding_y = 5
    padding_x = 5
    cy = padding_y
    cx = padding_x
    rows = blocks.rows

    # Collect and position parts
    parts = []
    for row in rows:
        row_cy = 0
        x = padding_x
        for block in row:
            size = block.size
            offset = Offset(x, cy)
            x = x + size.cx + padding_x

            get_image = LazyRenderer(
                state=block, fn=rgb_block_to_image)

            part = Part(size, offset, get_image)
            parts.append(part)
            # Calculate max height in row
            row_cy = max([row_cy, size.cy])

        cx = max([cx, x])
        cy = cy + row_cy + padding_y

    composition = Composition(Size(cx, cy, 'pixel'), parts)

    image = compose_image(composition)

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
