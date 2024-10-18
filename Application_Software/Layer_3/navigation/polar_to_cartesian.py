from math import ceil, cos, pi, sin
from matplotlib import pyplot as plt
import numpy as np
from Layer_3.navigation.calculate_deviation import calculate_deviation
from typing import List


from Layer_3.navigation.polar import Polar


def polar_to_cartesian(point_cloud_polar: List[Polar], resolution: float = 0.1, alignment_iterations: int = 20) -> List[np.ndarray]:
    """Generates and aligns Cartesian array from polar point cloud. 

    Args:
    ---
        point_cloud_polar (list[Polar]): Point cloud.
        resolution (float, optional): Point Clouds resolution. Defaults to 0.1.
        alignment_iterations (int, optional): Maximum iterations for the alignment process. Defaults to 20.

    Returns:
    ---
        list[np.ndarray, np.ndarray, float]: 
            1. Cartesian point cloud.
            2. Position in this point cloud.
            3. Estimated rotational offset with respect to next 90° step.
    """
    radius = ceil(sorted(point_cloud_polar, reverse=True)[0].abs)  # radius of coordinate with largest abs
    offset = ceil(radius/resolution)                    # offset to center position in array
    dimensions = [[offset, offset], [offset, offset]]
    rotationOffset = 0

    output = [180, 0, 0, 0]

    for _ in range(alignment_iterations):
        data = np.zeros(shape=[2*offset + 1, 2*offset + 1], dtype=int)
        for c in point_cloud_polar:
            x = round((c.abs / resolution + resolution) * sin((c.phase + rotationOffset) * pi / 180)) + offset
            y = round((c.abs / resolution + resolution) * cos((c.phase + rotationOffset) * pi / 180)) + offset

            if x < 0: x = 0
            elif x > 2*offset: x = 2*offset
            if y < 0: y = 0
            elif y > 2*offset: y = 2*offset

            if dimensions[0][0] > x: dimensions[0][0] = x
            elif dimensions[0][1] <= x: dimensions[0][1] = x + 1
            if dimensions[1][0] > y: dimensions[1][0] = y
            elif dimensions[1][1] <= y: dimensions[1][1] = y + 1

            data[int(x-1):int(x+2), int(y-1):int(y+2)] = 1

        cd = calculate_deviation(data)
        newOutput = [abs(cd), data, ((rotationOffset + 45)%90)-45, dimensions]
        if newOutput[0] < output[0]: output = newOutput

        rotationOffset += cd

        if abs(cd) < 0.3: break

    _, data, rotationOffset, dimensions = output

    dimensions[0][0] = max(dimensions[0][0] - 5, 0)
    dimensions[1][0] = max(dimensions[1][0] - 5, 0)
    
    dimensions[0][1] = min(dimensions[0][1] + 5, data.shape[0] - 1)
    dimensions[1][1] = min(dimensions[1][1] + 5, data.shape[1] - 1)

    data = data[int(dimensions[0][0]):int(dimensions[0][1]), int(dimensions[1][0]):int(dimensions[1][1])]
    position = [offset - dimensions[0][0], offset - dimensions[1][0]]
    
    return [data, np.array(position), rotationOffset]
