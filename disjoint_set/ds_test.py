from dset import DisjointSet
import math

def test1():
    n = 10
    ds = DisjointSet(n)
    for i in range(n):
        ds.union(0, i)

    assert ds.rank[0] == 1
    for i in range(n):
        assert ds.find(i) == 0

def test2():
    n = 10
    ds = DisjointSet(n)
    for k in range(1, math.ceil(math.log2(n))):
        for i in range(0, n - 1, 2**k):
            if i + 2 ** (k - 1) < n:
                ds.union(i, i + 2 ** (k - 1))

    assert ds.find(7) == 0
    assert ds.xs[7] == 0
    assert ds.xs[6] == 0

    assert ds.find(3) == 0
    assert ds.xs[3] == 0

    assert ds.rank[0] == math.floor(math.log2(n))

def test3():
    n = 20
    ds = DisjointSet(n)
    for i in range(n - 1):
        ds.xs[i + 1] = ds.xs[i]

    ds.find(n - 1)
    assert all(x == 0 for x in ds.xs)
