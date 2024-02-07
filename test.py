def add(x, y, bits=8):
    res = ""
    carry = 0
    n, m = len(x), len(y)
    for i in range(1, bits + 1):
        t = int(x[n - i]) + int(y[m - i]) + carry
        res += str(t % 2)
        carry = t // 2
    return res[::-1]


def make_negative(x):
    res = ""
    for i in range(len(x)):
        res += '1' if x[i] == '0' else '0'
    res = add(res, "00000001")
    return res


def sub(x, y):
    return add(x, make_negative(y))


def from_two_compl(x, bits=8):
    x = sub(x, "1".zfill(bits))
    res = ""
    for i in range(len(x)):
        res += '1' if x[i] == '0' else '0'
    return res


def mul(x, y, bits=8):
    ret = '0' * bits
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


def karatsuba_mul(x, y, bits=8):
    n, m = 0, 0
    if x[0] == '0':
        t = int(x, 2)
        n = len(str(int(x, 2)))
    else:
        n = len(str(int(make_negative(x), 2)))
    if y[0] == '0':
        m = len(str(int(y, 2)))
    else:
        m = len(str(int(make_negative(y), 2)))
    if n == 1 and m == 1:
        return mul(x, y)
    pivot = bits // 2
    a = x[:pivot]
    c = y[:pivot]
    b = x[-(bits - pivot):]
    d = y[-(bits - pivot):]

    s1 = karatsuba_mul(a, c)
    s2 = karatsuba_mul(b, d)
    s3 = karatsuba_mul(add(a, b), add(c, d))
    s4 = sub(sub(s3, s1), s2)
    return add(add(mul(bin(2 ** (2 * pivot))[2:], s1), mul(bin(2 ** pivot)[2:], s4)), s2)


# print(mul("00000110", make_negative("00000100")))
print(karatsuba_mul("00000110", "00000100"))
print(karatsuba_mul("00000110", make_negative("00000100")))
