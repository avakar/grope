arity = 8

class Node:
    def __init__(self, children):
        self.children = tuple(children)
        self.length = sum(len(ch) for ch in children)

    def __len__(self):
        return self.length

def length(tree):
    root, height = tree
    return root.length

def iter_leaves(tree):
    root, height = tree
    if height == 0:
        for ch in root.children:
            yield ch
    else:
        for ch in root.children:
            for leaf in iter_leaves((ch, height - 1)):
                yield leaf

def _concat(lhs, lhs_height, rhs, rhs_height):
    if lhs_height == rhs_height:
        new_children = lhs.children + rhs.children
        ch_count = len(new_children)
        if ch_count <= arity:
            return Node(new_children), lhs_height
        else:
            ch1 = Node(new_children[:ch_count//2])
            ch2 = Node(new_children[ch_count//2:])

            return Node((ch1, ch2)), lhs_height + 1
    elif lhs_height < rhs_height:
        new, new_height = _concat(lhs, lhs_height, rhs.children[0], rhs_height - 1)
        if new_height == rhs_height:
            return _concat(new, new_height, Node(rhs.children[1:]), rhs_height)

        assert new_height + 1 == rhs_height
        rhs = Node((new,) + rhs.children[1:])
        return rhs, rhs_height
    else:
        new, new_height = _concat(lhs.children[-1], lhs_height - 1, rhs, rhs_height)
        if lhs_height == new_height:
            return _concat(Node(lhs.children[:-1]), lhs_height, new, new_height)

        assert lhs_height == new_height + 1
        lhs = Node(lhs.children[:-1] + (new,))
        return lhs, lhs_height

def concat(trees):
    if not trees:
        return Node(()), 0

    r = trees[0]
    for tree in trees[1:]:
        r = _concat(r[0], r[1], tree[0], tree[1])
    return r

def index(tree, idx):
    root, height = tree
    while True:
        for ch in root.children:
            if idx < len(ch):
                if height == 0:
                    return ch[idx]
                else:
                    root = ch
                    height -= 1
                    break

            idx -= len(ch)

def slice(tree, start, stop):
    root, height = tree

    if stop != root.length:
        root, height = _slice_right(root, height, stop)

    if start != 0:
        root, height = _slice_left(root, height, start)

    return root, height

def _build_level(children):
    nodes = []

    while len(children) > 2*arity:
        nodes.append(Node(children[:arity]))
        children = children[arity:]

    if len(children) > arity:
        node_size = len(children) // 2
        nodes.append(Node(children[:node_size]))
        nodes.append(Node(children[node_size:]))
    else:
        nodes.append(Node(children))

    return nodes

def build_pbt(chunks):
    cur_level = _build_level(chunks)
    height = 0

    while len(cur_level) > 1:
        cur_level = _build_level(cur_level)
        height += 1

    assert len(cur_level) == 1
    return cur_level[0], height

def _slice_left(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            if idx == len(ch):
                return Node(node.children[i + 1:]), 0
            else:
                return Node((ch[idx:],) + node.children[i + 1:]), 0
        else:
            new_node, new_height = _slice_left(ch, height - 1, idx)
            if i == len(node.children) - 1:
                return new_node, new_height
            else:
                return _concat(new_node, new_height, Node(node.children[i+1:]), height)

def _slice_right(node, height, idx):
    for i, ch in enumerate(node.children):
        if len(ch) < idx:
            idx -= len(ch)
        elif height == 0:
            if idx == 0:
                return Node(node.children[:i]), 0
            else:
                return Node(node.children[:i] + (ch[:idx],)), 0
        else:
            new_node, new_height = _slice_right(ch, height - 1, idx)
            if i == 0:
                return new_node, new_height
            else:
                return _concat(Node(node.children[:i]), height, new_node, new_height)
