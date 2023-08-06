import numpy as np

from pidgan.optimization.scores.BaseScore import BaseScore


class KSDistance(BaseScore):
    def __init__(self, name="kst_score", dtype=None) -> None:
        super().__init__(name, dtype)
