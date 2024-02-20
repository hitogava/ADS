def div(x, y, prec=5):
    if y == 0:
        print("Division by zero")
        return None
    n = len(str(abs(x)))
    i = n - 1
    mantissa = exponent = 0
    r = 0
    frac = False
    while i >= 0 or frac:
        nxt = x // 10 ** i % 10 if not frac else 0
        t = r * 10 + nxt
        if frac is False:
            mantissa *= 10
        else:
            exponent *= 10
        if t < y:
            r = t
        else:
            r = t - y * (t // y)
            if not frac:
                mantissa += (t // y)
            else:
                exponent += (t // y)
        if (r == 0 and frac) or (len(str(exponent)) > prec):
            break
        i -= 1
        if i < 0:
            frac = True
    return mantissa, exponent


print(div(15, 10))