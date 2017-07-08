from .bytes_io import IoBlob
from .rope import rope

def wrap_io(file, chunk_size=2**20):
    return rope(IoBlob(file, chunk_size=chunk_size))

def open(name, chunk_size=2**20):
    file = open(name, 'rb')
    return wrap_io(file, chunk_size=chunk_size)

def dump(obj, fout):
    for chunk in rope(obj).chunks:
        fout.write(chunk)
