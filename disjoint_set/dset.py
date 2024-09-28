class DisjointSet:
    def __init__(self, init_n) -> None:
        self.xs = [i for i in range(init_n)]
        self.rank = [0 for _ in range(init_n)]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)

        if self.rank[px] < self.rank[py]:
            self.xs[px] = self.xs[py]
        else:
            self.xs[py] = self.xs[px]
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1

    def find(self, x):
        if self.xs[x] == x:
            return self.xs[x]
        self.xs[x] = self.find(self.xs[x])
        return self.xs[x]

    def display(self):
        p_map = {}
        for i in range(len(self.xs)):
            p = self.find(i)
            if p not in p_map:
                p_map[p] = []
            p_map[p].append(i)
        print(p_map)
        for k in p_map.keys():
            print(f"{k}: {self.rank[k]}")
