from .bytes_io import IoBlob
from .rope import rope

def wrap_file(file, mode='rb'):
    if 'b' in mode:
        return rope(IoBlob(file))

    raise RuntimeError('unsupported mode (only binary is allowed)')

def open(name, mode):
    file = open(name, mode)
    return wrap_file(file, mode)

def write(fout, ropelike):
    for chunk in rope(ropelike):
        fout.write(chunk)
