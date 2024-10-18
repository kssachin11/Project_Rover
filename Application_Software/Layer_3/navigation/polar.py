from typing import TypeVar
from typing import List
import numpy as np
from typing import List



TPolar = TypeVar('TPolar', bound='Polar')

class Polar():
    """Representation of a polar coordinate."""
    def __init__(self, phase: float, abs: float, turn: str = None, movement: float = 0) -> None:
        """Polar coordinates.
        
        Args:
        ---
            phase (float): Angle in degrees.
            abs (float): Distance.
            turn (str, optional): Turn type, e.g., "left" or "right". Defaults to None.
        """
        self.phase = phase
        self.abs = abs
        self.turn = turn
        self.movement = movement

        
    def __lt__(self, other) -> bool:
        return self.abs < other.abs
        
    def __le__(self, other) -> bool:
        return self.abs <= other.abs
        
    def __gt__(self, other) -> bool:
        return self.abs > other.abs
        
    def __ge__(self, other) -> bool:
        return self.abs >= other.abs
    
    def __str__(self) -> str:
        return f'abs: {self.abs}, arg: {self.phase}'
    
    def rotate(self, angle: float) -> TPolar:
        return Polar(phase=self.phase + angle, abs=self.abs)
        
    def __mul__(self, factor: float) -> TPolar:
        if factor >= 0: return Polar(phase=self.phase, abs=self.abs * factor)
        else: return Polar(phase=(self.phase + 180) % 360, abs=self.abs * -factor)
        
    def from_array(cls, coords: np.ndarray) -> List[TPolar]:
        """Create a list of Polar instances from a numpy array."""
        return [cls(abs=coord[0], phase=coord[1], movement=coord[2], turn=coord[3]) for coord in coords]
        
    
        
    @classmethod
    def from_array(cls, coords: List[List]) -> List[TPolar]:
        for i in range(len(coords)):
            coords[i] = cls(abs=coords[i][0], phase=coords[i][1])
        return coords
