# grope

An implementation of a generalized rope data structure.

## Getting started

Install from PyPI.

    pip install grope

Requires Python 2.7+ and Python 3.0+.

In the following text, if you're using Python 2.7, replace all references to `bytes` with `str` and
all references to `str` with `unicode`.

## Ropables

A set of ropable objects is the largest set such that each object `x` in the set

 1. has a length, i.e. `len(x)` is a valid expression, and
 2. supports slicing, i.e. `x[a:b]` is a valid expression for integers `a` and `b`.

Ropables of particular interest include `bytes` and `str` objects.

## Ropes

Any sequence of ropables can be strung together to form a rope.

    from grope import rope

    r = rope('hello, ', 'world')
    assert str(r) == 'hello, world'

Rope objects have length that is the sum of lengths of constituent parts.
They also support slicing.

    assert str(r[:5]) == 'hello'

As a consequence, all ropes are also ropables and as such can be strung together
to form longer ropes.

    r2 = rope(r[:5], ', cruel', r[6:])
    assert str(r2) == 'hello, cruel world'

Unlike builtin strings, ropes are fast to concatenate.

    s1 = 'some long string... ... ...'
    s2 = 'another long string ... ...'

    # slow; the time complexity is O(len(s))
    s = s1 + s2

    # fast; the time complexity is O(log(len(s)))
    r = rope(s1, s2)

However, conversion to string can be slow.

    # fast, O(1)
    print(str(s))

    # slow, O(len(r))
    print(str(r))

## Walking rope's chunks

Since the conversion of ropes to the builtin string objects is expensive, ropes support fast iteration of its chunks.

    from grope import iter_rope

    for chunk in iter_rope(r):
        sys.stdout.write(chunk)

Usually, large conversions can be avoided using `iter_rope`, since usually, ropes are ultimately written into a stream.
As this is such a common scenario, there is a helper function.

    from grope import write
    write(sys.stdout, r)

## Ropes over `bytes` and `str`

As a convenience, `iter_rope` also accepts `bytes` and `str` objects and yield a sequence of length 1. Furthermore,
all ropes in the package support a conversion to `bytes` and `str`.

    assert str(r) == ''.join(iter_rope(r))

Of course, the conversion is only valid if all parts of the rope are of the appropriate type.
