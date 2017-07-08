class rope(object):
    def __new__(cls, *ropables):
        if len(ropables) == 1 and isinstance(ropables[0], rope):
            return ropables[0]

        self = super(rope, cls).__new__(cls)
        self._children = ropables
        self._len = sum(len(c) for c in ropables)
        return self

    def __repr__(self):
        return 'rope({})'.format(', '.join(repr(ch) for ch in self.chunks))

    @property
    def chunks(self):
        return self.__iterrope__()

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        if not isinstance(key, slice):
            if key < 0:
                key = len(self) + key

            if key < 0 or key >= len(self):
                raise IndexError('index out of bounds')

            for child in self._children:
                if key >= len(child):
                    key -= len(child)
                    continue

                return child[key]
        else:
            start, stop, step = key.indices(self._len)
            if step != 1:
                raise RuntimeError('strides are not supported')

            size = stop - start

            parts = []
            for c in self._children:
                if len(c) <= start:
                    start -= len(c)
                    continue

                if start + size <= len(c):
                    parts.append(c[start:start + size])
                    break

                parts.append(c[start:])
                size -= len(c) - start
                start = 0

            return rope(*parts)

    def __iterrope__(self):
        for c in self._children:
            for chunk in _iter_rope(c):
                yield chunk

    def __bytes__(self):
        return b''.join(self.chunks)

    def __str__(self):
        return ''.join(self.chunks)

def _iter_rope(rope):
    iterrope = getattr(rope, '__iterrope__', None)
    if iterrope is None:
        yield rope
    else:
        for chunk in iterrope():
            yield chunk
