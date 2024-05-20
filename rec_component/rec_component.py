import sys, collections

# functions hash table
f_ht = {}


def reverse_graph(g):
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            g[i][j], g[j][i] = g[j][i], g[i][j]


def adj(u, g):
    return [i for i in range(len(g)) if g[u][i]]

def is_adj(u, v, g):
    return g[u][v] == 1


def has_cycle(src, curr, visited, g):
    visited[curr] = 1
    for u in adj(curr, g):
        if u == src:
            return True
        if visited[u]:
            continue
        if has_cycle(src, u, visited, g):
            return True
    return False


def get_func_by_val(val):
    return list(f_ht.keys())[list(f_ht.values()).index(val)]


def find_recursive_components(g):
    n = 0
    dq = collections.deque()
    recursives = [0 for _ in range(len(g))]

    def DFS(v, visited, scc, g):
        nonlocal n, dq, recursives
        visited[v] = 1
        if scc is not None:
            scc.append(v)
            recursives[v] = 1
        for u in adj(v, g):
            if visited[u]:
                continue
            DFS(u, visited, scc, g)
        dq.appendleft(v)

    rec_components = []
    visited = [0 for _ in range(len(g))]
    reverse_graph(g)
    for i in range(len(g)):
        if not visited[i]:
            DFS(i, visited, None, g)

    reverse_graph(g)
    visited = [0 for _ in range(len(g))]
    scc = []
    for v in list(dq):
        if not visited[v]:
            DFS(v, visited, scc, g)
            if len(scc) == 1 and not is_adj(scc[0], scc[0], g):
                recursives[scc[0]] = 0
            rec_components.append(scc)
            scc = []

    return (rec_components, recursives)


def create_adj_matrix(data, n):
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(len(data)):
        v, adj = data[i].split(": ")
        if not v in f_ht:
            f_ht[v] = len(f_ht.keys())
        for u in adj.split(", "):
            if not u in f_ht:
                f_ht[u] = len(f_ht.keys())
            adj_matrix[f_ht[v]][f_ht[u]] = 1
    return adj_matrix


input_name = sys.argv[1]
graph = None
with open(input_name, "r") as inp:
    data = [x[:-1] for x in inp.readlines()]
    n = int(data[0])
    graph = create_adj_matrix(data[1:], n)
    components, recursives = find_recursive_components(graph)
    for i in range(len(recursives)):
        if recursives[i]:
            print(f"{get_func_by_val(i)} is recursive")
        else:
            print(f"{get_func_by_val(i)} is not recursive")
