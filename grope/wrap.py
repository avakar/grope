from .bytes_io import IoBlob
from .rope import rope
import io

def wrap_io(file, chunk_size=2**20):
    return rope(IoBlob(file, chunk_size=chunk_size))

def dump(obj, fout):
    for chunk in rope(obj).chunks:
        fout.write(chunk)
