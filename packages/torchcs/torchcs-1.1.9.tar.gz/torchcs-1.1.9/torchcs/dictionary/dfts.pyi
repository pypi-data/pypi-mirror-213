def dftmtx(N):
    r"""Discrete Fourier transform matrix

    .. math::
       {\bm y} = {\bm D}{\bm x}
       :label: equ-DFT_MatrixRep

    where, :math:`{\bm x} = (x_n)_{N\times 1}, x_n = x[n]`, :math:`{\bm D} = (d_{ij})_{N\times N}` can be expressed as

    Arguments
    ----------------
    N : integer
        signal dimesion.

    Returns
    -------------------
    T tensor
        DFT matrix.
    """

def idftmtx(N):
    r"""Discrete Fourier transform matrix

    .. math::
       {\bm y} = {\bm D}{\bm x}
       :label: equ-DFT_MatrixRep

    where, :math:`{\bm x} = (x_n)_{N\times 1}, x_n = x[n]`, :math:`{\bm D} = (d_{ij})_{N\times N}` can be expressed as

    Arguments
    ----------------
    N : integer
        signal dimesion.

    Returns
    -------------------
    T tensor
        DFT matrix.
    """

def dft1(x, axis=0):
    r"""1-Dimension Discrete Fourier transform

       The DFT of signal :math:`x[n], n=0, 1,\cdots, N-1` is expressed as


    Arguments
    -------------
    x : numpy array
        signal vector or matrix

    Keyword Arguments
    --------------------
    axis : number
        transformation axis when x is a matrix (default: {0}, col)

    Returns
    -----------
    y : numpy array
        the coefficients.


    """

def idft1(y, axis=0):
    r"""1-Dimension Inverse Discrete cosine transform

    .. math::
       {\bm x} = {\bm D}^{-1}{\bm y} = {\bm D}^T{\bm y}
       :label: equ-IDFT_MatrixRep

    Arguments
    -------------
    y : numpy array
        coefficients

    Keyword Arguments
    ------------------
    axis : number
        IDFT along which axis (default: {0})

    Returns
    -------------
    x : numpy array
        recovered signal.
    """

def dft2(X):
    r"""2-Dimension Discrete cosine transform

    dft1(dft1(X, axis=0), axis=1)

    Arguments
    -----------------
    X : numpy array
        signal matrix

    Returns
    -----------
    Y : numpy array
        coefficients matrix
    """

def idft2(X):
    r"""2-Dimension Inverse Discrete cosine transform

    idft1(idft1(X, axis=0), axis=1)

    Arguments
    --------------
    X : numpy array
        signal matrix

    Returns
    --------------
    Y : numpy array
        coefficients matrix
    """

def dftdict(N, isnorm=True, islog=False):
    r"""Complete DFT dictionary


    Arguments
    -------------
    N : integer
        The dictionary is of size :math:`N\times N`

    Returns
    -------------
    D : numpy array
        DFT dictionary ( :math:`{\bm D}^T` ).
    """

def odftdict(dictshape, isnorm=True, islog=False):
    r"""Overcomplete 1D-DFT dictionary


    Arguments
    ----------------------
    dictshape : tuple
        dictionary shape

    Keyword Arguments
    ----------------------
    isnorm : bool
        normlize atoms (default: True)
    islog : bool
        display log (default: False)
    """

def odftndict(dictshape, axis=-1, isnorm=True, islog=False):
    r"""generates Overcomplete nD-DFT dictionary

    .. math::
       {\bm D}_{nd} = {\bm D}_{(n-1)d} \otimes {\bm D}_{(n-1)d}.
       :label: equ-CreatenDDFT_Matrix

    Arguments
    ---------------------
    dictshape : `list` or `tuple`
        shape of DFT dict [M, N]

    Keyword Arguments
    ---------------------
    axis : `number`
        Axis along which the dft is computed. If -1 then the transform
        is multidimensional(default=-1) (default: {-1})

    isnorm : `bool`
        normlize atoms (default: True)

    islog : `bool`
        display log info (default: False)

    Returns
    ---------------------
    OD : `torch tensor`
        Overcomplete nD-DFT dictionary
    """

