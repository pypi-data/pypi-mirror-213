import numpy as np


def numerical_gradient(f, x: np.ndarray):
    """
    calc gradient
    for now, only support ndim 2
    """
    h = 1e-4
    grad = np.zeros_like(x)
    for i in range(x.size):
        tmp_val = x.flat[i]
        x.flat[i] = tmp_val + h
        fxh1 = f(x)

        x.flat[i] = tmp_val - h
        fxh2 = f(x)
        grad.flat[i] = (fxh1 - fxh2) / (2 * h)
        x.flat[i] = tmp_val
    return grad


def gradient_decline(f, init_x, learn_gap, step=10000):
    """梯度下降，可能单词用错了"""
    x = init_x
    for i in range(step):
        grad = numerical_gradient(f, x)
        x = x - grad * learn_gap
    return f(x)
