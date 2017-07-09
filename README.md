# grope
[![Build Status](https://travis-ci.org/avakar/grope.svg?branch=master)](https://travis-ci.org/avakar/grope)
[![PyPI](https://img.shields.io/pypi/v/grope.svg)](https://pypi.python.org/pypi/grope)
[![Coverage Status](https://coveralls.io/repos/github/avakar/grope/badge.svg?branch=master)](https://coveralls.io/github/avakar/grope?branch=master)

An implementation of a generalized rope data structure for Python.

## Installation

Install from PyPI.

    pip install grope

Requires Python 2.7+ or Python 3.3+.

## Getting started

The library defines a new type object, `rope`. Ropes are efficient concatenations
of strings. Whereas `s + t` is a linear operation over the length of the strings
`s` and `t`, constructing the rope `rope(s, t)` is logarithmic.

Otherwise, ropes behave like normal strings, in that they are immutable,
can be indexed, sliced and iterated over.

    from grope import rope

    r = rope('Tirion', ' ', 'Fordring')

    assert len(r) == len('Tirion Fordring')
    assert r[0] == 'T'
    assert r[5] == 'n'
    assert r[7] == 'F'

    assert ''.join(r) == 'Tirion Fordring'

    # Equivalent to the previous expression, but faster
    assert str(r) == 'Tirion Fordring'

When we say *string*, we actually mean any object `s` that

  * is immutable,
  * has a length (`len(s)`),
  * can be sliced without stride (`s[i:j]`),
  * optionally can be indexed (`s[i]`), and
  * optionally can be iterated over.

Such objects include those of type `str`, `bytes`, `unicode`, and `tuple`.
Additionally, `rope` objects are also considered strings in this context.
As such, ropes can be nested.

    r2 = rope(r, " says to put one's faith in the light")
    assert str(r) == "Tirion Fordring says to put one's faith in the light"

Ropes will only be indexable if all contained strings are indexable. Similarly,
iteration will only work if the contained strings are iterable.

## Rope I/O

Any readable file can be converted to a rope using `wrap_io`. The contents
of the file will not be physically present in memory, instead, they will
be selectively read from the file on demand.

You can efficiently (as in with bounded memory requirements) write a rope that
contains only `bytes` objects with `grope.dump`.

    import grope
    from grope import rope

    with open('input.bin', 'rb') as fin:
        r = grope.wrap_io(fin)

        # recompute checksum at index 0x10
        chksum = _checksum(rope(r[:0x10], b'\0\0\0\0', r[0x14:]))
        r = rope(r[:0x10], struct.pack('<I', chksum), r[0x14:])

        with open('output.bin', 'wb') as fout:
            grope.dump(r, fout)

## Chunks

Since iterating over a long rope is not efficient, it's better to walk
along the rope in chunks. Use `chunks` property of ropes to get a chunks generator.

    r = rope('long', 'strings')
    for chunk in r.chunks:
        sys.stdout.write(chunk)

Note that a rope may mere 

By default, a wrapped file will be split into chunks of about 1MB in size.
You can set the size of the chunk by passing a parameter to `wrap_io`.

## Blobs

A blob is either

  * an object of type `bytes` (or `str` in Python 2.7), or
  * a rope consisting only of `bytes` (again, or `str`) objects.

Notice that slicing a blob will again produce a blob, indexing a blob
will produce the appropriate element and calling `bytes` on a blob
will create the appropriate `bytes` object.

It's easier to write functions that accept blobs rather than readable files.
Consider a function that parses a Windows .exe file.

    def parse_pe(blob):
        hdr_offs, = struct.unpack('<H', bytes(blob[0x3c:0x3e]))

        # ...

        for section in sections:
            section.content = blob[section.offset:section.offset + section.size]

        return PeFile(hdr, sections)

The function will be efficient whether you pass a `bytes` object or a wrapped file.
Similarly, instead of serializing to a writable file, return blobs.

    def save_pe(pe_file):
        r = [serialize_hdr(pe_file.hdr)]

        for section in pe_file.sections:
            r.append(section.content)

        return rope(*r)

## BlobIO

Akin to `StringIO` and `BytesIO`, `BlobIO` turns a blob into a readable file-like
object.

    blob = rope(b'hello', b', ', b'world')
    io = grope.BlobIO(blob)
    assert io.read() == b'hello, world'
