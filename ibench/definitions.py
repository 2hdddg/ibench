from collections import namedtuple


RGB = namedtuple('RGB', ['r', 'g', 'b'])
YCbCr = namedtuple('YCbCr', ['y', 'cb', 'cr'])

Size = namedtuple('Size', ['cx', 'cy', 'unit'])
Offset = namedtuple('Offset', ['x', 'y'])
Area = namedtuple('Area', ['x', 'y', 'cx', 'cy', 'unit'])

_block_properties = ['size', 'rows']
_plane_ycbcr_properties = ['size', 'y', 'cb', 'cr']

BlockRGB = namedtuple('BlockRGB', _block_properties)
BlockInt = namedtuple('BlockInt', _block_properties)
PlaneYCbCr = namedtuple('PlaneYCbCr', _plane_ycbcr_properties)
PlaneYCbCr420 = namedtuple('PlaneYCbCr420', _plane_ycbcr_properties)

BlocksRGB = namedtuple('BlocksRGB', _block_properties)
PlanesYCbCr = namedtuple('PlanesYCbCr', _block_properties)
PlanesYCbCr420 = namedtuple('PlanesYCbCr420', _block_properties)
