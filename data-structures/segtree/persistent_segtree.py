def print_tree(root):
    def height(root):
        return 1 + max(height(root.left), height(root.right)) if root else -1

    nlevels = height(root)
    width = pow(2, nlevels + 1)

    q = [(root, 0, width, "c")]
    levels = []

    while q:
        node, level, x, align = q.pop(0)
        if node:
            if len(levels) <= level:
                levels.append([])

            levels[level].append([node, level, x, align])
            seg = width // (pow(2, level + 1))
            q.append((node.left, level + 1, x - seg, "l"))
            q.append((node.right, level + 1, x + seg, "r"))

    for i, l in enumerate(levels):
        pre = 0
        preline = 0
        linestr = ""
        pstr = ""
        seg = width // (pow(2, i + 1))
        for n in l:
            # valstr = str(n[0].key) + f"({n[0].key},{n[0].height},{n[0].size})"
            valstr = f"{str(n[0].value)} ({n[0].alives})"
            if n[3] == "r":
                linestr += (
                    " " * (n[2] - preline - 1 - seg - seg)
                    + "¯" * (seg + seg // 2)
                    + "\\"
                )
                preline = n[2]
            if n[3] == "l":
                linestr += " " * (n[2] - preline - 1) + "/" + "¯" * (seg + seg // 2)
                preline = n[2] + seg + seg // 2
            pstr += " " * (n[2] - pre - len(valstr)) + valstr
            pre = n[2]
        print(linestr)
        print(pstr)


class segnode:
    def __init__(self, value, alives=0, left=None, right=None, parent=None):
        self.value = value
        self.alives = alives
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f"{self.value}, {self.alives}"


def find(node, idx, tl, tr):
    if tl == tr:
        return node
    tm = (tl + tr) >> 1
    if idx <= tm:
        return find(node.left, idx, tl, tm)
    return find(node.right, idx, tm + 1, tr)


def update(root, array, idx, value):
    def update_helper(delta, node, tl, tr):
        if tl == tr:
            node.value = value
            return
        tm = (tl + tr) >> 1
        node.value += delta
        if idx <= tm:
            update_helper(delta, node.left, tl, tm)
        else:
            update_helper(delta, node.right, tm + 1, tr)

    update_helper(value - array[idx], root, 0, len(array) - 1)
    array[idx] = value


def query(root, n, l, r, alives=False):
    def get_sum_helper(node, tl, tr, l, r):
        if tl == l and tr == r:
            if alives:
                return node.alives
            return node.value

        tm = (tl + tr) >> 1
        acc = 0
        if l <= tm:
            acc += get_sum_helper(node.left, tl, tm, l, min(r, tm))
        if r > tm:
            acc += get_sum_helper(node.right, tm + 1, tr, max(tm + 1, l), r)
        return acc

    return get_sum_helper(root, 0, n - 1, l, r)


def reincarnate(curr, tl, tr, l, r):
    def reincarnated(dead):
        return segnode(dead.value, dead.alives + 1, dead.left, dead.right, dead.parent)

    if tl == l and tr == r:
        return reincarnated(curr)

    newnode = reincarnated(curr)
    tm = (tl + tr) >> 1
    if l <= tm:
        newnode.left = reincarnate(curr.left, tl, tm, l, min(r, tm))
    if r > tm:
        newnode.right = reincarnate(curr.right, tm + 1, tr, max(tm + 1, l), r)

    return newnode


def lower_bound(arr, val):
    l, r = 0, len(arr)
    while l < r:
        m = (l + r) >> 1
        if val <= arr[m]:
            r = m
        else:
            l = m + 1
    return l


from bisect import bisect_left
from random import randint


def gte(root: segnode, array, l, r, k):
    roots = [root]
    sorted_array = sorted(
        [(i, el) for i, el in enumerate(array)], key=lambda x: x[1], reverse=True
    )
    ver = 0
    for idx, _ in sorted_array:
        roots.append(reincarnate(roots[-1], 0, len(array) - 1, idx, idx))
        ver += 1

    sorted_array = [x for _, x in sorted_array[::-1]]
    ver = len(a) - (bisect_left(sorted_array, k))
    return query(roots[ver], len(array), l, r, True)


def build(array):
    def build_helper(tl, tr):
        if tl == tr:
            return segnode(array[tl])
        tm = (tl + tr) >> 1
        left = build_helper(tl, tm)
        right = build_helper(tm + 1, tr)

        root = segnode(left.value + right.value, left=left, right=right)
        left.parent = root
        right.parent = root
        return root

    return build_helper(0, len(array) - 1)


a = [46, 11, 40, 8, 2, 42, 65, 10]
print(sorted(a))
root = build(a)
for sz in range(1, 20):
    a = [randint(0, 1000) for _ in range(sz)]
    root = build(a)
    for m in range(1, len(a) + 1):
        k = randint(0, 100)
        for i in range(len(a) - m + 1):
            j = i + m - 1
            assert gte(root, a, i, j, k) == len([x for x in a[i : j + 1] if x >= k])
