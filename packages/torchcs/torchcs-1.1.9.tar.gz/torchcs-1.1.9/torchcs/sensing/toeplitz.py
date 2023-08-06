#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
#
# @Note    : https://www.cnblogs.com/AndyJee/p/5091932.html
#
import numpy as np
from torchcs.sharing.normalization import colnormalize


def toeplitz(shape, verbose=True):
    r"""generates Toeplitz observation matrix

    Generates M-by-N Toeplitz observation matrix

    .. math::
        {\bm \Phi}_{ij} = \left[\begin{array}{ccccc}{a_{0}} & {a_{-1}} & {a_{-2}} & {\cdots} & {a_{-n+1}} \\ {a_{1}} & {a_{0}} & {a_{-1}} & {\cdots} & {a_{-n+2}} \\ {a_{2}} & {a_{1}} & {a_{0}} & {\cdots} & {a_{-n+3}} \\ {\vdots} & {\vdots} & {\vdots} & {\ddots} & {\vdots} \\ {a_{n-1}} & {a_{n-2}} & {a_{n-3}} & {\cdots} & {a_{0}}\end{array}\right]

    Arguments
    ------------
    shape : `list` or `tuple`
        shape of Toeplitz observation matrix [M, N]

    Keyword Arguments
    ----------------------
    verbose : `bool`
        display log info (default: {True})

    Returns
    -------------
    A : `ndarray`
        Toeplitz observation matrix :math:`\bm A`.
    """

    (M, N) = shape
    raise NotImplementedError

    return Phi
