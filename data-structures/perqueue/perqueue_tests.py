import perqueue


def t1():
    queue = perqueue.perQueue()
    n = 1000
    expected = [i for i in range(n)]
    actual = []
    for i in range(n):
        queue.push(i, i)

    for i in range(n, 2 * n):
        actual.append(queue.pop(i).val)

    assert all(expected[i] == actual[i] for i in range(len(expected)))


def t2():
    q = perqueue.perQueue()
    q.push(0, 1)
    q.print(1)
    q.push(1, 2)
    q.print(2)
    q.push(2, 3)
    q.print(3)
    q.push(3, 4)  # 4th ver
    q.print(4)

    print(q.pop(1), q.pop(2), q.pop(3), q.pop(4))


t1()
t2()
