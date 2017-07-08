class rope(object):
    def __new__(cls, *ropables):
        if len(ropables) == 1 and isinstance(ropables[0], rope):
            return ropables[0]

        self = super(rope, cls).__new__(cls)
        self._children = ropables
        self._len = sum(len(c) for c in ropables)
        return self

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        if not isinstance(key, slice):
            key = slice(key, key + 1)
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
            for chunk in iter_rope(c):
                yield chunk

    def __bytes__(self):
        return b''.join(iter_rope(self))

    def __str__(self):
        return ''.join(iter_rope(self))

def iter_rope(rope):
    iterrope = getattr(rope, '__iterrope__', None)
    if iterrope is None:
        yield rope
    else:
        for chunk in iterrope():
            yield chunk
