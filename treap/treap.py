import random


class Node:
    def __init__(self, key, priority, left=None, right=None, parent=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.k = key
        self.p = priority
        self.c = 1
        self.s = key

    def hang_left(self, node):
        if node:
            node.parent = self
        self.left = node

    def hang_right(self, node):
        if node:
            node.parent = self
        self.right = node

    def detach(self, node):
        if not node:
            return
        node.parent = None
        if self.left == node:
            self.left = None
        elif self.right == node:
            self.right = None

    def __str__(self):
        return f"(k, p)={self.k,self.p}, (c, s)={self.c, self.s}"


def build_treap(keys_dict):
    def try_to_hang(parent, child):
        nonlocal root
        if not parent:
            child.hang_left(root)
            root = child
            return
        if parent.p > child.p:
            try_to_hang(parent.parent, child)
        else:
            child.left = parent.right
            if parent.right and parent.right.parent:
                parent.right.parent = child
            parent.hang_right(child)

    root = None
    prev_node = None
    for k, p in keys_dict.items():
        node = Node(k, p)
        if not root:
            root = node
        else:
            try_to_hang(prev_node, node)
        prev_node = node
    return root


def build_implicit_treap(xs):
    root = None
    for i in range(len(xs)):
        root = insert(root, xs[i], i)
    return root


def update(t):
    if not t:
        return
    t.c = 1
    t.s = t.k
    if t.left:
        t.c += t.left.c
        t.s += t.left.s
    if t.right:
        t.c += t.right.c
        t.s += t.right.s


def size(node):
    return 0 if not node else node.c


def split(t, k):
    if not t:
        return None, None
    if t.k < k:
        rl, rr = split(t.right, k)
        if rr:
            rr.detach(rl)
        t.hang_right(rl)
        return t, rr
    ll, lr = split(t.left, k)
    if ll:
        ll.detach(lr)
    t.hang_left(lr)
    return ll, t


def split_by_size(t, k):
    if not t:
        return None, None
    if k <= size(t.left):
        ll, lr = split_by_size(t.left, k)
        t.hang_left(lr)
        update(t)
        return ll, t
    rl, rr = split_by_size(t.right, k - size(t.left) - 1)
    t.hang_right(rl)
    update(t)
    return t, rr


def merge(t1, t2):
    if not t1:
        return t2
    if not t2:
        return t1
    if t1.p < t2.p:
        t1.hang_right(merge(t1.right, t2))
        update(t1)
        return t1
    else:
        t2.hang_left(merge(t1, t2.left))
        update(t2)
        return t2


def insert(t, val, pos):
    l, r = split_by_size(t, pos)
    l = merge(l, Node(val, random.randint(0, 1000)))
    return merge(l, r)


def remove(t, k):
    def remove_helper(node):
        if node.k == k:
            node.parent.hang_left(node.right)
            return
        remove_helper(node.left)

    lt, rt = split(t, k)
    if rt and rt.k == k:
        return merge(lt, rt.right)
    else:
        remove_helper(rt)
        return merge(lt, rt)


def sum_treap(t, fr, to):
    l, r = split_by_size(t, fr)
    rl, rr = split_by_size(r, to - fr + 1)
    result = rl.s
    t = merge(l, merge(rl, rr))
    return result


def display(node):
    if node.left:
        display(node.left)
    print(node)
    if node.right:
        display(node.right)


def all(node, predicate):
    if not node:
        return True
    if not node.left and not node.right:
        return predicate(node)
    return all(node.left, predicate) and all(node.right, predicate)


xs = [5, 24, 42, 13, 99, 2, 17]
root = build_implicit_treap(xs)

for i in range(len(xs)):
    assert sum_treap(root, i, i) == xs[i]

for i in range(len(xs)):
    for j in range(i, len(xs)):
        assert sum_treap(root, i, j) == sum(xs[i : j + 1])

for _ in range(10):
    xs = [random.randint(0, 100) for _ in range(100)]
    root = build_implicit_treap(xs)
    for i in range(len(xs)):
        for j in range(i, len(xs)):
            assert sum_treap(root, i, j) == sum(xs[i : j + 1])
