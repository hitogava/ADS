from itertools import permutations, product


def tsp_dfs_naive(graph, start, n) -> int:
    def dfs(v, colors, path, ans, acc):
        nonlocal graph
        colors[v] = 1
        for u, w in graph[v]:
            if colors[u] == 0:
                dfs(u, [c for c in colors], path + [u], ans, acc + w)
            if colors[u] == 1 and u == path[0] and len(path) == n:
                ans.append(acc + w)

        colors[v] = 2
        return ans

    colors = [0 for _ in range(n + 1)]
    return min(dfs(1, colors, [start], [], 0))


def tsp_perms_naive(graph):
    n = len(graph)
    perms = permutations(range(n))
    ans = 10**6
    for p in perms:
        ans = min(ans, sum(graph[p[i]][p[(i + 1) % n]] for i in range(n)))
    return ans


def tsp(graph):
    n = len(graph) + 1
    m = 2 ** (n - 1)
    a = [[10**6 for _ in range(n)] for _ in range(m)]
    a[1][1] = 0

    sets = {i: [] for i in range(n)}
    for p in product([0, 1], repeat=n - 1):
        x = 0
        for i in range(len(p)):
            x += p[len(p) - i - 1] * 2**i
        sets[p.count(1)].append(x)

    for length, ss in sets.items():
        if length < 2:
            continue
        for s in ss:
            if s & 1 == 0:
                continue
            for v in range(1, n):
                if s & (1 << v) == 0:
                    continue
                mincost = 10**6
                for w in range(n):
                    if s & (1 << w) == 0 or w == v:
                        continue
                    mincost = min(mincost, a[s & ~(1 << v)][w + 1] + graph[w][v])
                a[s][v + 1] = mincost

    res = 10**6
    for v in range(1, n - 1):
        res = min(res, a[m - 1][v + 1] + graph[v][0])
    return res
