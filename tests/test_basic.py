from grope import rope
import pytest, string, sys

class _MockString:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, key):
        if not isinstance(key, slice):
            if not (-len(self) <= key < len(self)):
                raise AttributeError('out of bounds')
            if key < 0:
                key = len(self) + key
            return self.start + key
        else:
            start, stop, step = key.indices(len(self))
            assert step == 1
            return _MockString(self.start + start, self.start + stop)

    def __repr__(self):
        return '_MockString({}, {})'.format(self.start, self.stop)

def test_empty_rope():
    r = rope()
    assert isinstance(r, rope)
    assert len(r) == 0

def test_singleton_rope():
    r = rope('a')
    assert repr(r) == "rope('a')"
    assert isinstance(r, rope)
    assert len(r) == 1

def test_concat_rope():
    r = rope('a', 'b')
    assert isinstance(r, rope)
    assert len(r) == 2

def test_empty_leaves():
    r = rope('', '')
    assert len(r) == 0
    assert str(r) == ''

def test_rope_iteration():
    r = rope('a', 'bc', '', 'd')
    assert list(r) == ['a', 'b', 'c', 'd']

def test_rope_chunks():
    r = rope('a', 'bc', '', 'd')
    assert ''.join(r.chunks) == 'abcd'

def test_slicing():
    r = rope('abcd', 'efgh')
    rr = r[2:6]
    assert len(rr) == 4
    assert str(rr) == 'cdef'

def test_empty_slice():
    r = rope(_MockString(0, 1000))
    for ch in r.chunks:
        assert len(ch) != 0

    rr = r[0:0]
    for ch in rr.chunks:
        assert len(ch) != 0

    rr = r[999:999]
    for ch in rr.chunks:
        assert len(ch) != 0

    rr = r[1000:1000]
    for ch in rr.chunks:
        assert len(ch) != 0

def test_indexing():
    r = rope('abcd', 'efgh')

    assert r[0] == 'a'
    assert r[3] == 'd'
    assert r[4] == 'e'
    assert r[7] == 'h'
    assert r[-1] == 'h'
    assert r[-8] == 'a'

    with pytest.raises(IndexError):
        r[8]

    with pytest.raises(IndexError):
        r[-9]

def test_idempotence():
    r = rope('test')
    assert rope(r)._tree is r._tree

def test_heterogenous_rope():
    r = rope('abcd', b'efgh')

    assert r[0] == 'a'
    assert r[4] == b'e'[0]

def test_balancing():
    r = rope(*string.ascii_lowercase)
    assert str(r) == string.ascii_lowercase

if sys.version_info.major == 2:
    def test_unicode_conversion():
        r = rope(u'abcd', u'efgh')
        assert unicode(r) == u'abcdefgh'
