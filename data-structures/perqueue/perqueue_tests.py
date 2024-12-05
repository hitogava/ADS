import perqueue


def t1():
    queue = perqueue.perQueue()
    n = 100
    expected = [i + 1 for i in range(n)]
    actual = []
    for i in range(n):
        queue.push(i, i + 1)

    for i in range(n, 2 * n):
        actual.append(queue.pop(i).val)

    assert all(expected[i] == actual[i] for i in range(len(expected)))


def t2():
    q = perqueue.perQueue()
    q.push(0, 1)
    q.push(1, 2)
    q.push(2, 3)
    q.push(3, 4)  # 4th ver

    print(q.pop(1), q.pop(2), q.pop(3), q.pop(4))
    print(q.pop(5), q.pop(6), q.pop(7), q.pop(8))
    print(q.pop(9), q.pop(10), q.pop(11), q.pop(12))
    print(q.pop(13), q.pop(14), q.pop(15), q.pop(16))

    print(q.pop(1), q.pop(2), q.pop(3), q.pop(4))
    print(q.pop(5), q.pop(6), q.pop(7), q.pop(8))
    print(q.pop(9), q.pop(10), q.pop(11), q.pop(12))
    print(q.pop(13), q.pop(14), q.pop(15), q.pop(16))

    q.push(6, 228)
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))

    q.push(7, 42)
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))

    q.push(8, 21)
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))
    print(q.pop(len(q.queue) - 1))

    for i in range(100):
        q.push(len(q.queue) - 1, i * 2)

    for i in range(100):
        print(q.pop(len(q.queue) - 1))

t1()
t2()
