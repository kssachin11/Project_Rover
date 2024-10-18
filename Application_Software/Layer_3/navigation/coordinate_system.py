from typing import TypeVar

from Layer_3.navigation.metric_position import MetricPosition


TCoordinateSystem = TypeVar('TCoordinateSystem', bound='CoordinateSystem')

class CoordinateSystem():
    """A class, providing information about the coordinate system, coordinates are referring to.
    """
    def __init__(self, origin: list[float, float], orientation: float) -> None:
        """Constructor of CoordinateSystem().

        Args:
        ---
            origin (list[float, float]): geographic coordinates of coordinate systems origin
            orientation (float): orientation of the coordinate system in degrees 
            
        Returns:
        ----------
            None
        """        
        self.origin = origin
        self.orientation = orientation
        
    @property
    def origin(self) -> list[float, float]:
        return self._origin
    
    @origin.setter
    def origin(self, value) -> None:
        if len(value) != 2: raise ValueError(f'{value} not fitting for list[float, float]')
        value[0] = float(value[0])
        value[1] = float(value[1])
        self._origin = value
        
    @property
    def orientation(self) -> float:
        return self._orientation
    
    @orientation.setter
    def orientation(self, value) -> None:
        value = float(value)
        self._orientation = value
        
    def transform(self, coordinateSystem: TCoordinateSystem, coordinate: MetricPosition) -> MetricPosition:
        """Transforms a coordinate from a different coordinate System to its own coordinate system.

        Args:
        ---
            coordinateSystem (CoordinateSystem): coordinates original coordinate system
            coordinate (MetricPosition): coordinate in original coordinate system

        Raises:
        ---
            NotImplementedError: function not yet implemented

        Returns:
        ---
            MetricPosition: coordinate in this coordinate system
        """
        raise NotImplementedError
        return MetricPosition()