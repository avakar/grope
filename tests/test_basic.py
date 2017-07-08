from grope import rope
import pytest

def test_empty_rope():
    r = rope()
    assert isinstance(r, rope)
    assert len(r) == 0

def test_singleton_rope():
    r = rope('a')
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
    assert rope(r) is r

def test_heterogenous_rope():
    r = rope('abcd', b'efgh')

    assert r[0] == 'a'
    assert r[4] == b'e'[0]
