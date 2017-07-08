from .rope import rope

class IoBlob:
    def __init__(self, file, start=0, stop=None):
        self._file = file
        self._start = start

        if stop is None:
            file.seek(0, 2)
            self._len = file.tell()
        else:
            self._len = stop - start

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        if not isinstance(key, slice):
            if key < 0:
                key = self._len + key
            if key < 0 or key >= self._len:
                raise IndexError('index out of bounds')

            self._file.seek(key + self._start, 0)
            return self._file.read(1)[0]
        else:
            start, stop, step = key.indices(self._len)
            if step != 1:
                raise IndexError('strides are not supported')

            return IoBlob(self._file, self._start + start, self._start + stop)

    def __iterrope__(self):
        if self._len == 0:
            return

        self._file.seek(self._start, 0)

        read = 0
        while read < self._len:
            chunk = min(2**20, self._len - read)
            r = self._file.read(chunk)
            if not r:
                raise IOError('reached eof prematurely')
            yield r
            read += len(r)

    def __bytes__(self):
        return bytes(rope(self))
