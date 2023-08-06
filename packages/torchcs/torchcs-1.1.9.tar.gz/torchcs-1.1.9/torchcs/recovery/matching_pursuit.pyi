def mp(X, D, K=None, norm=[False, True], tol=1.0e-6, mode=None, islog=False):
    r"""Matching Pursuit

    .. math::
        x = Dz

    .. math::
        ({\bm D}_{{\mathbb I}_t}^T{\bm D}_{{\mathbb I}_t})^{-1}

    to avoid matrix singularity

    .. math::
        ({\bm D}_{{\mathbb I}_t}^T{\bm D}_{{\mathbb I}_t} + C {\bm I})^{-1}

    where, :math:`C > 0`.

    Parameters
    --------------
    X tensor
        signal vector or matrix, if :math:`{\bm X}\in{\mathbb R}^{M\times L}` is a matrix,
        then apply OMP on each column

    D tensor
        overcomplete dictionary ( :math:`{\bm D}\in {\mathbb R}^{M\times N}` )

    Keyword Arguments
    ----------------------
    K : int
        The sparse degree (default: size of :math:`{\bm x}`)

    norm : list of bool
        The first element specifies whether to normalize data, the second element specifies
        whther to normalize dictionary. If True, will be normalized by subtracting the mean
        and dividing by the l2-norm. (default: [False, True])

    tol : float
        The tolerance for the optimization (default: {1.0e-6})

    mode : str
        Complex mode or real mode, ``'cc'`` for complex-->complex,
        ``'cr'`` for complex-->real, ``'rr'`` for real-->real

    islog : bool
        Show more log info.
    """

def omp(X, D, K=None, C=1e-6, norm=[False, False], tol=1.0e-6, method='pinv', mode=None, device='cpu', islog=False):
    r"""Orthogonal Matching Pursuit

    ROMP add a small penalty factor :math:`C` to

    .. math::
        x = Dz

    .. math::
        ({\bm D}_{{\mathbb I}_t}^T{\bm D}_{{\mathbb I}_t})^{-1}

    to avoid matrix singularity

    .. math::
        ({\bm D}_{{\mathbb I}_t}^T{\bm D}_{{\mathbb I}_t} + C {\bm I})^{-1}

    where, :math:`C > 0`.

    Parameters
    --------------
    X tensor
        signal vector or matrix, if :math:`{\bm X}\in{\mathbb R}^{M\times L}` is a matrix,
        then apply OMP on each column

    D tensor
        overcomplete dictionary ( :math:`{\bm D}\in {\mathbb R}^{M\times N}` )

    Keyword Arguments
    ----------------------
    K : int
        The sparse degree (default: size of :math:`{\bm x}`)

    C : float
        The regularization factor (default: 1.0e-6)

    norm : list of bool
        The first element specifies whether to normalize data, the second element specifies
        whther to normalize dictionary. If True, will be normalized by subtracting the mean
        and dividing by the l2-norm. (default: [False, False])

    tol : float
        The tolerance for the optimization (default: {1.0e-6})

    method : str
        The method for solving new sparse coefficients.

    mode : str
        Complex mode or real mode, ``'cc'`` for complex-->complex,
        ``'cr'`` for complex-->real, ``'rr'`` for real-->real.

    islog : bool
        Show more log info.


    Examples
    ---------

    .. image:: ./_static/MPOMPdemo.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::

        import torch as th
        import torchcs as tc
        import matplotlib.pyplot as plt

        seed = 2021
        f0, f1, f2, f3 = 50, 100, 200, 400
        Fs = 800
        Ts = 0.32
        Ns = int(Ts * Fs)
        R = 2
        K = 7

        t = th.linspace(1, Ns, Ns).reshape(Ns, 1) / Fs
        pit2 = 2. * th.pi * t
        x = 0.3 * th.cos(pit2 * f0) + 0.6 * th.cos(pit2 * f1) + 0.1 * th.cos(pit2 * f2) + 0.9 * th.cos(pit2 * f3)

        f = th.linspace(-Fs / 2., Fs / 2., Ns).reshape(Ns, 1)
        X = th.fft.fftshift(th.fft.fft(x, dim=0))

        M = Ns
        N = int(Ns * R)
        Psi = tc.odctdict((M, N))
        # Psi = tc.idctmtx(N)

        z, _ = tc.mp(x, Psi, K=K, norm=[False, False], tol=1.0e-6, islog=False)
        xmp = Psi.mm(z)
        Xmp = th.fft.fftshift(th.fft.fft(xmp, dim=0))

        z, _ = tc.omp(x, Psi, K=K, C=1e-1, norm=[False, False], tol=1.0e-6, method='pinv', islog=False)
        xomp = Psi.mm(z)
        Xomp = th.fft.fftshift(th.fft.fft(xomp, dim=0))

        xgp = x
        Xgp = X
        plt.figure()
        plt.subplot(221)
        plt.grid()
        plt.plot(t, x, '-r')
        plt.subplot(222)
        plt.grid()
        plt.plot(f, X.abs(), '-r')
        plt.subplot(223)
        plt.grid()
        plt.plot(x, '-*r')
        plt.plot(xmp, '-sg')
        plt.plot(xomp, '-+b')
        plt.plot(xgp, '--k')
        plt.legend(['Real', 'MP', 'OMP', 'GP'])
        plt.subplot(224)
        plt.grid()
        plt.plot(X.abs(), '-*r')
        plt.plot(Xmp.abs(), '-sg')
        plt.plot(Xomp.abs(), '-+b')
        plt.plot(Xgp.abs(), '--k')
        plt.legend(['Real', 'MP', 'OMP', 'GP'])
        plt.show()

    """

def gp():
