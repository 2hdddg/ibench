from collections import namedtuple


RGB = namedtuple('RGB', ['r', 'g', 'b'])
YCbCr = namedtuple('YCbCr', ['Y', 'Cb', 'Cr'])

Size = namedtuple('Size', ['cx', 'cy', 'unit'])
Offset = namedtuple('Offset', ['x', 'y'])
Area = namedtuple('Area', ['x', 'y', 'cx', 'cy', 'unit'])

_block_properties = ['size', 'rows']

BlockRGB = namedtuple('BlockRGB', _block_properties)
BlockInt = namedtuple('BlockInt', _block_properties)
PlanesYCbCr = namedtuple('PlanesYCbCr', ['y', 'cb', 'cr'])

BlocksRGB = namedtuple('BlocksRGB', _block_properties)
