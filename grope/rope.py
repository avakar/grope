class RopeNode:
    def __init__(self, *children):
        self.children = children
        self.length = sum(len(ch) for ch in children)

    def __len__(self):
        return self.length

def _iter_leaves(node, height):
    if height == 0:
        for ch in node.children:
            yield ch
    else:
        for ch in node.children:
            for leaf in _iter_leaves(ch, height - 1):
                yield leaf

_arity = 8

def _concat(lhs, lhs_height, rhs, rhs_height):
    if lhs_height == rhs_height:
        new_children = lhs.children + rhs.children
        if len(new_children) <= _arity:
            return RopeNode(*new_children), lhs_height
        else:
            ch1 = RopeNode(*new_children[:_arity//2])
            ch2 = RopeNode(*new_children[_arity//2:])

            return RopeNode(ch1, ch2), lhs_height + 1
    elif lhs_height < rhs_height:
        lhs, lhs_height = _concat(lhs, lhs_height, rhs.children[0], rhs_height - 1)
        if lhs_height == rhs_height:
            return _concat(lhs, lhs_height, RopeNode(*rhs.children[1:]), rhs_height)

        assert lhs_height + 1 == rhs_height
        rhs = RopeNode(lhs, *rhs.children[1:])
        return rhs, rhs_height
    else:
        rhs, rhs_height = _concat(lhs.children[-1], lhs_height - 1, rhs, rhs_height)
        if lhs_height == rhs_height:
            return _concat(RopeNode(*lhs.children[:-1]), lhs_height, rhs, rhs_height)

        assert lhs_height== rhs_height + 1
        lhs = RopeNode(*(lhs.children[:-1] + (rhs,)))
        return lhs, lhs_height

def _slice_left(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            return RopeNode(ch[idx:], *node.children[i + 1:]), 0
        else:
            new_node, new_height = _slice_left(ch, height - 1, idx)
            if i == len(node.children) - 1:
                return new_node, new_height
            else:
                return _concat(new_node, new_height, RopeNode(node.children[i+1:]), height)

def _slice_right(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            return RopeNode(*(node.children[:i] + (ch[:idx],))), 0
        else:
            new_node, new_height = _slice_right(ch, height - 1, idx)
            if i == len(node.children) - 1:
                return new_node, new_height
            else:
                return _concat(RopeNode(node.children[:i]), height, new_node, new_height)

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
