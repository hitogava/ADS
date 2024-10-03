import dset


def parse(data):
    data = data.split("\n")
    arr = [("", 0, 0) for _ in range(len(data))]
    for i in range(len(data)):
        ch, d, p = data[i].split(" ")
        arr[i] = (ch, int(d), int(p))
    return arr


def solution(data) -> str:
    arr = parse(data)
    n = len(arr)
    chmap = {}
    ds = dset.DisjointSet(n + 1)
    for i in range(n):
        if arr[i][0] not in chmap:
            chmap[arr[i][0]] = i + 1
            chmap[i + 1] = arr[i][0]

    tasks = [-1 for _ in range(n + 1)]
    tails = [i for i in range(n + 1)]
    xs = [-1 for _ in range(n + 1)]

    for ch, d, _ in arr:
        if tasks[d] == -1 and ds.find(d) == d:
            tasks[d] = d
            tails[d] = tails[d] - 1 if tails[d] != 1 else n
            ds.union(d, tails[d])
            xs[d] = chmap[ch]
        else:
            parent = ds.find(d)
            tasks[tails[parent]] = d
            xs[tails[parent]] = chmap[ch]

            if tails[parent] == 1:
                tails[parent] = n
            else:
                tails[parent] -= 1

            ds.union(tails[parent], parent)
            tails[parent] = tails[tails[parent]]

    return "".join([chmap[x] for x in xs if x != -1])
