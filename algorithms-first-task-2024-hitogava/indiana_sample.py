from bheap import BinHeap
from fheap import HeapNode, FibHeap, GNode
from typing import Any
import sys, math


def Dijkstra(nodes, p) -> Any:
    result = -math.inf
    entry_finder = {}
    heap = FibHeap()
    for k, node in nodes.items():
        entry_finder[node] = heap.insert(node)
    while not heap.empty():
        u = heap.extract_min().content
        for v, weight in u.adj:
            if u.d + weight < v.d:
                v.d = u.d + weight
                heap.decrease_key(entry_finder[v], v.d)
    for node in nodes.items():
        gnode = node[1]
        if gnode.d <= p:
            result = max(result, gnode.tr)
    return result


def solution(data: str) -> int:
    sdata = data.split("\n")
    p, n, m = map(int, sdata[0].split())
    nodes = {}
    nodes[0] = GNode(0, 0, 0)
    for i in range(1, n):
        nodes[i] = GNode(math.inf, i)
    for i in range(1, m + 1):
        fr, to, w = map(int, sdata[i].split())
        nodes[fr].adj.append((nodes[to], w))
        nodes[to].adj.append((nodes[fr], w))
    for i in range(n):
        nodes[i].tr = int(sdata[m + 1 + i])
    return Dijkstra(nodes, p)


def run():
    if len(sys.argv) <= 2:
        print("Wrong number of arguments: please specify input and output files.")
        return

    input_name, output_name = sys.argv[1], sys.argv[2]
    with open(input_name, "r") as inp:
        with open(output_name, "w") as out:
            data = inp.read()
            result = solution(data)
            out.write(str(result))


run()
