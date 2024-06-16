from typing import Optional
from enum import Enum


class RotateDir(Enum):
    LEFT = 0
    RIGHT = 1


class Node:
    def __init__(self, key, value, twin=None, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.size = 1
        self.height = 1
        self.diff = 0
        self.left = left
        self.right = right
        self.parent = parent
        self.twin = twin

    def update(self):
        lh = 0 if not self.left else self.left.height
        rh = 0 if not self.right else self.right.height

        self.height = max(lh, rh) + 1
        self.diff = rh - lh

        ls = 0 if not self.left else self.left.size
        rs = 0 if not self.right else self.right.size

        self.size = ls + rs + 1

    def __eq__(self, other) -> bool:
        return self.key == other.key

    def __gt__(self, other) -> bool:
        return self.key > other.key

    def __lt__(self, other) -> bool:
        return self.key < other.key

    def __ge__(self, other) -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __str__(self) -> str:
        return f"{self.key}"


class AVLTree:
    def __init__(self, root: Optional[Node]):
        self.root = root

    def avl_invariant(self, root):
        return abs(root.diff) <= 1

    def find(self, root, value):
        if not root:
            return None
        if root.key == value:
            return root
        if value > root.key:
            return self.find(root.right, value)
        return self.find(root.left, value)

    def rotate(self, node, direction: RotateDir):
        new_root = node.right if direction == RotateDir.LEFT else node.left
        if direction == direction.LEFT:
            self.rmv_child(node, node.right)
        else:
            self.rmv_child(node, node.left)
        if self.root is node:
            self.root = new_root
        if node.parent:
            self.add_child(node.parent, new_root)

        if direction == RotateDir.LEFT:
            self.add_child(node, new_root.left)
        else:
            self.add_child(node, new_root.right)
        self.add_child(new_root, node)
        node.update()
        new_root.update()

    def big_rotate(self, node, direction: RotateDir):

        if direction == RotateDir.LEFT:
            self.rotate(node.right, RotateDir.RIGHT)
        else:
            self.rotate(node.left, RotateDir.LEFT)
        self.rotate(node, direction)

    def rank(self, root, node, rsum=0):
        not_equals = 0
        if root.right:
            not_equals += root.right.size
            if node == root.right:
                not_equals -= 1
            if root.right.left and root.right.left == node:
                not_equals -= 1

        if root is node:
            return rsum + not_equals

        if node < root or (node == root and node.value > root.value):
            return self.rank(root.left, node, rsum + not_equals + int(node != root))
        return self.rank(root.right, node, rsum)

    def topn(self, n, root=None):
        cnt = 0
        if not root:
            root = self.root

        def topn_helper(root, n):
            nonlocal cnt
            if not root:
                return
            if cnt < n:
                yield from topn_helper(root.right, n)
            if cnt < n:
                yield root
            cnt += 1
            if cnt < n:
                yield from topn_helper(root.left, n)

        yield from topn_helper(root, n)

    def range(self, root, lower, upper):
        if not root:
            return
        if root.key <= upper:
            yield from self.range(root.right, lower, upper)
        if lower <= root.key <= upper:
            yield root
        if root.key >= lower:
            yield from self.range(root.left, lower, upper)

    def add_child(self, parent, child):
        if not child:
            return
        child.parent = parent
        if not parent:
            return
        if (child > parent) or (child == parent and child.value < parent.value):
            parent.right = child
        elif (child < parent) or (child == parent and child.value > parent.value):
            parent.left = child

    def rmv_child(self, parent, child):
        if not (parent and child):
            return
        child.parent = None
        if parent.left and parent.left is child:
            parent.left = None
        elif parent.right is child:
            parent.right = None

    def swap_nodes(self, n1, n2):
        if n1.parent:
            if n1 is n1.parent.left:
                n1.parent.left = n2
            else:
                n1.parent.right = n2
        if n2.parent:
            if n2 is n2.parent.left:
                n2.parent.left = n1
            else:
                n2.parent.right = n1
        n1.parent, n2.parent = n2.parent, n1.parent

        if n1.left:
            n1.left.parent = n2
        if n1.right:
            n1.right.parent = n2

        if n2.left:
            n2.left.parent = n1
        if n2.right:
            n2.right.parent = n1

        n1.left, n2.left = n2.left, n1.left
        n1.right, n2.right = n2.right, n1.right

    def prep_for_insert(self, root, node):
        if node > root or (node == root and node.value < root.value):
            if not root.right:
                root.size += 1
                self.add_child(root, node)
                return
            self.prep_for_insert(root.right, node)
        elif node < root or (node == root and node.value > root.value):
            if not root.left:
                root.size += 1
                self.add_child(root, node)
                return
            self.prep_for_insert(root.left, node)

    def get_leftmost(self, root):
        if not root.left:
            return root
        return self.get_leftmost(root.left)

    def remove(self, node):
        nparent = node.parent
        balance_from = nparent
        if not node.left and not node.right:
            if node is self.root:
                self.root = None
                return
            self.rmv_child(node.parent, node)
        elif node.left and node.right:
            nroot = self.get_leftmost(node.right)
            if node is self.root:
                self.root = nroot

            self.swap_nodes(node, nroot)
            balance_from = node.parent
            self.remove(node)
        else:
            child = node.left if node.left else node.right
            if node is self.root:
                self.root = child
            self.rmv_child(nparent, node)
            self.add_child(nparent, child)

        self.balance(balance_from)

    def balance(self, node):
        if not node:
            return
        node.update()
        if not self.avl_invariant(node):
            if node.diff == 2:
                if node.right and (node.right.diff == 0 or node.right.diff == 1):
                    self.rotate(node, RotateDir.LEFT)
                elif node.right and node.right.diff == -1:
                    self.big_rotate(node, RotateDir.LEFT)
            if node.diff == -2:
                if node.left and (node.left.diff == 0 or node.left.diff == -1):
                    self.rotate(node, RotateDir.RIGHT)
                elif node.left and node.left.diff == 1:
                    self.big_rotate(node, RotateDir.RIGHT)
        self.balance(node.parent)

    def insert(self, node):
        if not self.root:
            self.root = node
            return node
        self.prep_for_insert(self.root, node)
        self.balance(node)
        return node


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
            valstr = str(n[0].key) + f"({n[0].twin.key})"
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
