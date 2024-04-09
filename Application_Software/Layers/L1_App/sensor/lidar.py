from abc import ABC, abstractmethod

from Layers.L1_App.navigation.polar import Polar


class Lidar(ABC):
    """Represents Lidar device

    Raises:
    ---
        NotImplementedError: _description_

    Returns:
    ---
        _type_: _description_
    """
    radius: float
    
    def __init__(self, radius: float = 4.0) -> None:
        self.radius = radius

    @abstractmethod
    def get_point_cloud(self) -> list[Polar]:
        """Records and returns point cloud.

        Raises:
        ---
            NotImplementedError: [description]

        Returns:
        ---
            list[Polar]: Recorded point cloud.
        """
        raise NotImplementedError
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        self._radius = float(value)