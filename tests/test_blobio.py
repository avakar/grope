from grope import BlobIO
import pytest

def test_read():
    f = BlobIO(b'test' * 1000)

    assert f.read(6) == b'testte'
    assert f.tell() == 6
    assert f.read(6) == b'sttest'
    assert f.tell() == 12

def test_out_of_bounds_read():
    f = BlobIO(b'test' * 1000)

    f.seek(3998)
    assert f.read(10) == b'st'
    assert f.tell() == 4000

    assert f.read(10) == b''
    assert f.tell() == 4000

    f.seek(5000)
    assert f.read(10) == b''

def test_read_all():
    f = BlobIO(b'test' * 3)

    assert f.read() == b'testtesttest'

    assert f.tell() == 12
    assert f.read() == b''

    f.seek(6)
    assert f.read() == b'sttest'

def test_seek():
    f = BlobIO(b'test' * 1000)

    assert f.tell() == 0

    f.seek(0, 2)
    assert f.tell() == 4000

    f.seek(-10, 2)
    assert f.tell() == 3990

    f.seek(-1, 1)
    assert f.tell() == 3989

    f.seek(-10000, 1)
    assert f.tell() == 0

    f.seek(1000, 0)
    assert f.tell() == 1000

    f.seek(2000, 0)
    assert f.tell() == 2000

    f.seek(3000)
    assert f.tell() == 3000

    f.seek(4000, 4)
    assert f.tell() == 4000
