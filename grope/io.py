from .bytes_io import IoBlob
from .rope import iter_rope, rope

def wrap_file(file, mode='rb'):
    if 'b' in mode:
        return rope(IoBlob(file))

    raise RuntimeError('unsupported mode (only binary is allowed)')

def open(name, mode):
    file = open(name, mode)
    return wrap_file(file, mode)

def write(fout, rope):
    for chunk in iter_rope(rope):
        fout.write(chunk)
