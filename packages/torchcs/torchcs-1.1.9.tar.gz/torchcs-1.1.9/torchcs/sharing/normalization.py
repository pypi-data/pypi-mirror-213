#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
#
# @Note    : https://www.cnblogs.com/AndyJee/p/5091932.html
#
import torch as th


def colnormalize(X, rmmean=True):

    if rmmean:
        X = X - X.mean(0, keepdims=True)

    N = X.shape[1]
    for k in range(N):
        v = X[:, k]
        norm = th.linalg.norm(v).item()
        if abs(norm) > 1e-32:
            X[:, k] = v / norm
        else:
            X[:, k] = v
    return X


if __name__ == '__main__':

    X = th.rand(4, 3)
    print(X)
    X = colnormalize(X)
    print(X)
