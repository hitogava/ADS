import sys, collections

# functions hash table
f_ht = {}


def reverse_graph(g):
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            g[i][j], g[j][i] = g[j][i], g[i][j]


def adj(u, g):
    return [i for i in range(len(g)) if g[u][i]]


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


def is_recursive(g, func):
    v = f_ht[func]
    visited = [0 for _ in range(len(g))]
    return has_cycle(v, v, visited, g)


def print_recursive_functions():
    for func in f_ht.keys():
        if is_recursive(graph, func):
            print(f"{func} is recursive")
        else:
            print(f"{func} is not recursive")

def get_func_by_val(val):
    return list(f_ht.keys())[list(f_ht.values()).index(val)]

def find_recursive_components(g):
    n = 0
    dq = collections.deque()

    def DFS(v, visited, scc, g):
        nonlocal n, dq
        visited[v] = 1
        if scc is not None:
            scc.append(v)
        for u in adj(v, g):
            if visited[u]:
                continue
            DFS(u, visited, scc, g)
        dq.appendleft(v)

    max_rec_comp = []
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
            max_rec_comp = max(scc, max_rec_comp, key=len)
            scc = []

    return max_rec_comp


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

print([get_func_by_val(x) for x in find_recursive_components(graph)])
