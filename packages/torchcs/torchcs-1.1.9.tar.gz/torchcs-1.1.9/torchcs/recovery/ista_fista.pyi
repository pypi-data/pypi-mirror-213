def upstep(Phi):
    r"""computes step size

    The update step size is computed by
    
    .. math::
       \alpha = \frac{1}{{\rm max}(|\lambda|)}
    
    where :math:`\lambda` is the eigenvalue of :math:`{\bf \Phi}^H{\bf \Phi}`

    Parameters
    ----------
    Phi : Tensor
        The observation matrix.

    Returns
    -------
    scalar
        The computed updation step size
    """    

def ista(Y, Phi, niter=None, lambd=0.5, alpha=None, tol=1e-6, ssmode='cc'):
    r"""Iterative Shrinkage Thresholding Algorithm

    Iterative Shrinkage Thresholding Algorithm

    .. math::
        {\bf Y} = {\bf \Phi}{\bf X} + \lambda \|{\bf X}\|_1


    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times L}`
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`
    niter : int, optional
        The number of iteration. (the default is None, which means Inf)
    lambd : float, optional
        Regularization factor (the default is 0.5)
    alpha : float, optional
        The update step (the default is None, which means auto computed, see :func:`upstep`)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    ssmode : str, optional
        The type of softshrink function, ``'cc'`` for complex-complex,
        ``'cr'`` for complex-real, ``'rr'`` for real-real.

    Returns
    -------
    X : Tensor
        Reconstructed tensor :math:`{\bf X} \in {\mathbb C}^{N\times L}`

    see :func:`fista`.

    Examples
    ---------

    .. image:: ./_static/ISTAFISTAdemo.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchcs as tc
        import matplotlib.pyplot as plt

        m, n = 32, 64
        x = th.zeros(n, 1)
        x[10] = x[20] = x[60] = 1
        x[15] = x[55] = 0.5
        Phi = th.randn(m, n)
        y = Phi.mm(x)
        Psi = tc.idctmtx(n)

        xista = ista(y, Phi, niter=None, lambd=0.05)
        xfista = fista(y, Phi, niter=None, lambd=0.05)

        plt.figure()
        plt.grid()
        plt.plot(x, 'go', markerfacecolor='none')
        plt.plot(xista, 'b+', markerfacecolor='none')
        plt.plot(xfista, 'r^', markerfacecolor='none')
        plt.legend(['orig', 'ista', 'fista'])
        plt.show()

    """

def fista(Y, Phi, niter=None, lambd=0.5, alpha=None, tol=1e-6, ssmode='cc'):
    r"""Fast Iterative Shrinkage Thresholding Algorithm

    Fast Iterative Shrinkage Thresholding Algorithm

    .. math::
        {\bf Y} = {\bf \Phi}{\bf X} + \lambda \|{\bf X}\|_1

    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times L}`
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`
    niter : int, optional
        The number of iteration (the default is None)
    lambd : float, optional
        Regularization factor (the default is 0.5)
    alpha : float, optional
        The update step (the default is None, which means auto computed, see :func:`upstep`)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    ssmode : str, optional
        The type of softshrink function, ``'cc'`` for complex-complex,
        ``'cr'`` for complex-real, ``'rr'`` for real-real.

    Returns
    -------
    X : Tensor
        Reconstructed tensor :math:`{\bf X} \in {\mathbb C}^{N\times L}`

    see :func:`ista`.

    Examples
    ---------

    .. image:: ./_static/ISTAFISTAdemo.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchcs as tc
        import matplotlib.pyplot as plt

        m, n = 32, 64
        x = th.zeros(n, 1)
        x[10] = x[20] = x[60] = 1
        x[15] = x[55] = 0.5
        Phi = th.randn(m, n)
        y = Phi.mm(x)
        Psi = tc.idctmtx(n)

        xista = ista(y, Phi, niter=None, lambd=0.05)
        xfista = fista(y, Phi, niter=None, lambd=0.05)

        plt.figure()
        plt.grid()
        plt.plot(x, 'go', markerfacecolor='none')
        plt.plot(xista, 'b+', markerfacecolor='none')
        plt.plot(xfista, 'r^', markerfacecolor='none')
        plt.legend(['orig', 'ista', 'fista'])
        plt.show()

    """

