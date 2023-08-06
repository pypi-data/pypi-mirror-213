def dictshow(D, rcsize=None, stride=None, plot=True, bgcolorv=0, cmap=None, title=None, xlabel=None, ylabel=None):
    r"""
    Trys to show image blocks in one image.

    Parameters
    ----------
    D : array_like
        Blocks to be shown, a bH-bW-bC-bN numpy ndarray.
    rcsize : int, tuple or None, optional
        Specifies how many rows and cols of blocks that you want to show,
        e.g. (rows, cols). If not given, rcsize=(rows, clos) will be computed
        automaticly.
    stride : int, tuple or None, optional
        The step size (blank pixels nums) in row and col between two blocks.
        If not given, stride=(1,1).
    plot : bool, optional
        True for ploting, False for silent and returns a H-W-C numpy ndarray
        for showing.
    bgcolorv : float or None, optional
        The background color, 1 for white, 0 for black. Default, 0.

    Returns
    -------
    out : ndarray or bool
        A H-W-C numpy ndarray for showing.

    See Also
    --------
    odctdict.

    Examples
    --------
    >>> D = pys.odctdict((M, N))
    >>> showdict(D, bgcolor='k')

    """

