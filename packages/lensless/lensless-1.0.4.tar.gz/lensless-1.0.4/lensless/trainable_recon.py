# #############################################################################
# trainable_recon.py
# =================
# Authors :
# Yohann PERRON [yohann.perron@gmail.com]
# #############################################################################

import abc
from lensless.recon import ReconstructionAlgorithm

try:
    import torch

except ImportError:
    raise ImportError("Pytorch is require to use trainable reconstruction algorithms.")


class TrainableReconstructionAlgorithm(ReconstructionAlgorithm, torch.nn.Module):
    """
    Abstract class for defining lensless imaging reconstruction algorithms with trainable parameters.

    The following abstract methods need to be defined:

    * ``_update``: updating state variables at each iterations.
    * ``reset``: reset state variables.
    * ``_form_image``: any pre-processing that needs to be done in order to view the image estimate, e.g. reshaping or clipping.
    * ``batch_call``: method for performing iterative reconstruction on a batch of images.

    One advantage of deriving from this abstract class is that functionality for
    iterating, saving, and visualization is already implemented, namely in the
    ``apply`` method.

    Consequently, using a reconstruction algorithm that derives from it boils down
    to four steps:

    1. Creating an instance of the reconstruction algorithm.
    2. Training the algorithm
    3. Setting the data.
    4. Applying the algorithm.


    """

    def __init__(self, psf, dtype=None, n_iter=1, **kwargs):
        """
        Base constructor. Derived constructor may define new state variables
        here and also reset them in `reset`.

        Parameters
        ----------

            psf : :py:class:`~torch.Tensor`
                Point spread function (PSF) that models forward propagation.
                Must be of shape (depth, height, width, channels) even if
                depth = 1 and channels = 1. You can use :py:func:`~lensless.io.load_psf`
                to load a PSF from a file such that it is in the correct format.
            dtype : float32 or float64
                Data type to use for optimization.
            n_iter : int
                Number of iterations for unrolled algorithm.
        """
        assert isinstance(psf, torch.Tensor), "PSF must be a torch.Tensor"
        super(TrainableReconstructionAlgorithm, self).__init__(
            psf, dtype=dtype, n_iter=n_iter, **kwargs
        )

    @abc.abstractmethod
    def batch_call(self, batch):
        """
        Method for performing iterative reconstruction on a batch of images.
        This implementation simply calls `apply` on each image in the batch.
        Training algorithms are expected to override this method with a properly vectorized implementation.

        Parameters
        ----------
        batch : :py:class:`~torch.Tensor` of shape (batch, depth, height, width, channels)
            The lensless images to reconstruct.

        Returns
        -------
        :py:class:`~torch.Tensor` of shape (batch, depth, height, width, channels)
            The reconstructed images.
        """

    def apply(
        self, disp_iter=10, plot_pause=0.2, plot=True, save=False, gamma=None, ax=None, reset=True
    ):
        """
        Method for performing iterative reconstruction. Contrary to non-trainable reconstruction
        algorithm, the number of iteration isn't required. Note that `set_data` must be called
        beforehand.

        Parameters
        ----------
        disp_iter : int
            How often to display and/or intermediate reconstruction (in number
            of iterations). If `None` OR `plot` or `save` are False, no
            intermediate reconstruction will be plotted/saved.
        plot_pause : float
            Number of seconds to pause after displaying reconstruction.
        plot : bool
            Whether to plot final result, and intermediate results if
            `disp_iter` is not None.
        save : bool
            Whether to save final result (as PNG), and intermediate results if
            `disp_iter` is not None.
        gamma : float, optional
            Gamma correction factor to apply for plots. Default is None.
        ax : :py:class:`~matplotlib.axes.Axes`, optional
            `Axes` object to fill for plotting/saving, default is to create one.

        Returns
        -------
        final_im : :py:class:`~torch.Tensor`
            Final reconstruction.
        ax : :py:class:`~matplotlib.axes.Axes`
            `Axes` object on which final reconstruction is displayed. Only
            returning if `plot` or `save` is True.

        """
        im = super(TrainableReconstructionAlgorithm, self).apply(
            n_iter=self._n_iter,
            disp_iter=disp_iter,
            plot_pause=plot_pause,
            plot=plot,
            save=save,
            gamma=gamma,
            ax=ax,
            reset=reset,
        )
        return im
