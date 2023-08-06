def dctmtx(N):
    r"""Discrete cosine transform matrix

    .. math::
       {\bm y} = {\bm D}{\bm x}
       :label: equ-DCT_MatrixRep

    where, :math:`{\bm x} = (x_n)_{N\times 1}, x_n = x[n]`, :math:`{\bm D} = (d_{ij})_{N\times N}` can be expressed as

    .. math::
       {\bm D} = \sqrt{\frac{2}{N}}\left[\begin{array}{cccc}{1/\sqrt{2}} & {1/\sqrt{2}} & {1/\sqrt{2}} & {\cdots} & {1/\sqrt{2}} \\ {\cos \frac{\pi}{2 N}} & {\cos \frac{3 \pi}{2 N}} & {\cos \frac{5 \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1) \pi}{2 N}} \\ {\vdots} & {\vdots} & {\vdots} & {\vdots} \\ {\cos \frac{(N-1) \pi}{2 N}} & {\cos \frac{3(N-1) \pi}{2 N}} & {\cos \frac{5(N-1) \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1)(N-1) \pi}{2 N}}\end{array}\right]
       :label: equ-DCT_Matrix

    Arguments
    ----------------
    N : int
        signal dimesion.

    Returns
    -------------------
    T tensor
        DCT matrix.
    """

def idctmtx(N):
    r"""Inverse discrete cosine transform matrix

    .. math::
       {\bm x} = {\bm D}{\bm z}
       :label: equ-DCT_MatrixRep

    where, :math:`{\bm x} = (x_n)_{N\times 1}, x_n = x[n]`, :math:`{\bm D}^T = (d_{ij})_{N\times N}` can be expressed as

    .. math::
       {\bm D}^T = \sqrt{\frac{2}{N}}\left[\begin{array}{cccc}{1/\sqrt{2}} & {1/\sqrt{2}} & {1/\sqrt{2}} & {\cdots} & {1/\sqrt{2}} \\ {\cos \frac{\pi}{2 N}} & {\cos \frac{3 \pi}{2 N}} & {\cos \frac{5 \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1) \pi}{2 N}} \\ {\vdots} & {\vdots} & {\vdots} & {\vdots} \\ {\cos \frac{(N-1) \pi}{2 N}} & {\cos \frac{3(N-1) \pi}{2 N}} & {\cos \frac{5(N-1) \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1)(N-1) \pi}{2 N}}\end{array}\right]
       :label: equ-IDCT_Matrix

    Arguments
    ----------------
    N : int
        signal dimesion.

    Returns
    -------------------
    T tensor
        IDCT matrix.
    """

def dct1(x, axis=0):
    r"""1-Dimension Discrete cosine transform

       The DCT of signal :math:`x[n], n=0, 1,\cdots, N-1` is expressed as

       .. math::
          y[k] = {\rm DCT}(x[n]) = \left\{ {\begin{array}{lll}
              {\sqrt{\frac{2}{N}}\sum_{n=0}^{N-1}x[n]\frac{1}{\sqrt 2}, \quad k=0}\\
              {\sqrt{\frac{2}{N}}\sum_{n=0}^{N-1}x[n]{\rm cos}\frac{(2n + 1)k\pi}{2N}, \quad k=1, \cdots, N-1}
              \end{array}} \right.
          :label: equ-DCT

       where, :math:`k=0, 1, \cdots, N-1`

    N. Ahmed, T. Natarajan, and K. R. Rao. Discrete cosine transform.
    IEEE Transactions on Computers, C-23(1):90–93, 1974. doi:10.1109/T-C.1974.223784

    Arguments
    -------------
    x tensor
        signal vector or matrix

    Keyword Arguments
    --------------------
    axis : number
        transformation axis when x is a matrix (default: {0}, col)

    Returns
    -----------
    y tensor
        the coefficients.


    """

def idct1(y, axis=0):
    r"""1-Dimension Inverse Discrete cosine transform

    .. math::
       {\bm x} = {\bm D}^{-1}{\bm y} = {\bm D}^T{\bm y}
       :label: equ-IDCT_MatrixRep

    Arguments
    -------------
    y tensor
        coefficients

    Keyword Arguments
    ------------------
    axis : number
        IDCT along which axis (default: {0})

    Returns
    -------------
    x tensor
        recovered signal.
    """

def dct2(X):
    r"""2-Dimension Discrete cosine transform

    dct1(dct1(X, axis=0), axis=1)

    Arguments
    -----------------
    X tensor
        signal matrix

    Returns
    -----------
    Y tensor
        coefficients matrix
    """

def idct2(X):
    r"""2-Dimension Inverse Discrete cosine transform

    idct1(idct1(X, axis=0), axis=1)

    Arguments
    --------------
    X tensor
        signal matrix

    Returns
    --------------
    Y tensor
        coefficients matrix
    """

def dctdict(N, isnorm=True, islog=False):
    r"""Complete DCT dictionary


    .. math::
       {\bm D} = \sqrt{\frac{2}{N}}\left[\begin{array}{cccc}{1/\sqrt{2}} & {1/\sqrt{2}} & {1/\sqrt{2}} & {\cdots} & {1/\sqrt{2}} \\ {\cos \frac{\pi}{2 N}} & {\cos \frac{3 \pi}{2 N}} & {\cos \frac{5 \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1) \pi}{2 N}} \\ {\vdots} & {\vdots} & {\vdots} & {\vdots} \\ {\cos \frac{(N-1) \pi}{2 N}} & {\cos \frac{3(N-1) \pi}{2 N}} & {\cos \frac{5(N-1) \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1)(N-1) \pi}{2 N}}\end{array}\right]
       :label: equ-DCT_Matrix

    Because :math:`{\bm z} = {\bm D}{\bm x}`, :math:`{\bm D}{\bm D}^T = {\bm I}`
    So, :math:`{\bm x} = {\bm D}^T{\bm z}`

    Arguments
    -------------
    N : int
        The dictionary is of size :math:`N\times N`

    Returns
    -------------
    D tensor
        DCT dictionary ( :math:`{\bm D}^T` ).
    """

def odctdict(dictshape, isnorm=True, islog=False):
    r"""Overcomplete 1D-DCT dictionary

    .. math::
       {\bm D} = \sqrt{\frac{2}{N}}\left[\begin{array}{cccc}{1/\sqrt{2}} & {1/\sqrt{2}} & {1/\sqrt{2}} & {\cdots} & {1/\sqrt{2}} \\ {\cos \frac{\pi}{2 N}} & {\cos \frac{3 \pi}{2 N}} & {\cos \frac{5 \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1) \pi}{2 N}} \\ {\vdots} & {\vdots} & {\vdots} & {\vdots} \\ {\cos \frac{(M-1) \pi}{2 N}} & {\cos \frac{3(M-1) \pi}{2 N}} & {\cos \frac{5(M-1) \pi}{2 N}} & {\cdots} & {\cos \frac{(2 N-1)(M-1) \pi}{2 N}}\end{array}\right]
       :label: equ-ODCT_Matrix

    .. math::
       {\bm D} = \left[\frac{{\bm d}_0}{\|{\bm d}_0\|_2}, \frac{{\bm d}_1}{\|{\bm d}_1\|_2},\cdots, \frac{{\bm d}_{N-1}}{\|{\bm d}_{N-1}\|_2}\right]
       :label: equ-ODCT_Matrix_normed

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

def odctndict(dictshape, axis=-1, isnorm=True, islog=False):
    r"""generates Overcomplete nD-DCT dictionary

    .. math::
       {\bm D}_{nd} = {\bm D}_{(n-1)d} \otimes {\bm D}_{(n-1)d}.
       :label: equ-CreatenDDCT_Matrix

    Arguments
    ---------------------
    dictshape : `list` or `tuple`
        shape of DCT dict [M, N]

    Keyword Arguments
    ---------------------
    axis : `number`
        Axis along which the dct is computed. If -1 then the transform
        is multidimensional(default=-1) (default: {-1})

    isnorm : `bool`
        normlize atoms (default: True)

    islog : `bool`
        display log info (default: False)

    Returns
    ---------------------
    OD : `torch tensor`
        Overcomplete nD-DCT dictionary
    """

