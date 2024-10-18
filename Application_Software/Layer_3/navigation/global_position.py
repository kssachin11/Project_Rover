from typing import TypeVar

from Layer_3.navigation.metric_position import MetricPosition

TGlobalPosition = TypeVar('TGlobalPosition', bound='GlobalPosition')

class GlobalPosition():
    """Represents a position in the geographic coordinate system."""
    longitude: float
    latitude: float
    height: float
    orientation: float
    
    
    def __init__(self, longitude: float, latitude: float, height: float, orientation: float) -> None:
        """Represents a position in the geographic coordinate system.

        Args:
        ---
            longitude (float): Geographic longitude.
            latitude (float): Geographic latitude.
            height (float): Height over mean sea level.
            orientation (float): Orientation in degrees, relative to north, clockwise.
            
        Returns:
        ----------
            None
        """
        self.longitude      = longitude
        self.latitude       = latitude
        self.height         = height
        self.orientation    = orientation
        
    
    def get_difference(self, pos: TGlobalPosition, gamma: float = 0) -> MetricPosition:
        """Returns:
        ---
            Difference between self and another geographic coordinate related to the rotation value gamma as a MetricPosition.
        """
        raise NotImplementedError
    
    @staticmethod
    def get_difference(pos1: TGlobalPosition, pos2: TGlobalPosition, gamma: float = 0) -> MetricPosition:
        """Returns:
        ---
            Difference between two geographic coordinates related to the rotation value gamma as a MetricPosition.
        """
        pos1.get_difference(pos2)
    
    def get_distance(self, pos: TGlobalPosition) -> float:
        """Returns:
        ---
            Distance between self and another geographic coordinate in meters.
        """
        return self.get_difference(pos).abs
    
    @staticmethod
    def get_distance(pos1: TGlobalPosition, pos2: TGlobalPosition) -> float:
        """Returns:
        ---
            Distance between two geographic coordinates in meters.
        """
        return pos1.get_distance(pos2)
        
        
    @property
    def longitude(self) -> float:
        """Returns:
        ----------
            float: Geographic longitude.
        """
        return self._longitude
    
    @longitude.setter
    def longitude(self, value: float) -> None:
        value = float(value)
        if value < -180 or value > 180: raise ValueError(f'{value} out of range -180 ... 180')
        self._longitude = value
        
        
    @property
    def latitude(self) -> float:
        """Returns:
        ----------
            float: Geographic latitude.
        """
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: float) -> None:
        value = float(value)
        if value < -90 or value > 90: raise ValueError(f'{value} out of range -90 ... 90')
        self._latitude = value
        
        
    @property
    def height(self) -> float:
        """Returns:
        ----------
            float: Height over mean sea level"""
        return self._height
    
    @height.setter
    def height(self, value: float) -> None:
        value = float(value)
        if value < -10000 or value > 10000: raise ValueError(f'{value} out of range -10000 ... 10000')
        self._height = value
        
        
    @property
    def orientation(self) -> float:
        """Returns:
        ----------
            float: Orientation in degrees, relative to north, clockwise.
        """
        return self._orientation
    
    @orientation.setter
    def orientation(self, value: float) -> None:
        value = float(value%360)
        self._orientation = value
        
        
    def __str__(self):
        """Returns:
        ----------
           str: String representation.
        """
        return f'longitude: {self.longitude}, latitude: {self.latitude}, height: {self.height}, orientation: {self.orientation}'
    
    def __add__(self, other: TGlobalPosition):
        """Addition of two positions.
    """
        return GlobalPosition(
            longitude=self.longitude+other.longitude,
            latitude=self.latitude+other.latitude,
            height=self.height+other.height,
            orientation=self.orientation+other.orientation,
        )
    
    def __sub__(self, other: TGlobalPosition):
        """Returns:
        ----------
            GlobalPosition: Subtraction of two positions.
        """
        return GlobalPosition(
            longitude=self.longitude-other.longitude,
            latitude=self.latitude-other.latitude,
            height=self.height-other.height,
            orientation=self.orientation-other.orientation,
        )
        
    def __mul__(self, num: float):
        """Returns:
        -------
            GlobalPosition: Multiplication of a position with a number. The value of each axis will be multiplied. The orientation value will remain the same.
        """
        num = float(num)
        return GlobalPosition(
            longitude=self.longitude*num,
            latitude=self.latitude*num,
            height=self.height*num,
            orientation=self.orientation
        )
        
    def __div__(self, num: float):
        """Returns:
        ----------
            GlobalPosition: Division of a position with a number. The value of each axis will be divided. The alpha value will remain the same.
        """
        num = float(num)
        return GlobalPosition(
            longitude=self.longitude/num,
            latitude=self.latitude/num,
            height=self.height/num,
            orientation=self.orientation
        )