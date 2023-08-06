def grpulse(Np=None, Tpr=[2e-3, 90e-3], Apr=[1, 5], Fs=5e3, Ts=1., seed=None):
    r"""generates rectangular pulse

    Parameters
    ----------
    Np : int or None, optional
        the number of pulses, by default None, which means generates randomly
    Tpr : list, optional
        the range of pulse width, by default [2e-3, 100e-3]
    Apr : list, optional
        the range of amplitudes, by default [1, 4]
    Fs : float, optional
        the sampling frequency, by default 10e3
    Ts : float, optional
        the sampling duration, by default 1.
    seed : int or None, optional
        the seed for random number generator, by default None

    Returns
    -------
    tensor
        generated signal tensor (:math:`N_s\times 1`)

    Examples
    ---------

    .. image:: ./_static/DemoGrpulse.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchbox as tb
        import matplotlib.pyplot as plt

        x = tb.grpulse(seed=2023)

        plt.figure()
        plt.grid()
        plt.plot(x, '-b')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

    """

