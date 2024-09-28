class DisjointSet:
    def __init__(self, init_n) -> None:
        self.elements = [i for i in range(init_n)]
        self.sizes = [1 for _ in range(init_n)]

    def union(self, p1, p2):
        if self.sizes[p1] < self.sizes[p2]:
            self.sizes[p2] += self.sizes[p1]
            self.elements[p1] = p2
        else:
            self.sizes[p1] += self.sizes[p2]
            self.elements[p2] = p1

    def find(self, x):
        if self.elements[x] == x:
            return self.elements[x]
        return self.find(self.elements[x])

    def print(self):
        p_map = {}
        for i in range(len(self.elements)):
            p = self.find(i)
            if p not in p_map:
                p_map[p] = []
            p_map[p].append(i)
        print(p_map)


edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
init_n = len(edges) + 1
ds = DisjointSet(init_n)

for fr, to in edges:
    p1, p2 = ds.find(fr), ds.find(to)
    if p1 != p2:
        ds.union(p1, p2)
    else:
        print(fr, to)
        break
