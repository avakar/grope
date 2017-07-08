class BlobIO:
    def __init__(self, blob):
        self._blob = blob
        self._fptr = 0

    def read(self, size):
        rem = max(0, len(self._blob) - self._fptr)
        if size < 0:
            size = rem
        else:
            size = min(size, rem)

        r = bytes(self._blob[self._fptr:self._fptr + size])
        self._fptr += size
        return r

    def seek(self, offs, whence):
        if whence == 0:
            self._fptr = offs
        elif whence == 1:
            self._fptr += offs
        elif whence == 2:
            self._fptr = len(self._blob) + offs
        else:
            raise ValueError('expected 0, 1, or 2')

        if self._fptr < 0:
            self._fptr = 0

    def tell(self):
        return self._fptr
