class DisjointSet:
    def __init__(self, init_n) -> None:
        self.elements = [i for i in range(init_n)]
        self.rank = [0 for _ in range(init_n)]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)

        if self.rank[px] < self.rank[py]:
            self.elements[px] = self.elements[py]
        else:
            self.elements[py] = self.elements[px]
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1

    def find(self, x):
        if self.elements[x] == x:
            return self.elements[x]
        self.elements[x] = self.find(self.elements[x])
        return self.elements[x]

    def display(self):
        p_map = {}
        for i in range(len(self.elements)):
            p = self.find(i)
            if p not in p_map:
                p_map[p] = []
            p_map[p].append(i)
        print(p_map)
        for k in p_map.keys():
            print(f"{k}: {self.rank[k]}")

n = 10
ds = DisjointSet(n)
for i in range(5):
    ds.union(0, i)

for i in range(5, 10):
    ds.union(5, i)

ds.union(0, 5)

for i in range(n):
    print(i, ds.elements[i])
