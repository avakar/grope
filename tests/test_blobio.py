from grope import rope, wrap_io
import six

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

