from copy import deepcopy


class BinomialTreeNode:
    def __init__(
        self, priority=0, value=0, parent=None, left_child=None, right=None, k=0
    ) -> None:
        self.priority = priority
        self.left_child = left_child
        self.value = value
        self.parent = parent
        self.right = right
        self.k = k

    def __str__(self) -> str:
        return f"Priority: {self.priority}, value: {self.value}, k: {self.k}"


class BinomialHeap:
    def __init__(self, root=None) -> None:
        self.root = root
        self.tail = root

    def trees_add_tail(self, tree):
        if not self.root:
            self.root = tree
            self.tail = tree
        else:
            self.tail.right = tree
            self.tail = tree

    def trees_add_head(self, tree):
        if not self.root:
            self.root = tree
            self.tail = tree
        else:
            tree.right = self.root
            self.root = tree

    def print_tree_roots(self):
        it = self.root
        while it:
            print(it)
            it = it.right

    def peek_min(self):
        min_r = 10**6
        result_node = None
        it = self.root
        while it:
            if it.priority < min_r:
                min_r = it.priority
                result_node = it
            it = it.right
        return result_node

    def insert(self, priority, value):
        h = BinomialHeap(BinomialTreeNode(priority=priority, value=value, k=0))
        merged = merge_heaps(self, h)
        self.root = merged.root
        self.tail = merged.tail
    
    def extract_min(self):
        m = self.peek_min()
        it = self.root
        while it:
            if it.right == m:
                break
            it = it.right
        it.right = m.right
        if m.left_child:
            h = BinomialHeap(m.left_child)
            merged = merge_heaps(self, h)
            self.root = merged.root
            self.tail = merged.tail


def merge_trees(t1: BinomialTreeNode, t2: BinomialTreeNode):
    new_tree = BinomialTreeNode()
    if t1.priority < t2.priority:
        new_tree = deepcopy(t1)
        t2.right = t1.left_child
        t2.parent = t1
        new_tree.left_child = t2
    else:
        new_tree = deepcopy(t2)
        t1.right = t2.left_child
        t1.parent = t2
        new_tree.left_child = t1
    new_tree.k = t1.k + 1
    return new_tree


def merge_heaps(h1: BinomialHeap, h2: BinomialHeap):
    merged = BinomialHeap()
    carry = None

    maxk = max(h1.tail.k, h2.tail.k)

    t1 = [None] * (maxk + 1)
    t2 = [None] * (maxk + 1)

    it = h1.root

    it = h1.root
    while it:
        t1[it.k] = it
        it = it.right

    it = h2.root
    while it:
        t2[it.k] = it
        it = it.right

    nmax = max(len(t1), len(t2))
    roots = [None] * nmax
    for i in range(nmax):
        if t1[i] and t2[i] and carry:
            roots[i] = carry
            carry = merge_trees(t1[i], t2[i])
        elif t1[i] and t2[i]:
            carry = merge_trees(t1[i], t2[i])
        elif t1[i] and carry:
            carry = merge_trees(t1[i], carry)
        elif carry and t2[i]:
            carry = merge_trees(carry, t2[i])
        elif t1[i]:
            roots[i] = t1[i]
        elif t2[i]:
            roots[i] = t2[i]
        else:
            roots[i] = carry
            carry = None
    if carry is not None:
        roots[-1] = carry
    for root in roots:
        if root:
            merged.trees_add_tail(root)
    return merged


r = BinomialTreeNode(-1)
h = BinomialHeap(r)
for i in range(100):
    h.insert(i, 0)
h.print_tree_roots()
h.extract_min()
# print(h.peek_min())
print("---")
h.print_tree_roots()
# h.insert(-2, 0)
# print(h.peek_min())
