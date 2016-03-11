from definitions import PlaneYCbCr420


def _444_to_420(cx, cy, in_rows):
    if cx % 2:
        raise "hell"

    if cy % 2:
        raise "hell"

    rows = []
    for y in range(0, cy, 2):
        row = []
        for x in range(0, cx, 2):
            p11 = in_rows[y][x]
            p12 = in_rows[y][x + 1]
            p21 = in_rows[y + 1][x]
            p22 = in_rows[y + 1][x + 1]

            p = (p11 + p12 + p21 + p22) / 4
            row.append(p)
        rows.append(row)

    return rows


def _copy(buf):
    rows = []

    for y in buf:
        row = []
        for x in y:
            row.append(x)
        rows.append(row)

    return rows


def planeYCbCr_to_planeYCbCr420(planeYCbCr):
    """ Converts buffer of YCbCr pixels to
    a buffer containing subsampled buffers
    of y, Cb and Cr
    """
    size = planeYCbCr.size
    cx = size.cx
    cy = size.cy

    y = _copy(planeYCbCr.y)
    cb = _444_to_420(cx, cy, planeYCbCr.cb)
    cr = _444_to_420(cx, cy, planeYCbCr.cr)

    planeYCbCr420 = PlaneYCbCr420(
        size=size, y=y, cb=cb, cr=cr)

    return planeYCbCr420
