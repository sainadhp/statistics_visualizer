"""
Dispersion = "how spread out is the data?"

ddof ("delta degrees of freedom") decides what we divide by:
    ddof=0 -> divide by n      -> POPULATION  (you have every value)
    ddof=1 -> divide by n - 1  -> SAMPLE      (your data is a subset)
"""

import numpy as np


def deviations(data):
    """Distance of each value from the mean: x_i - mean. These always sum to 0."""
    arr = np.asarray(data, dtype=float)
    return (arr - arr.mean()).tolist()


def sum_of_squares(data):
    """Sum of squared deviations: Σ(x_i - mean)²  (the top of the variance formula)."""
    return float(np.sum(np.square(deviations(data))))


def variance(data, ddof=0):
    """Average squared distance from the mean."""
    return float(np.var(data, ddof=ddof))


def std(data, ddof=0):
    """Standard deviation = square root of variance -> back in the data's own units."""
    return float(np.std(data, ddof=ddof))


def within_k_std(data, k=1, ddof=0):
    """How many values lie within mean ± k·std. Returns (count, total)."""
    arr = np.asarray(data, dtype=float)
    s = std(arr, ddof)
    inside = np.abs(arr - arr.mean()) <= k * s + 1e-12
    return int(inside.sum()), len(arr)