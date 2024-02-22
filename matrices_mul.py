import random, math, time
import table_formatter as tf


class Matrix:
    def printMatrix(self):
        for i in range(self.n):
            print(*self.values[i])
        print()

    def initWithRandom(self):
        self.values = [
            [random.randint(100, 1000) for _ in range(self.n)] for _ in range(self.n)
        ]

    def __init__(self, n):
        self.n = 2 ** math.ceil(math.log(n, 2))
        self.values = []
        self.initWithRandom()


def qubicMultiply(m1, m2, n):
    res = Matrix(n)
    for k in range(n):
        for i in range(n):
            s = 0
            for j in range(n):
                s += m1.values[k][j] * m2.values[j][i]
            res.values[k][i] = s
    return res


# isNeg means the secons parameter is negative (for subtraction)
def add(m1, m2, n, isNeg=False):
    res = Matrix(n)
    for i in range(n):
        for j in range(n):
            res.values[i][j] = m1.values[i][j] + (
                (-1 if isNeg else 1) * m2.values[i][j]
            )
    return res


#  0 | 1
# ---|---
#  2 | 3
def nQuater(matrix, size, n):
    res = Matrix(size // 2)
    # TODO:
    if n == 0:
        for i in range(size // 2):
            for j in range(size // 2):
                res.values[i][j] = matrix.values[i][j]
    elif n == 1:
        for i in range(size // 2):
            for j in range(size // 2):
                res.values[i][j] = matrix.values[i][size // 2 + j]
    elif n == 2:
        for i in range(size // 2):
            for j in range(size // 2):
                res.values[i][j] = matrix.values[size // 2 + i][j]
    elif n == 3:
        for i in range(size // 2):
            for j in range(size // 2):
                res.values[i][j] = matrix.values[size // 2 + i][size // 2 + j]
    return res


def buildMatrixFromQuotes(q0: Matrix, q1: Matrix, q2: Matrix, q3: Matrix, quoteSize):
    matrSize = quoteSize * 2
    res = Matrix(matrSize)
    for i in range(quoteSize):
        res.values[i] = q0.values[i] + q1.values[i]
    for i in range(quoteSize):
        res.values[quoteSize + i] = q2.values[i] + q3.values[i]
    return res


def recursiveMultiply(m1, m2, n):
    # TODO: n <= ?
    if n <= 16:
        return qubicMultiply(m1, m2, n)
    A = nQuater(m1, n, 0)
    B = nQuater(m1, n, 1)
    C = nQuater(m1, n, 2)
    D = nQuater(m1, n, 3)

    E = nQuater(m2, n, 0)
    F = nQuater(m2, n, 1)
    G = nQuater(m2, n, 2)
    H = nQuater(m2, n, 3)

    q1 = add(recursiveMultiply(A, E, n // 2), recursiveMultiply(B, G, n // 2), n // 2)
    q2 = add(recursiveMultiply(A, F, n // 2), recursiveMultiply(B, H, n // 2), n // 2)

    q3 = add(recursiveMultiply(C, E, n // 2), recursiveMultiply(D, G, n // 2), n // 2)
    q4 = add(recursiveMultiply(C, F, n // 2), recursiveMultiply(D, H, n // 2), n // 2)

    return buildMatrixFromQuotes(q1, q2, q3, q4, n // 2)


def StrassenAlgorithm(m1, m2, n):
    if n <= 16:
        return qubicMultiply(m1, m2, n)

    A = nQuater(m1, n, 0)
    B = nQuater(m1, n, 1)
    C = nQuater(m1, n, 2)
    D = nQuater(m1, n, 3)

    E = nQuater(m2, n, 0)
    F = nQuater(m2, n, 1)
    G = nQuater(m2, n, 2)
    H = nQuater(m2, n, 3)

    p = [
        0,
        StrassenAlgorithm(A, add(F, H, n // 2, True), n // 2),
        StrassenAlgorithm(add(A, B, n // 2), H, n // 2),
        StrassenAlgorithm(add(C, D, n // 2), E, n // 2),
        StrassenAlgorithm(D, add(G, E, n // 2, True), n // 2),
        StrassenAlgorithm(add(A, D, n // 2), add(E, H, n // 2), n // 2),
        StrassenAlgorithm(add(B, D, n // 2, True), add(G, H, n // 2), n // 2),
        StrassenAlgorithm(add(A, C, n // 2, True), add(E, F, n // 2), n // 2),
    ]
    # p5 + p4 - (p2 - p6)
    q1 = add(add(p[5], p[4], n // 2), add(p[2], p[6], n // 2, True), n // 2, True)
    q2 = add(p[1], p[2], n // 2)
    q3 = add(p[3], p[4], n // 2)
    # p1 + p5 - (p3 + p7)
    q4 = add(add(p[1], p[5], n // 2), add(p[3], p[7], n // 2), n // 2, True)

    return buildMatrixFromQuotes(q1, q2, q3, q4, n // 2)


def sampleMean(X_i, N):
    return (1 / N) * sum(X_i)


def geomMean(X_i, N):
    m = 1
    for x in X_i:
        m *= x
    return m ** (1 / N)


def standartDeviation(X_i, N):
    return ((1 / N) * sum((x_i - sampleMean(X_i, N)) ** 2 for x_i in X_i)) ** (1 / 2)


def benchmark(dataSet: (Matrix, Matrix), algorithm, N):
    results = []
    for i in range(N):
        st = time.perf_counter()
        algorithm(dataSet[0], dataSet[1], dataSet[0].n)
        end = time.perf_counter()
        results.append(end - st)
    sm = sampleMean(results, N)
    gm = geomMean(results, N)
    sd = standartDeviation(results, N)
    return [sm, gm, sd]


def genDataSet(k: int, n: int):
    testData = []
    for _ in range(k):
        testData.append((Matrix(n), Matrix(n)))
    return testData


algos = ["Qubic", "8 recursive calls", "Strassen"]

for _ in range(5):
    k = 3
    n = random.randint(200,250)
    dataSet = (Matrix(n), Matrix(n))
    print(f"Matrices {n} x {n}:")
    results = [
        benchmark(dataSet, qubicMultiply, k),
        benchmark(dataSet, recursiveMultiply, k),
        benchmark(dataSet, StrassenAlgorithm, k),
    ]

    tf.format_table(
        ["Sample mean", "Geometric mean", "Standart deviation"],
        algos,
        list(zip(results[0], results[1], results[2])),
    )
    print()
