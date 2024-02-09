import random, math


def skip_leading_zeros(x: str):
    i = 0
    while i < len(x):
        if x[i] == '1':
            return i
        i += 1
    return i - 1


def is_zero(x):
    return all(c == '0' for c in x)


def add(x, y, bits):
    res = ""
    carry = 0
    x = x.zfill(bits)
    y = y.zfill(bits)
    for i in range(1, bits + 1):
        t = int(x[-i]) + int(y[-i]) + carry
        res += str(t % 2)
        carry = t // 2
    res = res[::-1]
    return res[skip_leading_zeros(res):]


def make_negative(x, bits):
    res = ""
    x = x.zfill(bits)
    for i in range(bits):
        res += '1' if x[i] == '0' else '0'
    res = add(res, "1".zfill(bits), bits)
    return res


def sub(x, y, bits):
    return add(x, make_negative(y, bits), bits)


def mul(x, y, bits):
    ret = '0' * bits
    x = x.zfill(bits)
    y = y.zfill(bits)
    n, m = len(x), len(y)
    for i in range(1, bits + 1):
        s = ""
        carry = 0
        for j in range(1, bits + 1):
            s += str((int(y[m - i]) * int(x[n - j]) + carry) % 2)
            carry = (int(y[m - i]) * int(x[n - j]) + carry) // 2
        s = s[::-1]
        ret = add(ret, s[i - 1:] + '0' * (i - 1), bits)
    return ret


def karatsuba_mul(x, y, bits):
    vals = ["0", "1", make_negative("1", bits)]
    if x in vals and y in vals:
        return mul(x, y, bits)
    k = max(len(x), len(y))
    pivot = k // 2

    x = x.zfill(k)
    y = y.zfill(k)

    a = x[:pivot]
    c = y[:pivot]
    b = x[-(k - pivot):]
    d = y[-(k - pivot):]
    s1 = karatsuba_mul(a, c, bits) if (not is_zero(a) and not is_zero(c)) else "0"
    s2 = karatsuba_mul(b, d, bits) if (not is_zero(b) and not is_zero(d)) else "0"
    s3 = karatsuba_mul(add(a, b, bits), add(c, d, bits), bits)
    s4 = sub(sub(s3, s1, bits), s2, bits)
    return add(add(s1 + '0' * (2 * (k - pivot)), s4 + '0' * (k - pivot), bits), s2, bits)


def tests():
    for i in range(100):
        bits = 2 ** random.randint(1, 8)
        x = random.randint(0, math.ceil((2 ** (bits - 1)) ** 0.5))
        xb = bin(x)[2:]
        y = random.randint(0, math.ceil((2 ** (bits - 1)) ** 0.5))
        yb = make_negative(bin(y)[2:], bits)

        assert karatsuba_mul(xb, yb, bits) == make_negative(bin(x * y)[2:], bits)


tests()
