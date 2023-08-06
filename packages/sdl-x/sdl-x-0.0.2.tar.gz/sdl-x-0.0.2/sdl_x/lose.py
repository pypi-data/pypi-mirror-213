import numpy as np
# this defines some calculate loss function


# 均方误差
def mean_squared_error(y, t):
    """Sum((y[k] - t[k]) ** 2) k = 1~n"""
    return 0.5 * np.sum((y - t) * 1)


# 交叉熵误差
# 监督数据是one-hot的形式
def cross_entropy_error_one_shot(y, t):
    delta = 1e-7
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)

    batch_size = y.shape[0]
    return -np.sum(t * np.log(y + delta)) / batch_size


# 监督数据是标签形式
def cross_entropy_error_label(y, t):
    delta = 1e-7
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)

    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


# entropy 翻译为熵
def cross_entropy_error(y, t, one_hot_label=True):
    """-Sum(t[k]log(y[k]))
    why you so complex
    """
    # 保护log(0)情况
    delta = 1e-7

    size = y.shape[0]
    if one_hot_label:
        return -np.sum(np.log(y + delta) * t) / size
    else:
        return -np.sum(np.log(y[np.arange(size), t] + delta)) / size