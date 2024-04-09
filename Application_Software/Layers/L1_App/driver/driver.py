from abc import ABC, abstractmethod


class Driver(ABC):
    
    @abstractmethod
    def drive_right(self, angle: float, radius: float, speed: float = 100.0) -> None:
        """Bot drives to right hand side.

        Args:
            angle (float): curve angle
            radius (float): curve radius
            speed (float, optional): speed in %. Range: -100...100 . Defaults to 100.0.
        """
        pass
    
    @abstractmethod
    def drive_left(self, angle: float, radius: float, speed: float = 100.0) -> None:
        """Bot drives to left hand side.

        Args:
            angle (float): curve angle
            radius (float): curve radius
            speed (float, optional): speed in %. Range: -100...100 . Defaults to 100.0.
        """
        pass
    
    @abstractmethod
    def turn_right(self, angle: float, speed: float = 100.0) -> None:
        """Bot turns right.

        Args:
            angle (float): angle to rotate
            speed (float, optional): speed in %. Range: 0...100 . Defaults to 100.0.
        """
        pass
    
    @abstractmethod
    def turn_left(self, angle: float, speed: float = 100.0) -> None:
        """Bot turns left.

        Args:
            angle (float): angle to rotate
            speed (float, optional): speed in %. Range: 0...100 . Defaults to 100.0.
        """
        pass