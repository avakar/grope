from grope import _pbt
import six

class Range:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __repr__(self):
        return 'Range({}, {})'.format(self.start, self.stop)

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return Range(self.start + start, self.start + stop)

        return self.start + key

    def __eq__(self, rhs):
        return (self.start, self.stop) == (rhs.start, rhs.stop)

def _is_consistent(tree):
    root, height = tree
    if height == 0:
        return True

    return all(len(ch.children) >= _pbt.arity // 2 and _is_consistent((ch, height - 1)) for ch in root.children)

def _make_pbt(levels):
    chunks = _pbt.arity**levels
    tree = _pbt.build_pbt([Range(i*100, (i + 1)*100) for i in six.moves.range(chunks)])
    assert _is_consistent(tree)
    return tree, Range(0, chunks*100)

def _collate(tree):
    r = []
    start = None
    for range in _pbt.iter_leaves(tree):
        if start is None:
            start = range.start
            stop = range.stop
        else:
            if stop == range.start:
                stop = range.stop
            else:
                r.append(Range(start, stop))
                start = range.start
                stop = range.stop

    if start is not None:
        r.append(Range(start, stop))

    return tuple(r)

def test_slice():
    t1, r1 = _make_pbt(4)

    r2 = Range(r1.start + 1234, r1.stop - 1234)

    t = _pbt.slice(t1, r2.start, r2.stop)
    assert _is_consistent(t)
    assert _collate(t) == (r2,)

def test_slice2():
    t1, r1 = _make_pbt(4)

    r2 = Range(r1.start + 1234, r1.start + 2234)

    t = _pbt.slice(t1, r2.start, r2.stop)
    assert _is_consistent(t)
    assert _collate(t) == (r2,)

def test_index():
    t1, r1 = _make_pbt(4)
    assert _pbt.index(t1, 1234) == 1234

def test_concat():
    t1, r1 = _make_pbt(4)
    t2, r2 = _make_pbt(3)

    tree = _pbt.concat((t1, t2))

    assert _is_consistent(tree)
    assert _collate(tree) == (r1, r2)

def test_concat2():
    t1, r1 = _make_pbt(4)
    t2, r2 = _make_pbt(2)

    tree = _pbt.concat((t1, t2))

    assert _is_consistent(tree)
    assert _collate(tree) == (r1, r2)
