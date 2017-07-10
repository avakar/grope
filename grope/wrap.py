from .rope import rope
import io

class _FileWrap:
    def __init__(self, file, chunk_size=2**20, start=0, stop=None):
        self._file = file
        self._chunk_size = chunk_size
        self._start = start

        if stop is None:
            file.seek(0, 2)
            self._len = file.tell()
        else:
            self._len = stop - start

    def __repr__(self):
        return '{!r}[{}:{}]'.format(self._file, self._start, self._start + self._len)

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        if not isinstance(key, slice):
            assert 0 <= key < self._len
            self._file.seek(key + self._start, 0)
            return self._file.read(1)[0]
        else:
            start, stop, step = key.indices(self._len)
            assert step == 1
            return _FileWrap(self._file, self._chunk_size, self._start + start, self._start + stop)

    def __iterrope__(self):
        assert self._len

        self._file.seek(self._start, 0)

        read = 0
        while read < self._len:
            chunk = min(self._chunk_size, self._len - read)
            r = self._file.read(chunk)
            if not r:
                raise IOError('reached eof prematurely')
            yield r
            read += len(r)

def wrap_io(file, chunk_size=2**20):
    return rope(_FileWrap(file, chunk_size=chunk_size))

def dump(obj, fout):
    for chunk in rope(obj).chunks:
        fout.write(chunk)
