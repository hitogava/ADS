primes = [2, 3, 7, 13, 31, 61, 127, 251, 509, 1021, 2039, 4093, 8191, 16381, 32749, 65521, 131071, 262139, 524287, 1048573, 2097143, 4194301, 8388593, 16777213, 33554393, 67108859, 134217689, 268435399, 536870909, 1073741789, 2147483647, 4294967291, 8589934583]

def binpower(base, ex, mod):
    result = 1
    base %= mod
    while ex:
        if ex & 1:
            result = result * base % mod
        base = base * base % mod
        ex >>= 1
    return result

def is_composite(n, a, d, s):
    x = binpower(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(1, s):
        x = x * x % n
        if x == n - 1:
            return False
    return True

# a^(n-1) === 1 mod n <=> (a^(2^s * d) - 1) == 0
def MillerRabin(n):
    if n < 4:
        return n == 2 or n == 3
    r = 0
    d = n - 1
    while (d & 1) == 0:
        d >>= 1
        r += 1
    for base in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n == base:
            return True
        if is_composite(n, base, d, r):
            return False
    return True
