from . import _pbt

class rope(object):
    def __init__(self, *chunks):
        trees = []

        i = 0
        while i < len(chunks):
            start = i
            while i < len(chunks) and isinstance(chunks[i], rope):
                i += 1
            trees.extend(r._tree for r in chunks[start:i])

            start = i
            while i < len(chunks) and not isinstance(chunks[i], rope):
                i += 1

            nonempty_chunks = [ch for ch in chunks[start:i] if len(ch) != 0]
            if nonempty_chunks:
                trees.append(_pbt.build_pbt(nonempty_chunks))

        self._tree =_pbt.concat(trees)

    def __repr__(self):
        return 'rope({})'.format(', '.join(repr(ch) for ch in _pbt.iter_leaves(self._tree)))

    @property
    def chunks(self):
        return self.__iterrope__()

    def __len__(self):
        return _pbt.length(self._tree)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            if key < 0:
                key = len(self) + key
            if key < 0 or key >= len(self):
                raise IndexError('index out of bounds')

            return _pbt.index(self._tree, key)
        else:
            start, stop, step = key.indices(len(self))
            if step != 1:
                raise IndexError('strides are not supported')

            r = rope()
            r._tree = _pbt.slice(self._tree, start, stop)
            return r

    def __iter__(self):
        for chunk in self.chunks:
            for item in chunk:
                yield item

    def __iterrope__(self):
        for leaf in _pbt.iter_leaves(self._tree):
            iterrope = getattr(leaf, '__iterrope__', None)
            if iterrope is None:
                yield leaf
            else:
                for chunk in iterrope():
                    yield chunk

    def __bytes__(self):
        return b''.join(self.chunks)

    def __str__(self):
        return ''.join(self.chunks)

    def __unicode__(self):
        return u''.join(self.chunks)
