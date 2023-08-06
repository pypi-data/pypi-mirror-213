import cv2
import csv
import numpy as np
from lensless.constants import RPI_HQ_CAMERA_CCM_MATRIX, RPI_HQ_CAMERA_BLACK_LEVEL

try:
    import torch
    import torchvision.transforms as tf

    torch_available = True
except ImportError:
    torch_available = False

SUPPORTED_BIT_DEPTH = np.array([8, 10, 12, 16])
FLOAT_DTYPES = [np.float32, np.float64]


def resize(img, factor=None, shape=None, interpolation=cv2.INTER_CUBIC):
    """
    Resize by given factor.

    Parameters
    ----------
    img : :py:class:`~numpy.ndarray`
        Downsampled image.
    factor : int or float
        Resizing factor.
    shape : tuple
        (Height, width).
    interpolation : OpenCV interpolation method
        See https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#cv2.resize

    Returns
    -------
    img : :py:class:`~numpy.ndarray`
        Resized image.
    """
    min_val = img.min()
    max_val = img.max()
    img_shape = np.array(img.shape)[-3:-1]

    assert not ((factor is None) and (shape is None)), "Must specify either factor or shape"
    new_shape = tuple((img_shape * factor).astype(int)) if (shape is None) else shape[-3:-1]

    if np.array_equal(img_shape, new_shape):
        return img

    if torch_available:
        # torch resize expects an input of form [color, depth, width, height]
        tmp = np.moveaxis(img, -1, 0)
        resized = tf.Resize(size=new_shape, interpolation=interpolation)(
            torch.from_numpy(tmp)
        ).numpy()
        resized = np.moveaxis(resized, 0, -1)

    else:
        resized = np.array(
            [
                cv2.resize(img[i], dsize=new_shape[::-1], interpolation=interpolation)
                for i in range(img.shape[-4])
            ]
        )
        # OpenCV discards channel dimension if it is 1, put it back
        if len(resized.shape) == 3:
            # resized = resized[:, :, :, np.newaxis]
            resized = np.expand_dims(resized, axis=-1)

    return np.clip(resized, min_val, max_val)


def rgb2gray(rgb, weights=None):
    """
    Convert RGB array to grayscale.

    Parameters
    ----------
    rgb : :py:class:`~numpy.ndarray`
        (Depth, Height, Width, Channel) image.
    weights : :py:class:`~numpy.ndarray`
        [Optional] (3,) weights to convert from RGB to grayscale.

    Returns
    -------
    img :py:class:`~numpy.ndarray`
        Grayscale image of dimension (depth, height, width, 1).

    """
    assert len(rgb.shape) == 4, "Input must be (depth, height, width, channel)"
    if weights is None:
        weights = np.array([0.299, 0.587, 0.114])
    assert len(weights) == 3
    return np.tensordot(rgb, weights, axes=((3,), 0))[:, :, :, np.newaxis]


def gamma_correction(vals, gamma=2.2):
    """
    Apply `gamma correction <https://www.cambridgeincolour.com/tutorials/gamma-correction.htm>`__.

    Parameters
    ----------
    vals : :py:class:`~numpy.ndarray`
        RGB values to gamma correct.
    gamma : float, optional
        Gamma correction factor.

    Returns
    -------
    vals : :py:class:`~numpy.ndarray`
        Gamma-corrected data.

    """

    # Rec. 709 gamma correction
    # http://www.fourmilab.ch/documents/specrend/specrend.c
    cc = 0.018
    inv_gam = 1 / gamma
    clip_val = (1.099 * np.power(cc, inv_gam) - 0.099) / cc
    return np.where(vals < cc, vals * clip_val, 1.099 * np.power(vals, inv_gam) - 0.099)


def get_max_val(img, nbits=None):
    """
    For uint image.

    Parameters
    ----------
    img : :py:class:`~numpy.ndarray`
        Image array.
    nbits : int, optional
        Number of bits per pixel. Detect if not provided.

    Returns
    -------
    max_val : int
        Maximum pixel value.
    """
    assert img.dtype not in FLOAT_DTYPES
    if nbits is None:
        nbits = int(np.ceil(np.log2(img.max())))

    if nbits not in SUPPORTED_BIT_DEPTH:
        nbits = SUPPORTED_BIT_DEPTH[nbits < SUPPORTED_BIT_DEPTH][0]
    max_val = 2**nbits - 1
    if img.max() > max_val:
        new_nbit = int(np.ceil(np.log2(img.max())))
        print(f"Detected pixel value larger than {nbits}-bit range, using {new_nbit}-bit range.")
        max_val = 2**new_nbit - 1
    return max_val


def bayer2rgb(
    img,
    nbits,
    blue_gain=None,
    red_gain=None,
    black_level=RPI_HQ_CAMERA_BLACK_LEVEL,
    ccm=RPI_HQ_CAMERA_CCM_MATRIX,
    nbits_out=None,
):
    """
    Convert raw Bayer data to RGB with the following steps:

    #. Demosaic with bi-linear interpolation, mapping the Bayer array to RGB.
    #. Black level removal.
    #. White balancing, applying gains to red and blue channels.
    #. Color correction matrix.
    #. Clip.

    Parameters
    ----------
    img : :py:class:`~numpy.ndarray`
        2D Bayer data to convert to RGB.
    nbits : int
        Bit depth of input data.
    blue_gain : float
        Blue gain.
    red_gain : float
        Red gain.
    black_level : float
        Black level. Default is to use that of Raspberry Pi HQ camera.
    ccm : :py:class:`~numpy.ndarray`
        Color correction matrix. Default is to use that of Raspberry Pi HQ camera.
    nbits_out : int
        Output bit depth. Default is to use that of input.

    Returns
    -------
    rgb : :py:class:`~numpy.ndarray`
        RGB data.
    """
    assert len(img.shape) == 2, img.shape
    if nbits_out is None:
        nbits_out = nbits
    if nbits_out > 8:
        dtype = np.uint16
    else:
        dtype = np.uint8

    # demosaic Bayer data
    img = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)

    # correction
    img = img - black_level
    if red_gain:
        img[:, :, 0] *= red_gain
    if blue_gain:
        img[:, :, 2] *= blue_gain
    img = img / (2**nbits - 1 - black_level)
    img[img > 1] = 1
    img = (img.reshape(-1, 3, order="F") @ ccm.T).reshape(img.shape, order="F")
    img[img < 0] = 0
    img[img > 1] = 1
    return (img * (2**nbits_out - 1)).astype(dtype)


def get_distro():
    """
    Get current OS distribution.

    Returns
    -------
    result : str
        Name and version of OS.
    """
    # https://majornetwork.net/2019/11/get-linux-distribution-name-and-version-with-python/
    RELEASE_DATA = {}
    with open("/etc/os-release") as f:
        reader = csv.reader(f, delimiter="=")
        for row in reader:
            if row:
                RELEASE_DATA[row[0]] = row[1]
    if RELEASE_DATA["ID"] in ["debian", "raspbian"]:
        with open("/etc/debian_version") as f:
            DEBIAN_VERSION = f.readline().strip()
        major_version = DEBIAN_VERSION.split(".")[0]
        version_split = RELEASE_DATA["VERSION"].split(" ", maxsplit=1)
        if version_split[0] == major_version:
            # Just major version shown, replace it with the full version
            RELEASE_DATA["VERSION"] = " ".join([DEBIAN_VERSION] + version_split[1:])
    return f"{RELEASE_DATA['NAME']} {RELEASE_DATA['VERSION']}"


def print_image_info(img):
    """
    Print dimensions, data type, max, min, mean.
    """
    print("dimensions : {}".format(img.shape))
    print("data type : {}".format(img.dtype))
    print("max  : {}".format(img.max()))
    print("min  : {}".format(img.min()))
    print("mean : {}".format(img.mean()))


def autocorr2d(vals, pad_mode="reflect"):
    """
    Compute 2-D autocorrelation of image via the FFT.

    Parameters
    ----------
    vals : :py:class:`~numpy.ndarray`
        2-D image.
    pad_mode : str
        Desired padding. See NumPy documentation: https://numpy.org/doc/stable/reference/generated/numpy.pad.html

    Return
    ------
    autocorr : :py:class:`~numpy.ndarray`
    """

    shape = vals.shape
    assert len(shape) == 2

    # pad
    vals_padded = np.pad(
        vals,
        pad_width=((shape[0] // 2, shape[0] // 2), (shape[1] // 2, shape[1] // 2)),
        mode=pad_mode,
    )

    # compute autocorrelation via DFT
    X = np.fft.rfft2(vals_padded)
    autocorr = np.fft.ifftshift(np.fft.irfft2(X * X.conj()))

    # remove padding
    return autocorr[shape[0] // 2 : -shape[0] // 2, shape[1] // 2 : -shape[1] // 2]
