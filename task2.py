import random


def mul(x, y):
    n, m = len(str(abs(x))), len(str(abs(y)))
    if n == 1 and m == 1:
        return x * y
    pivot = max(n, m) // 2
    a = x // 10 ** pivot
    c = y // 10 ** pivot
    b = x % 10 ** pivot
    d = y % 10 ** pivot
    s1 = mul(a, c)
    s2 = mul(b, d)
    s3 = mul(a + b, c + d)
    s4 = s3 - s1 - s2
    return (10 ** (2 * pivot)) * s1 + (10 ** pivot) * s4 + s2


cases = [
    (mul(0, 0), 0),
    (mul(3, 0), 0),
    (mul(0, 3), 0),
    (mul(1234, 5678), 1234 * 5678),
    (mul(1234, 5), 1234 * 5),
    (mul(5, 1234), 1234 * 5),
    (mul(1234, 56), 1234 * 56),
    (mul(56, 1234), 1234 * 56),
    (mul(1234, 567), 1234 * 567),
    (mul(567, 1234), 1234 * 567),
    (mul(-567, 1234), 1234 * (-567)),
    (mul(567, -1234), 1234 * (-567)),
    (mul(-567, -1234), 1234 * 567),
]


def run_tests():
    for c in cases:
        assert (c[0] == c[1])
    # Test on some randomized values
    for i in range(1000):
        x, y = random.randint(-10_000, 100_000_000), random.randint(-10_000, 100_000_000)
        assert (mul(x, y) == x * y)


run_tests()
