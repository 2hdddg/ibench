from definitions import YCbCr, PlaneYCbCr

# Standard for television
Kb = 0.114
Kr = 0.299
# These can be derived from above
KbKrComplement = 1 - Kr - Kb
KbComplement = 1 - Kb
KrComplement = 1 - Kr
m = float(255)


def rgb_to_yCbCr(rgb):
    """Converts a single RGB pixel
    to Y, Cb, Cr
    rgb - RGB namedtuple
    returns YCbCr namedtuple
    """
    r = rgb.r / m
    g = rgb.g / m
    b = rgb.b / m

    y = Kr * r + KbKrComplement * g + Kb * b
    cb = 0.5 * ((b - y) / KbComplement)
    cr = 0.5 * ((r - y) / KrComplement)

    return YCbCr(y, cb, cr)


def blockRgb_to_planeYCbCr(block):
    y = []
    cb = []
    cr = []

    for row in block.rows:
        y.append([])
        cb.append([])
        cr.append([])
        for x, rgb in enumerate(row):
            yCbCr = rgb_to_yCbCr(rgb)

            y[-1].append(yCbCr.y)
            cb[-1].append(yCbCr.cb)
            cr[-1].append(yCbCr.cr)

    return PlaneYCbCr(block.size, y, cb, cr)
