import abc
import functools
import inspect
import logging

import cv2
import numpy as np
from skimage import measure, morphology

from ..meta.ppid import kwargs_to_ppid


class Segmenter(abc.ABC):
    #: Whether to enable mask post-processing. If disabled, you should
    #: make sure that your mask is properly defined and cleaned or you
    #: have to call `process_mask` in your `segment_approach` implementation.
    mask_postprocessing = False
    #: Default keyword arguments for mask post-processing. See `process_mask`
    #: for available options.
    mask_default_kwargs = {}
    #: If the segmenter requires a background image, set this to True
    requires_background = False

    def __init__(self, kwargs_mask=None, debug=False, **kwargs):
        """Base segemnter

        Parameters
        ----------
        data: HDF5Data
            Instance containing the raw data. Requires at least the
            `image` and `image_bg` attributes. Some segemnters require
            more properties, so make sure to use :class:`.HDF5Data`.
        kwargs_mask: dict
            Keyword arguments for mask post-processing (see `process_mask`)
        """
        self.debug = debug
        self.logger = logging.getLogger(__name__).getChild(
            self.__class__.__name__)
        spec = inspect.getfullargspec(self.segment_approach)
        #: custom keyword arguments for the subclassing segmenter
        self.kwargs = spec.kwonlydefaults or {}
        self.kwargs.update(kwargs)

        #: keyword arguments for mask post-processing
        self.kwargs_mask = {}
        if self.mask_postprocessing:
            spec_mask = inspect.getfullargspec(self.process_mask)
            self.kwargs_mask.update(spec_mask.kwonlydefaults or {})
            self.kwargs_mask.update(self.mask_default_kwargs)
            if kwargs_mask is not None:
                self.kwargs_mask.update(kwargs_mask)
        elif kwargs_mask:
            raise ValueError(
                "`kwargs_mask` has been specified, but mask post-processing "
                f"is disabled for segmenter {self.__class__}")

    @classmethod
    def key(cls):
        """The unique key/name of this segmenter class"""
        key = cls.__name__.lower()
        if key.startswith("segment"):
            key = key[7:]
        return key

    def get_ppid(self):
        """Return a unique segmentation pipeline identifier

        The pipeline identifier is universally applicable and must
        be backwards-compatible (future versions of dcevent will
        correctly acknowledge the ID).

        The segmenter pipeline ID is defined as::

            KEY:KW_APPROACH:KW_MASK

        Where KEY is e.g. "legacy" or "watershed", and KW_APPROACH is a
        list of keyword arguments for `segment_approach`, e.g.::

            thresh=-6^blur=0

        which may be abbreviated to::

            t=-6^b=0

        KW_MASK represents keyword arguments for `process_mask`.
        """
        return self.get_ppid_from_kwargs(self.kwargs, self.kwargs_mask)

    @classmethod
    def get_ppid_from_kwargs(cls, kwargs, kwargs_mask=None):
        """Return the pipeline ID from given keyword arguments

        See Also
        --------
        get_ppid: Same method for class instances
        """
        if kwargs_mask is None and kwargs.get("kwargs_mask", None) is None:
            raise KeyError("`kwargs_mask` must be either specified as "
                           "keyword argument to this method or as a key "
                           "in `kwargs`!")
        if kwargs_mask is None:
            # see check above (kwargs_mask may also be {})
            kwargs_mask = kwargs["kwargs_mask"]
        # Start with the default mask kwargs defined for this subclass
        kwargs_mask_used = cls.mask_default_kwargs
        kwargs_mask_used.update(kwargs_mask)
        key = cls.key()
        csegm = kwargs_to_ppid(cls, "segment_approach", kwargs)
        cmask = kwargs_to_ppid(cls, "process_mask", kwargs_mask_used)
        return ":".join([key, csegm, cmask])

    @staticmethod
    @functools.cache
    def get_disk(radius):
        """Cached `skimage.morphology.disk(radius)`"""
        return morphology.disk(radius)

    @staticmethod
    def process_mask(mask, *,
                     clear_border: bool = True,
                     fill_holes: bool = True,
                     closing_disk: int = 5):
        """Post-process retrieved mask image

        This is an optional convenience method that is called for each
        subclass individually. To enable mask post-processing, set
        `mask_postprocessing=True` in the subclass and specify default
        `mask_default_kwargs`.

        Parameters
        ----------
        mask: 2d boolean ndarray
        clear_border: bool
            clear the image boarder using
            :func:`skimage.segmentation.clear_border`
        fill_holes: bool
            binary-fill-holes in the binary mask image using
            :func:`scipy.ndimage.binary_fill_holes`
        closing_disk: int or None
            if > 0, perform a binary closing with a disk
            of that radius in pixels
        """
        if clear_border:
            #
            # from skimage import segmentation
            # segmentation.clear_border(mask, out=mask)
            #
            if (mask[0, :].sum() or mask[-1, :].sum()
                    or mask[:, 0].sum() or mask[:, -1].sum()):
                border = np.zeros_like(mask)
                border[0] = True
                border[-1] = True
                border[:, 0] = True
                border[:, -1] = True
                label = measure.label(mask)
                indices = sorted(np.unique(label[border]))
                for ii in indices[1:]:
                    mask[label == ii] = False

        # scikit-image is too slow for us here. So we use OpenCV.
        # https://github.com/scikit-image/scikit-image/issues/1190
        mask_int = np.array(mask, dtype=np.uint8) * 255

        if closing_disk:
            #
            # from skimage import morphology
            # morphology.binary_closing(
            #    mask,
            #    footprint=morphology.disk(closing_disk),
            #    out=mask)
            #
            element = Segmenter.get_disk(closing_disk)
            mask_dilated = cv2.dilate(mask_int, element)
            mask_int = cv2.erode(mask_dilated, element)

        if fill_holes:
            #
            # from scipy import ndimage
            # mask_old = ndimage.binary_fill_holes(mask)
            #
            # Floodfill algorithm fills the background image and
            # the resulting inversion is the image with holes filled.
            im_floodfill = mask_int.copy()
            h, w = mask_int.shape
            ff_mask = np.zeros((h + 2, w + 2), np.uint8)
            cv2.floodFill(im_floodfill, ff_mask, (0, 0), 255)
            im_floodfill_inv = cv2.bitwise_not(im_floodfill)
            mask_int = mask_int | im_floodfill_inv

        mask = mask_int > 0
        return mask

    def segment_frame(self, image):
        """Return the frame mask for one image at `index`"""
        segm_wrap = self.segment_frame_wrapper()
        # obtain mask
        mask = segm_wrap(image)
        # optional postprocessing
        if self.mask_postprocessing:
            mask = self.process_mask(mask, **self.kwargs_mask)
        return mask

    @functools.cache
    def segment_frame_wrapper(self):
        if self.kwargs:
            # For segmenters that accept keyword arguments.
            segm_wrap = functools.partial(self.segment_approach,
                                          **self.kwargs)
        else:
            # For segmenters that don't accept keyword arguments.
            segm_wrap = self.segment_approach
        return segm_wrap

    @staticmethod
    @abc.abstractmethod
    def segment_approach(image, image_bg):
        """Perform segmentation and return binary mask

        This is the approach the subclasses implements.
        """

    @abc.abstractmethod
    def segment_batch(self, data, start, stop):
        """Return the frame mask array for an entire batch"""
