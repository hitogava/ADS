def mergeStones(stones, k):
    n = len(stones)
    A = [[] for _ in range(n)]
    B = [0 for _ in range(n + 1)]

    if (n - 1) % (k - 1) != 0:
        return -1

    for i in range(n):
        A[i].extend([0 for _ in range(n)])

    for i in range(n):
        B[i + 1] = B[i] + stones[i]

    for l in range(k, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            A[i][j] = 10**6
            for m in range(i, j, k - 1):
                A[i][j] = min(A[i][j], A[i][m] + A[m + 1][j])
            if (l - 1) % (k - 1) == 0:
                A[i][j] += B[j + 1] - B[i]
    for i in range(n):
        print(A[i])

    return A[0][n - 1]
