from typing import NamedTuple

import numpy as np


class Sprite:
    """
    A sprite.
    """
    def __init__(self, pos: np.ndarray, texture_name: str)
    self.pos = pos
    self.texture_name = texture_name
    self.relative = np.array([0.0, 0.0])

    @property
    def relative(self):
        return self._relative

    @relative.setter
    def relative(self, value):
        self._relative = value
        self.distance = value @ value

    def __lt__(self, other):
        """
        Sprites are ordered by their distance to camera.
        """
        return self.distance > other.distance
