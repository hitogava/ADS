class SegTree:
    def __init__(self, a):
        self.n = len(a)
        self.arr = a
        self.t = [0] * (4 * self.n)

    def update(self, idx, value):
        def update_helper(delta, v, tl, tr):
            if tl == tr:
                self.t[v] = value
                return
            tm = (tl + tr) >> 1
            self.t[v] += delta
            if idx <= tm:
                update_helper(delta, v * 2 + 1, tl, tm)
            else:
                update_helper(delta, v * 2 + 2, tm + 1, tr)

        update_helper(value - self.arr[idx], 0, 0, self.n - 1)
        self.arr[idx] = value

    def get_sum(self, l, r):
        def get_sum_helper(v, tl, tr, l, r):
            if tl == l and tr == r:
                return self.t[v]

            tm = (tl + tr) >> 1
            acc = 0
            if l <= tm:
                acc += get_sum_helper(v * 2 + 1, tl, tm, l, min(r, tm))
            if r > tm:
                acc += get_sum_helper(v * 2 + 2, tm + 1, tr, max(tm + 1, l), r)
            return acc

        return get_sum_helper(0, 0, self.n - 1, l, r)

    def gte(self, l, r, k):
        def lower_bound(arr, val):
            l, r = 0, len(arr)
            while l < r:
                m = (l + r) >> 1
                if val <= arr[m]:
                    r = m
                else:
                    l = m + 1
            return l

        def gte_helper(v, tl, tr, l, r):
            if l == tl and r == tr:
                return lower_bound(self.t[v], k)
            tm = (tl + tr) >> 1
            acc = 0
            if l <= tm:
                acc += gte_helper(v * 2 + 1, tl, tm, l, min(r, tm))
            if r > tm:
                acc += gte_helper(v * 2 + 2, tm + 1, tr, max(tm + 1, l), r)

            return acc

        return gte_helper(0, 0, self.n - 1, l, r)


def build(t):
    def build_helper(idx, tl, tr):
        if tl == tr:
            t.t[idx] = t.arr[tl]
            return
        tm = (tl + tr) >> 1
        build_helper(idx * 2 + 1, tl, tm)
        build_helper(idx * 2 + 2, tm + 1, tr)

        t.t[idx] = t.t[idx * 2 + 1] + t.t[idx * 2 + 2]

    build_helper(0, 0, t.n - 1)


def build_merge_sort_tree(t):
    def merge(left, right, result):
        lsize, rsize, n = len(left), len(right), len(result)
        i = j = k = 0
        while k < n and i < lsize and j < rsize:
            if left[i] < right[j]:
                result[k] = left[i]
                i += 1
            else:
                result[k] = right[j]
                j += 1
            k += 1

        while i < lsize:
            result[k] = left[i]
            k += 1
            i += 1

        while j < rsize:
            result[k] = right[j]
            k += 1
            j += 1

    def merge_sort(array, v, l, r):
        if l == r:
            t.t[v] = [array[l]]
            return [array[l]]
        m = (l + r) >> 1
        left = merge_sort(array, v * 2 + 1, l, m)
        right = merge_sort(array, v * 2 + 2, m + 1, r)
        merged = [0] * (r - l + 1)
        merge(left, right, merged)
        t.t[v] = merged
        return merged

    t.arr = merge_sort(t.arr, 0, 0, t.n - 1)


# a = [46, 11, 40, 8, 2, 42, 65, 10]
nums = [5, 2, 6, 1]
t = SegTree(nums)
build_merge_sort_tree(t)
counts = [0] * len(nums)
for i in range(len(nums) - 1):
    counts[i] = t.gte(i + 1, len(nums) - 1, nums[i])
print(counts)
