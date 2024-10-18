# The MetricPosition class represents a position in a 3D Cartesian coordinate system and provides
# methods for addition, subtraction, multiplication, and division of positions.
from math import sqrt
from typing import TypeVar   
from typing import List


TMetricPosition = TypeVar('TMetricPosition', bound='MetricPosition')

    
    
class MetricPosition():
    """Represents a position in a 3D Cartesian coordinate system."""
    x: float
    y: float
    z: float
    alpha: float
    
    def __init__(self, x: float, y: float, z: float, alpha: float) -> None:
        """Represents a position in a 3D Cartesian coordinate system.

        Args:
        ---
            x (float): x-coordinate
            y (float): y-coordinate
            z (float): z-coordinate
            alpha (float): alpha-coordinate
        """
        self.x      = x
        self.y      = y
        self.z      = z
        self.alpha  = alpha
        
        
    def getCoordinates(self) -> List[float]:
        """Returns list of coordinates
        
        Returns:
        ---
            list[float]: list of coordinates.
        """
        return [self.x, self.y, self.z, self.alpha]
    
    @property
    def abs(self) -> float:
        """Return the absolute distance of this position."""
        return sqrt(self.x**2 + self.y**2 + self.z**2)
        
        
    @property
    def x(self) -> float:
        """x-coordinate."""
        return self._x
    
    @x.setter
    def x(self, value: float) -> None:
        value = float(value)
        self._x = value
        
        
    @property
    def y(self) -> float:
        """y-coordinate."""
        return self._y
    
    @y.setter
    def y(self, value: float) -> None:
        value = float(value)
        self._y = value
        
        
    @property
    def z(self) -> float:
        """z-coordinate."""
        return self._z
    
    @z.setter
    def z(self, value: float) -> None:
        value = float(value)
        self._z = value
        
        
    @property
    def alpha(self) -> float:
        """Orientation according to Cartesian coordinate system."""
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: float) -> None:
        value = float(value%360)
        self._alpha = value
        
        
    def __str__(self) -> str:
        """String representation."""
        return f'x: {self.x}, y: {self.y}, z: {self.z}, alpha: {self.alpha}'
    
    def __add__(self, other: TMetricPosition):
        """Addition of two positions."""
        return MetricPosition(
            x=self.x+other.x,
            y=self.y+other.y,
            z=self.z+other.z,
            alpha=self.alpha+other.alpha,
        )
    
    def __sub__(self, other: TMetricPosition):
        """Subtraction of two positions."""
        return MetricPosition(
            x=self.x-other.x,
            y=self.y-other.y,
            z=self.z-other.z,
            alpha=self.alpha-other.alpha,
        )
        
    def __mul__(self, num: float):
        """Multiplication of a position with a number. The value of each axis will be multiplied. The alpha value will remain the same."""
        num = float(num)
        return MetricPosition(
            x=self.x*num,
            y=self.y*num,
            z=self.z*num,
            alpha=self.alpha
        )
        
    def __truediv__(self, num: float):
        """Division of a position with a number. The value of each axis will be divided. The alpha value will remain the same."""
        num = float(num)
        return MetricPosition(
            x=self.x/num,
            y=self.y/num,
            z=self.z/num,
            alpha=self.alpha
        )
