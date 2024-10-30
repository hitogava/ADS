import random
from treap import build, split, all


def split_test():
    def split_random():
        xs = sorted(random.randint(0, 1000) for _ in range(0, 1000))
        d = {x: random.randint(0, 1000) for x in xs}
        k = random.randint(0, 1000)
        root = build(d)
        t1, t2 = split(root, k)
        assert all(t1, lambda x: x.k < k)
        assert all(t2, lambda x: x.k >= k)

    for _ in range(100):
        split_random()

    d = {8: 10, 12: 8, 14: 14, 15: 4, 18: 9, 23: 6, 24: 15, 25: 11}
    root = build(d)
    t1, t2 = split(root, 20)


split_test()
