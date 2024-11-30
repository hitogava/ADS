from tsp import tsp_perms_naive, tsp
from math import inf
from random import randint


def test():
    for i in range(2, 10 + 1):
        graph = [
            [0 if k == j else randint(1, 1000) for k in range(i)] for j in range(i)
        ]
        assert tsp_perms_naive(graph) == tsp(graph)
test()
