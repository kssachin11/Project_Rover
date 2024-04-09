from typing import TypeVar


TPolar = TypeVar('TPolar', bound='Polar')

class Polar():
    """Representation of a polar coordinate."""
    def __init__(self, abs: float, phase: float) -> None:
        """Representation of a polar coordinate.

        Args:
        ----
            abs (float): coordinates absolute value [m]
            phase (float): coordinates phase/argument [deg]
        """
        self.abs = abs
        self.phase = phase
        
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
        
    @classmethod
    def from_array(cls, coords: list[list]) -> list[TPolar]:
        for i in range(len(coords)):
            coords[i] = cls(abs=coords[i][0], phase=coords[i][1])
        return coords