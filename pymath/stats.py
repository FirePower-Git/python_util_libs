from math import sqrt


def avg(a: list):
    n: int = len(a)
    return 0 if n == 0 else sum(a) / n


def expectancy(a: list, f=lambda e: e):
    n: int = len(a)
    if n == 0:
        return 0

    n_inv: float = 1 / n

    return [f(e) * n_inv for e in a]


def mean(a: list):
    n: int = len(a)
    if n == 0:
        return 0

    if n & 0x01 == 0:
        return (a[(n // 2) - 1] + a[n // 2]) * 0.5
    else:
        return a[n // 2]


def std(a: list):
    return sqrt(var(a))


def std_sample(a: list):
    n: int = len(a)
    if n < 2:
        return 0

    return (n / (n - 1)) * std(a)


def var(a: list):
    n: int = len(a)
    if n == 0:
        return 0

    return expectancy(a, lambda e: e * e) - expectancy(a) ** 2


def var_sample(a: list):
    n: int = len(a)
    if n < 2:
        return 0

    return (n / (n - 1)) * var(a)
