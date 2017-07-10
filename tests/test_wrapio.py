from grope import rope, wrap_io
import six, grope, pytest

def test_empty_wrap():
    fin = six.BytesIO(b'')
    blob = wrap_io(fin)

    assert repr(blob)

    assert len(blob) == 0
    assert bytes(blob) == b''
    assert not list(blob.chunks)

def test_indexes():
    fin = six.BytesIO(b'abcdefgh')
    blob = wrap_io(fin)

    assert len(blob) == 8
    assert blob[0] == b'a'[0]
    assert blob[7] == b'h'[0]
    assert blob[-1] == b'h'[0]
    assert blob[-8] == b'a'[0]

    with pytest.raises(IndexError):
        blob[8]

    with pytest.raises(IndexError):
        blob[-9]

def test_slices():
    fin = six.BytesIO(b'abcdefgh')
    blob = wrap_io(fin)

    assert len(blob[2:6]) == 4
    assert bytes(blob[2:6]) == b'cdef'

    with pytest.raises(IndexError):
        blob[2:6:2]

def test_moving_target():
    fin = six.BytesIO(b'abcdefgh')
    blob = wrap_io(fin)

    assert len(blob) == 8

    fin.seek(4)
    fin.truncate()

    with pytest.raises(IOError):
        bytes(blob)

def test_blob_io():
    fin = six.BytesIO(b'abcdefgh' * 2**18)

    blob = wrap_io(fin)
    assert isinstance(blob, rope)

    assert len(blob) == 2**21
    assert blob[0] == b'a'[0]
    assert blob[7] == b'h'[0]
    assert blob[8] == b'a'[0]
    assert blob[-1] == b'h'[0]

    assert isinstance(blob[2:3], rope)
    assert list(blob[2:3]) == [b'c'[0]]
    assert bytes(blob[2:3]) == b'c'

    assert isinstance(blob[2:4], rope)
    assert bytes(blob[2:4]) == b'cd'

    chunks = list(blob.chunks)
    assert 1 < len(chunks) < 2**8

def test_blob_io_swap_bytes():
    fin = six.BytesIO(b'abcdefgh' * 2**18)

    blob = wrap_io(fin)
    blob = rope(blob[:4], b'x', blob[6:])

    assert bytes(blob[:7]) == b'abcdxgh'

def test_bytes_dump():
    r = b'abcdejklfghi'

    fout = six.BytesIO()
    grope.dump(r, fout)

    assert fout.getvalue() == b'abcdejklfghi'

def test_rope_dump():
    r = rope(b'abcd', b'efgh', b'ijkl')
    r = rope(r[:5], r[9:], r[5:9])

    fout = six.BytesIO()
    grope.dump(r, fout)

    assert fout.getvalue() == b'abcdejklfghi'
