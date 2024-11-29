from tsp import tsp_dfs_naive, tsp_perms_naive, tsp
from math import inf
from random import randint


def test():
    for i in range(1, 30):
        graph = [[0 if k == j else randint(1, 9) for k in range(i)] for j in range(i)]
        print(i, tsp(graph))


test()
