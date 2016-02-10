import copy


class Buf(object):
    """Representation of data that "flows" through
    different transformations. Each transformation
    takes an intermediate as input and creates a new one
    as its output and connects the two.
    Treat as immutable!
    Short name of this class is due to python built-in: buffer
    """
    def __init__(self, data, format, size, label, prior=None):
        self._data = data
        self._format = format
        self._size = size
        self._label = label
        self._prior = prior

    @property
    def data(self):
        cloned = copy.copy(self._data)
        return cloned

    @property
    def label(self):
        return self._label

    @property
    def format(self):
        return self._format

    @property
    def size(self):
        return self._size

    @property
    def prior(self):
        return self._prior

    def __str__(self):
        return '%s as %s' % (self._label, self._format)
