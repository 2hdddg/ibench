from collections import namedtuple


def _format_2d_array_of_x(x):
    return '[[]:(%s)]' % x


RGB = namedtuple('Pixel', ['r', 'g', 'b'])
YCbCr = namedtuple('YCbCr', ['Y', 'Cb', 'Cr'])

Size = namedtuple('Size', ['cx', 'cy', 'unit'])
Offset = namedtuple('Offset', ['x', 'y'])
Area = namedtuple('Area', ['x', 'y', 'cx', 'cy', 'unit'])

Buf_2d_rgb = _format_2d_array_of_x('RGB')
Buf_2d_buffers_of_2d_rgb = _format_2d_array_of_x(Buf_2d_rgb)
