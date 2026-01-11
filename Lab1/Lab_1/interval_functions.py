import intvalpy as ip
import numpy as np
from interval_mode import interval_mode

def kreinovich(x):
    lefts = [float(el.a) for el in x]
    rights = [float(el.b) for el in x]
    return ip.Interval([float(np.median(lefts)), float(np.median(rights))])


def prolubnikov(x):
    X = sorted(x, key=lambda t: (float(t.a) + float(t.b)) / 2)
    index_med = len(X) // 2

    if len(X) % 2 == 0:
        return (X[index_med - 1] + X[index_med]) / 2

    return X[index_med]


def jaccard_interval(x, y):
    a1 = float(x.a)
    b1 = float(x.b)
    a2 = float(y.a)
    b2 = float(y.b)

    return (min(b1, b2) - max(a1, a2)) / (max(b1, b2) - min(a1, a2))


def jaccard_set(X):
    lefts = [float(x.a) for x in X]
    rights = [float(x.b) for x in X]

    return (min(rights) - max(lefts)) / (max(rights) - min(lefts))


def jaccard_sets(X, Y):
    coeffs = [jaccard_interval(x, y) for x, y in zip(X, Y)]
    return np.array(coeffs)


def jaccard_similarity(X, Y=None):
    if Y is None:
        return jaccard_set(X)

    if isinstance(X, ip.ClassicalArithmetic) and isinstance(Y, ip.ClassicalArithmetic):
        return jaccard_interval(X, Y)

    return jaccard_sets(X, Y)


def mean_jaccart_a(a, X, Y):
    shift = X + a
    return np.mean(jaccard_similarity(shift, Y))


def mean_jaccart_t(t, X, Y):
    scale = X * t
    return np.mean(jaccard_similarity(scale, Y))


def mean_jaccart_a_mode(a, X, Y):
    shift = X + a
    return np.mean(jaccard_similarity(interval_mode(shift), interval_mode(Y)))


def mean_jaccart_t_mode(t, X, Y):
    scale = X * t
    return np.mean(jaccard_similarity(interval_mode(scale), interval_mode(Y)))


def mean_jaccart_a_pro(a, X, Y):
    shift = X + a
    return np.mean(jaccard_similarity(prolubnikov(shift), prolubnikov(Y)))


def mean_jaccart_t_pro(t, X, Y):
    scale = X * t
    return np.mean(jaccard_similarity(prolubnikov(scale), prolubnikov(Y)))


def mean_jaccart_a_kre(a, X, Y):
    shift = X + a
    return np.mean(jaccard_similarity(kreinovich(shift), kreinovich(Y)))


def mean_jaccart_t_kre(t, X, Y):
    scale = X * t
    return np.mean(jaccard_similarity(kreinovich(scale), kreinovich(Y)))


def golden_search(func, a, b, eps=1e-4):
    phi = (3 - np.sqrt(5)) / 2
    x1 = a + phi * (b - a)
    x2 = b - phi * (b - a)
    f1 = func(x1)
    f2 = func(x2)

    while abs(b - a) > eps:
        if f1 < f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - phi * (b - a)
            f2 = func(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + phi * (b - a)
            f1 = func(x1)

    return (a + b) / 2