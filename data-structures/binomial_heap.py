from typing import Any
import random, math


class BinomialHeapNode:
    def __init__(self, p=0, v=0, k=0, parent=None, next=None, child=None) -> None:
        self.p = p
        self.val = v
        self.k = k
        self.parent = parent
        self.next = next
        self.child = child

    def __str__(self) -> str:
        return f"p: {self.p}, k: {self.k}, val: {self.val}"


class BinomialHeap:
    def __init__(self, root: Any) -> None:
        self.root = root

    def __str__(self) -> str:
        return f"heap: {self.root}"

    def max_k(self):
        i = self.root
        maxk = 0
        while i:
            maxk = max(maxk, i.k)
            i = i.next
        return maxk

    def empty(self) -> bool:
        return self.root is None

    def rmv_root(self, trgt):
        i = self.root
        while i and i.next != trgt:
            i = i.next
        if i:
            i.next = trgt.next

    def invariant(self) -> bool:
        r = self.root
        prev_k = -(10**6)
        while r:
            if r.k <= prev_k:
                print("Heap has been broken")
                return False
            ch = r.child
            while ch:
                n = ch
                while n:
                    if n.p < n.parent.p:
                        print("Heap has been broken")
                        return False
                    n = n.next
                ch = ch.child
            prev_k = r.k
            r = r.next
        return True

    def insert(self, priority=0, value=0) -> Any:
        node = BinomialHeapNode(priority, value)
        self.root = merge_heaps(self, BinomialHeap(node)).root
        self.invariant()
        return node

    def peek_min(self) -> Any:
        if self.empty():
            return None
        m = 10**6
        min_node = self.root
        i = self.root
        while i:
            if i.p < m:
                m = i.p
                min_node = i
            i = i.next
        return min_node

    def extract_min(self) -> Any:
        m = self.peek_min()
        if not m:
            print("Heap is empty")
            return None
        if m.child:
            rmv_parent(m.child)
        if m == self.root:
            newroot = merge_heaps(BinomialHeap(m.next), BinomialHeap(m.child))
            self.root = newroot.root if newroot else None
        else:
            self.rmv_root(m)
            self.root = merge_heaps(BinomialHeap(self.root), BinomialHeap(m.child)).root
        return m

    def sift_up(self, node: BinomialHeapNode):
        while node.parent and node.p < node.parent.p:
            node.parent.p, node.p = node.p, node.parent.p
            node.parent.val, node.val = node.val, node.parent.val
            node = node.parent

    def decrease_key(self, node: BinomialHeapNode, np) -> None:
        if np >= node.p:
            return
        node.p = np
        self.sift_up(node)

    def delete_key(self, node: BinomialHeapNode) -> None:
        self.decrease_key(node, -math.inf)
        self.extract_min()


def rmv_parent(head: BinomialHeapNode):
    while head:
        head.parent = None
        head = head.next


def swap_nodes(heap: BinomialHeap, n1: BinomialHeapNode, n2: BinomialHeapNode):
    if n2.parent:
        n2.parent.child = n1
    # swapping with heap root
    else:
        # looking for previous root
        i = heap.root
        while i:
            if i.next == n2:
                i.next = n1
                break
            i = i.next

    n1.next, n2.next = n2.next, n1.next
    n1.parent, n2.parent = n2.parent, n1


def merge_trees(t1: Any, t2: Any) -> BinomialHeapNode:
    min_p_tree = t1 if t1.p < t2.p else t2
    merged = min_p_tree
    merged.k += 1
    if t1.p < t2.p:
        t2.parent = merged
        t2.next = merged.child
        merged.child = t2
    else:
        t1.parent = merged
        t1.next = merged.child
        merged.child = t1
    return merged


def merge_heaps(h1: BinomialHeap, h2: BinomialHeap) -> Any:
    m_root = None
    carry = None

    if h1.empty() and not h2.empty():
        maxk = h2.max_k()
    elif h2.empty() and not h1.empty():
        maxk = h1.max_k()
    elif not (h1.empty() and h2.empty()):
        maxk = max(h1.max_k(), h2.max_k())
    else:
        return None
    # t1 = [None] * (maxk + 1)
    # t2 = [None] * (maxk + 1)
    t1 = [None for _ in range(maxk + 1 + 1)]
    t2 = [None for _ in range(maxk + 1 + 1)]

    i = h1.root
    while i:
        t1[i.k] = i
        i = i.next

    i = h2.root
    while i:
        t2[i.k] = i
        i = i.next
    roots = [None for _ in range(maxk + 1 + 1)]

    for i in range(maxk + 1):
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
    t = None
    for r in roots:
        if r:
            r.next = None
            if m_root:
                t.next = r
            else:
                m_root = r
            t = r
    return BinomialHeap(m_root)


def test_insertion():
    heap = BinomialHeap(BinomialHeapNode(0, 0))
    for i in range(100):
        heap.insert(random.randint(0, i), i * 2)
    assert heap.invariant()


def test_extracting():
    heap = BinomialHeap(BinomialHeapNode())
    p = [random.randint(-1000, 1000) for _ in range(1000)]

    for i in range(len(p)):
        heap.insert(p[i], i * 2)

    assert heap.invariant()

    # because of root
    p.append(0)
    sp = sorted(p)
    l = 0

    while not heap.empty():
        m = heap.extract_min().p
        assert m == sp[l]
        l += 1

    assert heap.invariant()


def test_decreasing_key():
    heap = BinomialHeap(BinomialHeapNode())
    p = [89, 0, 1, -2, 5, 10, -100, 1000]

    nodes = {}
    for i in range(len(p)):
        nodes[p[i]] = heap.insert(p[i], p[i])

    assert heap.peek_min().p == -100
    assert heap.invariant()

    heap.decrease_key(heap.root, -100)
    assert heap.invariant()
    assert heap.peek_min().p == -100

    heap.decrease_key(heap.root, -200)
    assert heap.invariant()
    assert heap.peek_min().p == -200

    # decreasing
    heap.decrease_key(nodes[89], -250)
    assert heap.invariant()
    assert heap.peek_min().p == -250
    assert heap.peek_min().val == 89

    for _ in range(100):
        heap = BinomialHeap(BinomialHeapNode())
        p = [random.randint(-100, 100) for _ in range(1000)]
        nodes = {}
        for i in range(len(p)):
            nodes[p[i]] = heap.insert(p[i], p[i])
        rnode = list(nodes.keys())[random.randint(0, len(nodes.keys()) - 1)]
        heap.decrease_key(nodes[rnode], -(10**6))
        assert heap.invariant()
        assert heap.peek_min().p == -(10**6)
        assert heap.peek_min().val == rnode

def lookup(heap:BinomialHeap, priority) -> bool:
    r = heap.root
    while r:
        ch = r.child
        while ch:
            n = ch
            while n:
                if n.p == priority:
                    return True
                n = n.next
            ch = ch.child
        r = r.next
    return False

def test_deleting():
    heap = BinomialHeap(BinomialHeapNode())
    p = [89, 0, 1, -2, 5, 23, 10, -100, 100]
    nodes = {}
    for i in range(len(p)):
        nodes[p[i]] = heap.insert(p[i], p[i])
    heap.delete_key(nodes[89])
    assert heap.invariant()
    assert not lookup(heap, nodes[89])

    heap.delete_key(nodes[-100])
    assert heap.invariant()
    assert not lookup(heap, nodes[-100])
    assert heap.peek_min().p != -100

    while not heap.empty():
        m = heap.peek_min()
        heap.delete_key(m)
        assert not lookup(heap, m.p)


test_insertion()
test_extracting()
test_decreasing_key()
test_deleting()
