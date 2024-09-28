from typing import Any


class MyT:
    def __init__(self, priority=0, value=0) -> None:
        self.p = priority
        self.val = value

    def __str__(self):
        return f"{self.p}, {self.val}"


class BinaryHeap:
    def __init__(self) -> None:
        self.heap = []
        self.entry_finder = {}

    def __str__(self):
        res = ""
        for i in range(len(self.heap)):
            res += f"{self.heap[i].p}, {self.heap[i].val}\n"
        return res[:-1]

    def check_invariant(self):
        n = len(self.heap)
        for i in range((n - 1) // 2 + 1):
            if 2 * i + 1 < n and self.heap[i].p > self.heap[2 * i + 1].p:
                return False
            if 2 * i + 2 < n and self.heap[i].p > self.heap[2 * i + 2].p:
                return False
        return True

    def sift_up(self, i):
        while i > 0 and self.heap[(i - 1) // 2].p > self.heap[i].p:
            parent, act = self.heap[(i - 1) // 2], self.heap[i]

            self.entry_finder[parent.val], self.entry_finder[act.val] = (
                self.entry_finder[act.val],
                self.entry_finder[parent.val],
            )

            self.heap[(i - 1) // 2], self.heap[i] = (
                self.heap[i],
                self.heap[(i - 1) // 2],
            )
            i = (i - 1) // 2

    def sift_down(self, i):
        n = len(self.heap)
        while i <= (n - 1) // 2 - (n % 2):
            min_child_i = 2 * i + 1
            if 2 * i + 2 < n and self.heap[2 * i + 2].p < self.heap[2 * i + 1].p:
                min_child_i = 2 * i + 2
            if self.heap[i].p > self.heap[min_child_i].p:
                # updating map of entries
                (
                    self.entry_finder[self.heap[i].val],
                    self.entry_finder[self.heap[min_child_i].val],
                ) = (
                    self.entry_finder[self.heap[min_child_i].val],
                    self.entry_finder[self.heap[i].val],
                )
                self.heap[i], self.heap[min_child_i] = (
                    self.heap[min_child_i],
                    self.heap[i],
                )
            i = min_child_i

    def insert(self, priority: Any, value: Any) -> None:
        t = MyT(priority, value)
        self.heap.append(t)
        self.entry_finder[value] = len(self.heap) - 1
        self.sift_up(len(self.heap) - 1)

    def peek_min(self) -> Any:
        return self.heap[0]

    def swp_nodes(self, node1, node2):
        i, j = self.entry_finder[node1.val], self.entry_finder[node2.val]
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.entry_finder[node1.val], self.entry_finder[node2.val] = (
            self.entry_finder[node2.val],
            self.entry_finder[node1.val],
        )

    def extract_min(self):
        if len(self.heap) == 0:
            print("Heap is empty")
            return None
        ret = self.heap[0]
        self.swp_nodes(self.peek_min(), self.heap[-1])
        self.entry_finder[ret.val] = -1
        self.heap = self.heap[:-1]
        self.sift_down(0)
        return ret

    def decrease_key(self, s, p) -> Any:
        i = self.entry_finder[s]
        # need to delete
        if self.entry_finder[s] == -1:
            print("Access to extracted node")
        if i >= len(self.heap):
            print("Index is out of boundary")
            return None
        elif self.heap[i].p <= p:
            print("New priority should be less than actual")
            return None
        self.heap[i].p = p
        return self.sift_up(i)

    def empty(self):
        return len(self.heap) == 0
