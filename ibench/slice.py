from buf import Buf
from definitions import Size, Area, Buf_2d_rgb, Buf_2d_buffers_of_2d_rgb


def _get_size_in_blocks(block_size, size_in_pixels):
    # Full blocks
    cx = size_in_pixels.cx / block_size.cx
    cy = size_in_pixels.cy / block_size.cx

    size_in_blocks = Size(cx=cx, cy=cy, unit='block')

    return size_in_blocks


def source(
        source, block_size, block_area=None):
    blocked_size = _get_size_in_blocks(
        block_size, source.get_size_in_pixels())
    block_area = block_area if block_area else Area(0, 0, blocked_size.cx, blocked_size.cy, 'block')
    blocks = []

    y = block_area.y * block_size.cy
    for block_y in range(block_area.y, block_area.y + block_area.cy):
        line = []
        x = block_area.x * block_size.cx
        for block_x in range(block_area.x, block_area.x + block_area.cx):
            pixels = source.get_rgb_pixels(
                x, y, block_size)
            x = x + block_size.cx
            block_buf = Buf(
                data=pixels,
                format=Buf_2d_rgb,
                size=Size(cx=block_size.cx, cy=block_size.cy, unit='pixel'),
                label='Block %s:%s' % (block_x, block_y))
            line.append(block_buf)
        blocks.append(line)
        y = y + block_size.cy

    buf = Buf(
        data=blocks,
        format=Buf_2d_buffers_of_2d_rgb,
        size=blocked_size,
        label='Blocks %sx%s' % (blocked_size.cx, blocked_size.cy))

    return buf
