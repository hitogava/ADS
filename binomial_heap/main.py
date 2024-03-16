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


def decrease_heap_k(heap):
    bot_it = heap
    while bot_it:
        right_it = bot_it
        while right_it:
            right_it.k -= 1
            right_it = right_it.right
        bot_it = bot_it.left_child


def remove_parents(head):
    while head:
        head.parent = None
        head = head.right


def merge_trees(t1: BinomialTreeNode, t2: BinomialTreeNode):
    new_tree = BinomialTreeNode()
    if t1.priority < t2.priority:
        new_tree = deepcopy(t1)
        new_tree.k += 1
        t2.right = new_tree.left_child
        t2.parent = new_tree
        new_tree.left_child = t2
    else:
        new_tree = deepcopy(t2)
        new_tree.k += 1
        t1.right = new_tree.left_child
        t1.parent = new_tree
        new_tree.left_child = t1
    return new_tree


def get_tail(heap):
    i = heap
    while i:
        if not i.right:
            return i
        i = i.right
    return None


def get_max_k(heap):
    m = -1
    while heap:
        m = max(m, heap.k)
        heap = heap.right
    return m


def merge_heaps(h1: BinomialTreeNode, h2: BinomialTreeNode):
    merged_head = None
    carry = None

    # h1_tail = get_tail(h1)
    # h2_tail = get_tail(h2)
    h1_k = get_max_k(h1)
    h2_k = get_max_k(h2)

    if not h1 and h2:
        maxk = h2_k
    elif not h2 and h1:
        maxk = h1_k
    elif h1 and h2:
        maxk = max(h1_k, h2_k)
    else:
        return None

    t1 = [None] * (maxk + 1)
    t2 = [None] * (maxk + 1)

    it = h1

    while it:
        t1[it.k] = it
        it = it.right

    it = h2
    while it:
        t2[it.k] = it
        it = it.right

    # TODO:
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
    merged_tail = None
    for root in roots:
        if root:
            root.right = None
            if merged_head:
                merged_tail.right = root
            else:
                merged_head = root
            merged_tail = root
    return merged_head


def insert(heap, priority, value):
    return merge_heaps(heap, BinomialTreeNode(priority, value))


def peek_min(heap):
    min_r = 10**6
    result_node = None
    while heap:
        if heap.priority < min_r:
            min_r = heap.priority
            result_node = heap
        heap = heap.right
    return result_node


def extract_min(heap):
    root = heap
    m = peek_min(heap)
    remove_parents(m.left_child)
    if m == heap:
        return merge_heaps(heap.right, m.left_child)
    while heap:
        if heap.right == m:
            heap.right = m.right
            break
        heap = heap.right
    return merge_heaps(root, m.left_child)


def print_tree_roots(heap):
    print("Tree roots:")
    while heap:
        print(heap)
        heap = heap.right

def print_heap(heap):
    root_iter = heap
    while root_iter:
        print(f"K: {root_iter.k}, p: {root_iter.priority}")
        children_iter = root_iter.left_child
        while children_iter:
            n_iter = children_iter
            while n_iter:
                print(n_iter.priority, end=' ')
                n_iter = n_iter.right
            children_iter = children_iter.left_child
            print()
        root_iter = root_iter.right



heap = BinomialTreeNode(-1)
for i in range(15):
    # TODO:
    heap = insert(heap, i, 0)
print_heap(heap)
# print("Min:", peek_min(heap))
# heap = extract_min(heap)
# # print("---")
# print_heap(heap)
# for i in range(20, 30):
#     # TODO:
#     heap = insert(heap, i, 0)
# print_heap(heap)
# print("Min:", peek_min(heap))
