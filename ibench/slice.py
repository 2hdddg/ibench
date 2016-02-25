from definitions import Size, Area, BlockRGB, BlocksRGB


def _get_size_in_blocks(block_size, size_in_pixels):
    # Full blocks
    cx = size_in_pixels.cx / block_size.cx
    cy = size_in_pixels.cy / block_size.cx

    size_in_blocks = Size(cx=cx, cy=cy, unit='block')

    return size_in_blocks


def source(source, block_size, source_area=None):
    """Splits a source into blocks of RGB
    source - implements: get_size_in_pixels, get_rgb_pixels
    block_size - requested size in pixels of each block
    source_area - optionally split only a part of the source
    """
    source_size = _get_size_in_blocks(
        block_size, source.get_size_in_pixels())
    source_area = source_area if source_area else Area(0, 0, source_size.cx, source_size.cy, 'block')
    block_rows = []

    y = source_area.y * block_size.cy
    for block_y in range(source_area.y, source_area.y + source_area.cy):
        row = []
        x = source_area.x * block_size.cx
        for block_x in range(source_area.x, source_area.x + source_area.cx):
            rows = source.get_rgb_pixels(x, y, block_size)
            x = x + block_size.cx
            block = BlockRGB(size=block_size, rows=rows)
            row.append(block)
        block_rows.append(row)
        y = y + block_size.cy

    return BlocksRGB(Size(source_area.cx, source_area.cy, 'block'), block_rows)
