from .bytes_io import IoBlob
from .rope import rope

def wrap_io(file):
    return rope(IoBlob(file))

def open(name):
    file = open(name, 'rb')
    return wrap_io(file)

def write(fout, ropelike):
    for chunk in rope(ropelike).chunks:
        fout.write(chunk)
