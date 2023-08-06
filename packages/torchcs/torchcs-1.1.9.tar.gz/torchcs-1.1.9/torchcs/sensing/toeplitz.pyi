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

