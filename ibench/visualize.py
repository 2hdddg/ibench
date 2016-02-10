from collections import namedtuple
from PIL import Image
from definitions import Buf_2d_rgb, Buf_2d_buffers_of_2d_rgb, Offset, Size


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


def rgb_2d_to_bytes(data):
    """Converts a two-dimensional array of
    RGB pixels to a one-dimensional bytearray
    """
    size_in_bytes = len(data) * len(data[0]) * 3
    pixels = bytearray(size_in_bytes)

    i = 0
    for row in data:
        for pixel in row:
            pixels[i] = pixel.r
            i = i + 1
            pixels[i] = pixel.g
            i = i + 1
            pixels[i] = pixel.b
            i = i + 1
    return pixels


def rgb_2d_to_image(buf):
    data = buf.data
    height = len(data)
    width = len(data[0])
    pixels = rgb_2d_to_bytes(data)
    image = Image.frombytes('RGB', (width, height), buffer(pixels))

    return image


def compose_image(composition):
    image_size = (composition.size.cx, composition.size.cy)
    image = Image.new('RGB', image_size)

    for part in composition.parts:
        part_image = part.get_image()
        part_box = (part.offset.x, part.offset.y)
        image.paste(part_image, part_box)

    return image


def buffer_of_rgb_2d_to_image(buf):
    padding_y = 5
    padding_x = 5
    cy = padding_y
    cx = padding_x

    # Collect and position parts
    parts = []
    for row in buf.data:
        row_cy = 0
        x = padding_x
        for buf in row:
            size = buf.size
            offset = Offset(x, cy)
            x = x + size.cx + padding_x

            get_image = LazyRenderer(
                state=buf, fn=rgb_2d_to_image)

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
    Buf_2d_rgb: rgb_2d_to_image,
    Buf_2d_buffers_of_2d_rgb: buffer_of_rgb_2d_to_image
}


def get_visualizer(buff, get_custom_visualizer=None):
    visualizer = get_custom_visualizer(buff) if get_custom_visualizer else None
    if not visualizer:
        visualizer = _visualizers.get(buff.format)

    return visualizer


def buf(b, get_custom_visualizer=None):
    visualizer = get_visualizer(b, get_custom_visualizer)
    if not visualizer:
        raise Exception("Visualizer for buf: '%s' not found." % b)

    return visualizer(b)
