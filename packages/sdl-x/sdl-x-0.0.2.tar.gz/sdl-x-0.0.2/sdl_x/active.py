# softmax函数
import numpy as np


def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    """
    y[k] = exp(e[k]) / Sum(exp[1~n]))
    """
    # 换成转置，省的处理(3,)这种shape
    x = x.T
    x = x - x.max(axis=0)
    exp = np.exp(x)
    y = exp / exp.sum(axis=0)
    return y.T