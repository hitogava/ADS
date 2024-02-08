import random


def skip_leading_zeros(x: str):
    i = 0
    while i < len(x):
        if x[i] == '1':
            return i
        i += 1
    return i - 1


def add(x, y, bits=64):
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


def make_negative(x, bits=64):
    res = ""
    x = x.zfill(bits)
    for i in range(bits):
        res += '1' if x[i] == '0' else '0'
    res = add(res, "1".zfill(bits))
    return res


def sub(x, y):
    return add(x, make_negative(y))


def mul(x, y, bits=64):
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
        ret = add(ret, s[i - 1:] + '0' * (i - 1))
    return ret


def karatsuba_mul(x, y, bits=64):
    vals = ["0", "1", make_negative("1")]
    if x in vals and y in vals:
        return mul(x, y)
    k = max(len(x), len(y))
    pivot = k // 2

    x = x.zfill(k)
    y = y.zfill(k)

    a = x[:pivot]
    c = y[:pivot]
    b = x[-(k - pivot):]
    d = y[-(k - pivot):]
    s1 = karatsuba_mul(a, c)
    s2 = karatsuba_mul(b, d)
    s3 = karatsuba_mul(add(a, b), add(c, d))
    s4 = sub(sub(s3, s1), s2)
    return add(add(s1 + '0' * (2 * (k - pivot)), s4 + '0' * (k - pivot)), s2)


def tests():
    assert (karatsuba_mul("0", "0") == "0")
    assert (karatsuba_mul("00", "00") == "0")
    assert (karatsuba_mul(make_negative("0"), "00") == "0")
    assert (karatsuba_mul(make_negative("1"), make_negative("1")) == "1")
    assert (karatsuba_mul("1", "0") == "0")
    assert (karatsuba_mul(make_negative("1"), "0") == "0")
    assert (karatsuba_mul(make_negative("1"), "1") == make_negative("1"))
    assert (karatsuba_mul("1101", "101") == "1000001")
    assert (make_negative(karatsuba_mul("1101", make_negative("110"))) == "1001110")

    for _ in range(100):
        x = random.randint(0, 100)
        xb = bin(x)[2:]
        y = random.randint(0, 100)
        yb = make_negative(bin(y)[2:])
        print(x, y, xb, yb)
        assert (karatsuba_mul(xb, yb) == make_negative(bin(x * y)[2:]))


tests()
