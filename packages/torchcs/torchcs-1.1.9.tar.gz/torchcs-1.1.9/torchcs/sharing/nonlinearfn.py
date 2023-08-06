#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import torch as th


def rrsoftshrink(x, T):
    # s = th.sign(x)
    # x = x.abs() - t
    # x[x < 0.] = 0.
    # return s * x
    return th.nn.functional.softshrink(x, lambd=T)


def crsoftshrink(x, T):

    if th.is_complex(x):
        return th.nn.functional.softshrink(x.real, lambd=T) + 1j * th.nn.functional.softshrink(x.imag, lambd=T)
    elif x.shape[-1] == 2:
        return th.nn.functional.softshrink(x, lambd=T)


def ccsoftshrink(x, T):
    xabs = x.abs()
    x = (x / (xabs + 1e-32)) * (xabs - T)
    x[xabs <= T] = 0.
    return x


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    x = th.randn(256, 1)
    x = th.linspace(-5, 5, 256)

    y = rrsoftshrink(x, 0.5)
    print(y.shape)

    plt.figure()
    plt.plot(x, y)

    x = th.linspace(-5, 5, 256) + 1j * th.linspace(-3, 3, 256)
    y = crsoftshrink(x, 0.5)
    plt.figure()
    plt.plot(x.real, y.real)
    plt.plot(x.imag, y.imag)

    x = th.linspace(-5, 5, 256) + 1j * th.linspace(-3, 3, 256)
    y = ccsoftshrink(x, 0.5)
    plt.figure()
    plt.plot(x.real, y.real)
    plt.plot(x.imag, y.imag)
    plt.show()
