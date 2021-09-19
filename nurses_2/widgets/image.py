from pathlib import Path

import cv2
import numpy as np

from ..data_structures import Size
from .graphic_widget import GraphicWidget


class Image(GraphicWidget):
    """
    An Image widget.

    Parameters
    ----------
    path : pathlib.Path
        Path to image.

    Notes
    -----
    Updating the path immediately reloads the image.
    """
    def __init__(self,
        *args,
        path: Path,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path
        self._load_texture()

    def _load_texture(self):
        path = str(self.path)
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        if image.dtype == np.dtype(np.uint16):
            image = (image // 257).astype(np.uint8)
        elif image.dtype == np.dtype(np.float32):
            image = (image * 255).astype(np.uint8)

        # Add an alpha channel if there isn't one.
        h, w, c = image.shape
        if c == 3:
            default_alpha_channel = np.full((h, w, 1), 255, dtype=np.uint8)
            image = np.dstack((image, default_alpha_channel))

        self._image_texture = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        self.resize(self.size)

    def resize(self, size: Size):
        """
        Resize image.
        """
        self._size = h, w = size

        self.texture = cv2.resize(self._image_texture, (w, 2 * h), interpolation=self.interpolation)
