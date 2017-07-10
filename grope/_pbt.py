class RopeNode:
    def __init__(self, *children):
        self.children = children
        self.length = sum(len(ch) for ch in children)

    def __len__(self):
        return self.length

def _iter_leaves(node, height):
    if height == 0:
        for ch in node.children:
            yield ch
    else:
        for ch in node.children:
            for leaf in _iter_leaves(ch, height - 1):
                yield leaf

_arity = 8

def _concat(lhs, lhs_height, rhs, rhs_height):
    if lhs_height == rhs_height:
        new_children = lhs.children + rhs.children
        if len(new_children) <= _arity:
            return RopeNode(*new_children), lhs_height
        else:
            ch1 = RopeNode(*new_children[:_arity//2])
            ch2 = RopeNode(*new_children[_arity//2:])

            return RopeNode(ch1, ch2), lhs_height + 1
    elif lhs_height < rhs_height:
        lhs, lhs_height = _concat(lhs, lhs_height, rhs.children[0], rhs_height - 1)
        if lhs_height == rhs_height:
            return _concat(lhs, lhs_height, RopeNode(*rhs.children[1:]), rhs_height)

        assert lhs_height + 1 == rhs_height
        rhs = RopeNode(lhs, *rhs.children[1:])
        return rhs, rhs_height
    else:
        rhs, rhs_height = _concat(lhs.children[-1], lhs_height - 1, rhs, rhs_height)
        if lhs_height == rhs_height:
            return _concat(RopeNode(*lhs.children[:-1]), lhs_height, rhs, rhs_height)

        assert lhs_height== rhs_height + 1
        lhs = RopeNode(*(lhs.children[:-1] + (rhs,)))
        return lhs, lhs_height

def _slice_left(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            return RopeNode(ch[idx:], *node.children[i + 1:]), 0
        else:
            new_node, new_height = _slice_left(ch, height - 1, idx)
            if i == len(node.children) - 1:
                return new_node, new_height
            else:
                return _concat(new_node, new_height, RopeNode(node.children[i+1:]), height)

def _slice_right(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            return RopeNode(*(node.children[:i] + (ch[:idx],))), 0
        else:
            new_node, new_height = _slice_right(ch, height - 1, idx)
            if i == len(node.children) - 1:
                return new_node, new_height
            else:
                return _concat(RopeNode(node.children[:i]), height, new_node, new_height)
