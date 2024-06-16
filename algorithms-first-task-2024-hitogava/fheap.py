import math


class GNode:
    def __init__(self, priority=0, value=0, d=math.inf, tr=0) -> None:
        self.p = priority
        self.val = value
        self.adj = []
        self.d = d
        self.tr = tr

    def __str__(self):
        return f"{self.p}, {self.val}"


class HeapNode:
    def __init__(
        self,
        content=GNode(),
        marked=0,
        degree=0,
        parent=None,
        prev=None,
        next=None,
        child=None,
    ) -> None:
        self.content = content
        self.marked = marked
        self.degree = degree
        self.parent = parent
        self.next = next
        self.prev = prev
        self.child = child

    def __str__(self) -> str:
        return f"p: {self.content.p}, v: {self.content.val}, d: {self.degree}"

    def __lt__(self, other):
        return self.content.p < other.content.p


class FibHeap:
    def __init__(self, head=None, tail=None, N=1) -> None:
        if not tail:
            tail = head
        self.head = head
        self.tail = tail
        self.current_min = self.head

        self.N = N

    def insert(self, t: GNode):
        node = HeapNode(t)
        self.N += 1
        self.rpush(node)
        return node

    def peek_min(self):
        return self.current_min

    def cut_prep(self, t):
        assert t.parent.child
        if t.parent.child == t:
            t.parent.child = t.next
            if t.next:
                t.next.prev = None
        elif t.parent.child:
            t.prev.next = t.next
            if t.next:
                t.next.prev = t.prev
        t.prev = None
        t.next = None
        t.parent.degree -= 1

    def cut_subtree(self, t):
        if not t.parent:
            return
        self.cut_prep(t)
        pbuf = t.parent
        t.parent = None
        self.rpush(t)
        if pbuf.marked:
            self.cut_subtree(pbuf)
        else:
            pbuf.marked = 1

    def empty(self):
        return self.head is None

    def decrease_key(self, node, newp):
        node.content.p = newp
        if not node.parent:
            self.update_min(node)
        elif node.parent and node.parent < node:
            return
        else:
            self.cut_subtree(node)

    def delete(self, node):
        self.decrease_key(node, -math.inf)
        self.extract_min()

    def extract_min(self):
        if not self.head:
            print("Heap is empty")
            return None

        ch = self.current_min.child
        while ch:
            ch.parent = None
            tmp = ch.next
            ch.next = None
            self.rpush(ch)
            ch = tmp
        self.rmv_root(self.current_min)
        rslt = self.current_min
        if self.head:
            self.consolidate()
        return rslt

    def update_min(self, root):
        if not self.current_min:
            self.current_min = root
        else:
            self.current_min = min(self.current_min, root)

    def rmv_root(self, root):
        assert not root.parent
        self.N -= 1
        if self.head == self.tail == root:
            self.head = self.tail = None
        elif root == self.head:
            self.head = self.head.next
            self.head.prev = None
        elif root == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            root.prev.next = root.next
            root.next.prev = root.prev

    def rpush(self, root):
        self.update_min(root)
        if not self.head:
            self.head = root
            self.tail = root
        elif self.head == self.tail:
            self.tail = root
            self.head.next = self.tail
            self.tail.prev = self.head
        else:
            root.prev = self.tail
            self.tail.next = root
            self.tail = root

    def add_child(self, node1, node2):
        if node2 < node1:
            node1, node2 = node2, node1
        node2.next = node1.child
        node2.parent = node1
        if node1.child:
            node1.child.prev = node2
        node1.child = node2
        node1.degree += 1
        return node1

    def add_to_ptrs(self, ptrs, node):
        if not ptrs[node.degree]:
            ptrs[node.degree] = node
        else:
            assert ptrs[node.degree].degree == node.degree
            t = node.degree
            sm = self.add_child(ptrs[node.degree], node)
            ptrs[t] = None

            self.add_to_ptrs(ptrs, sm)

    def consolidate(self):
        N = self.N
        ptrs = [None for _ in range(N + 1)]
        while self.head:
            assert not self.head.parent
            tmp = self.head
            self.rmv_root(self.head)
            self.add_to_ptrs(ptrs, tmp)

        self.head, self.tail, self.N, self.current_min = (None, None, N, None)
        for ptr in ptrs:
            if ptr:
                ptr.next, ptr.prev, ptr.parent = None, None, None
                self.rpush(ptr)
