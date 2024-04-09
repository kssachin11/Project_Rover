import heapq
from math import pi
import numpy as np

from scipy.signal import convolve2d
from scipy.stats import norm

BLUR_RADIUS = 8


SOBEL = np.array([
    [1 +1j,   0 +2j,   -1 +1j], 
    [2 +0j,   0 +0j,   -2 +0j],
    [1 -1j,   0 -2j,   -1 -1j]
])

PREWITT = np.array([
    [1 +1j,   0 +1j,   -1 +1j], 
    [1 +0j,   0 +0j,   -1 +0j],
    [1 -1j,   0 -1j,   -1 -1j]
])

SCHARR = np.array([
    [ 47 +47j,   0 +162j,    -47 +47j],
    [162  +0j,   0   +0j,   -162  +0j],
    [ 47 -47j,   0 -162j,    -47 -47j]
])

binsIn = [pi/180*i for i in range(-44, 44)]

def calculate_deviation(data: np.ndarray) -> float:
    """Calculates the rotational deviation of a point cloud array with respect to 90° steps. Uses average of Sobel, Prewitt and Scharr operator.

    Args:
    ---
        data (np.ndarray): Point cloud array.

    Returns:
    ---
        float: Estimated deviation in degrees.
    """
    matrices = [SOBEL, PREWITT, SCHARR]

    x = norm.pdf(np.linspace(-2, 2, 2*BLUR_RADIUS + 1))
    k = np.outer(x, x)
    data = convolve2d(data, k)

    def single_calculation(data: np.ndarray, matrix: np.ndarray) -> float:
        """Calculates the rotational deviation of a point cloud array with respect to 90° steps. Uses operator k.

        Args:
        ---
            data (np.ndarray): Point cloud array.
            matrix (np.ndarray): Complex operator matrix (Sobel, Scharr, Prewitt).

        Returns:
        ---
            float: Estimated deviation in degrees.
        """
        out = convolve2d(data, matrix, 'same')

        direction = ((np.angle(out)+pi/4)%(pi/2))-pi/4

        h, bins = np.histogram(direction, bins=binsIn)
        h = h.tolist()
        h[44] = 0
        angles = []

        m_sum = 0

        maxima = heapq.nlargest(5, h)
        for m in maxima:
            m_sum += m
            i = h.index(m)
            angles.append((bins[i]*180/pi + 0.5))

        return np.average(angles, weights=maxima)

    results = []

    for m in matrices:
        results.append(single_calculation(data, m))

    return -np.mean(results)