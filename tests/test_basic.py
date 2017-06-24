from grope import rope

def test_rope():
    r = rope('hello', ', world')
    assert str(r) == 'hello, world'
