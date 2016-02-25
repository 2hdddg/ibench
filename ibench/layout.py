from collections import namedtuple
from PIL import Image

from definitions import Offset, Size

Part = namedtuple('Part', ['size', 'offset', 'get_image'])
Composition = namedtuple('Composition', ['size', 'parts'])


def compose_image(composition):
    image_size = (composition.size.cx, composition.size.cy)
    image = Image.new('RGB', image_size)

    for part in composition.parts:
        part_image = part.get_image()
        part_box = (part.offset.x, part.offset.y)
        image.paste(part_image, part_box)

    return image


def fixed_grid(grid_size, padding_size, cell_size, get_renderer):
    parts = []
    y = padding_size.cy
    for row in xrange(grid_size.cy):
        x = padding_size.cx
        for col in xrange(grid_size.cx):
            renderer = get_renderer(row, col)
            part = Part(cell_size, Offset(x, y), renderer)
            parts.append(part)
            x = x + cell_size.cx + padding_size.cx
        y = y + cell_size.cy + padding_size.cy

    image_size = Size(
        grid_size.cx * (cell_size.cx + padding_size.cx),
        grid_size.cy * (cell_size.cy + padding_size.cy),
        'pixel')
    composition = Composition(image_size, parts)

    return composition
