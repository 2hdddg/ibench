from PIL import Image

from definitions import RGB, Size


class ImageSource(object):
    """ Buffer of RGB pixels
    """
    def __init__(self, image):
        self._image = image

    def get_rgb_pixels(self, x, y, size):
        """ Returns 2-dimensional array of RGB pixels at
        the specified offset
        """
        box = (x, y, size.cx+x, size.cy+y)
        cropped = self._image.crop(box)
        # Pixels is a single line
        # Convert to pure python list to be able
        # to slice
        line_of_pixels = [RGB(r=p[0], g=p[1], b=p[2]) for p in cropped.getdata()]

        # Make it 2 dimensional
        strides = range(0, size.cx*size.cy, size.cx)
        pixels = [line_of_pixels[stride:(stride + size.cx)] for stride in strides]

        return pixels

    def get_size_in_pixels(self):
        size = self._image.size
        return Size(cx=size[0], cy=size[1], unit='pixel')


def from_file(image_path):
    image = Image.open(image_path)
    source = ImageSource(image)
    return source
