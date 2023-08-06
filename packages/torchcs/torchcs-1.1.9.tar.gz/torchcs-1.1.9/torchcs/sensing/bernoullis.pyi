def bernoulli(shape, seed=None, norm=True, rmmean=False, dtype='float32', device='cpu'):
    r"""generates Bernoulli observation matrix

    Generates M-by-N Bernoulli observation matrix which have Bernoulli distribution elements(
    columns are l2 normalized).

    Parameters
    ----------
    shape : list or tuple
        shape of Gauss observation matrix [M, N]
    seed : int or None, optional
        the seed for random number generator, by default None
    norm : bool, optional
        normalize the columns of observation matrix, by default True
    rmmean : bool, optional
        remove the mean values before normalization, by default False
    dtype : str, optional
        torch's data type, such as ``'float32'``, ``'float64'``, ``'complex64'``, ``'complex128'``, by default ``'float32'``
    device : str, optional
        generates data on the specified device, supported are ``'cpu'``, ``'cuda:x'``, where, `x` is the cuda device's id.

    Returns
    -------
    th.Tensor
        Bernoulli observation matrix :math:`\bm A`.

    Examples
    ---------

    .. image:: ./_static/BernoulliMatrix.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchcs as tc
        import matplotlib.pyplot as plt

        PhiReal = tc.bernoulli((32, 256), dtype='float32')
        PhiCplx = tc.bernoulli((32, 256), dtype='complex64')
        print(PhiReal.shape)
        print(PhiCplx.shape)

        plt.figure()
        plt.subplot(411)
        plt.imshow(PhiReal)
        plt.title('Real-valued')
        plt.subplot(412)
        plt.imshow(PhiCplx.abs())
        plt.title('Complex-valued (amplitude)')
        plt.subplot(413)
        plt.imshow(PhiCplx.real)
        plt.title('Complex-valued (real part)')
        plt.subplot(414)
        plt.imshow(PhiCplx.imag)
        plt.title('Complex-valued (imaginary part)')
        plt.show()
    """

