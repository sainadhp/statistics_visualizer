import numpy as np
from manim import Scene

DEFAULT_DATA = [3, 7, 4, 7, 9, 2, 7, 5]

def fmt(v):
    """5.0 -> '5', 
       5.5 -> '5.5', 
       3.14159 -> '3.14'
    """
    return f"{round(float(v), 2):g}"

def axis_range(values):
    """Return (start, end, step, decimals) for a NumberLine that fits the data nicely."""
    lo, hi = float(min(values)), float(max(values))
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    raw = (hi - lo) / 8                              # aim for about 8-10 ticks
    mag = 10 ** np.floor(np.log10(raw))
    step = next(m * mag for m in (1, 2, 5, 10) if m * mag >= raw)   # 1, 2, 5, 10, 20, 50...
    start = np.floor(lo / step) * step
    end = np.ceil(hi / step) * step
    decimals = max(0, int(-np.floor(np.log10(step))))
    return start, end, step, decimals


class DataScene(Scene):
    """
    A normal Manim Scene, plus `self.data`.
    Usage:  MeanScene(data=[1, 2, 3])   or   MeanScene()  (uses DEFAULT_DATA)
    """

    def __init__(self, data=None, **kwargs):
        self.data = [float(x) for x in (data if data is not None else DEFAULT_DATA)]
        super().__init__(**kwargs)