from ._pbt import RopeNode, _concat, _slice_left, _slice_right, _iter_leaves

class rope(object):
    def __init__(self, *ropables):
        nodes = [(v._root, v._height) if isinstance(v, rope) else (RopeNode(v), 0) for v in ropables if len(v) != 0]

        if len(nodes) == 0:
            self._root = RopeNode()
            self._height = 0
        else:
            self._root, self._height = nodes[0]
            for node, node_height in nodes[1:]:
                self._root, self._height = _concat(self._root, self._height, node, node_height)

    def __repr__(self):
        return 'rope({})'.format(', '.join(repr(ch) for ch in _iter_leaves(self._root, self._height)))

    @property
    def chunks(self):
        return self.__iterrope__()

    def __len__(self):
        return self._root.length

    def __getitem__(self, key):
        if not isinstance(key, slice):
            if key < 0:
                key = len(self) + key
            if key < 0:
                raise IndexError('index out of bounds')

            cur = self._root
            height = self._height
            while True:
                for ch in cur.children:
                    if key < len(ch):
                        if height == 0:
                            return ch[key]
                        else:
                            cur = ch
                            height -= 1
                            break

                    key -= len(ch)
                else:
                    raise IndexError('index out of bounds')
        else:
            start, stop, step = key.indices(len(self))
            if step != 1:
                raise IndexError('strides are not supported')

            root = self._root
            height = self._height

            if stop != len(self):
                root, height = _slice_right(root, height, stop)

            if start != 0:
                root, height = _slice_left(root, height, start)

            r = rope()
            r._root = root
            r._height = height
            return r

    def __iterrope__(self):
        for leaf in _iter_leaves(self._root, self._height):
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
