class _Rope:
    def __init__(self, children):
        self._children = children
        self._len = sum(len(c) for c in children)

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

def rope(*ropables):
    # TODO: optimize, in particular, actually implement rope data structure
    return _Rope(ropables)
