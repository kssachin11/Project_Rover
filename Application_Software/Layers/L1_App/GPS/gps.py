from abc import ABC, abstractmethod
from Layers.L1_App.navigation.global_position import GlobalPosition
from Layers.L1_App.navigation.metric_position import MetricPosition


class GPS(ABC):
    """Representation of GPS-receiver. Contains methods for reading data from receiver."""
    origin: GlobalPosition = None
    
    def __init__(self) -> None:
        """Representation of GPS-receiver. Contains methods for reading data from receiver.
            
        Returns:
        ----------
            None
        """
        self.origin = self.get_position()

    @abstractmethod
    def get_position(self) -> GlobalPosition:
        """Reads and returns position from receiver.

        Raises:
        ---
            NotImplementedError: Not yet implemented.

        Returns:
        ---
            GlobalPosition: Position, detected by sensor.
        """
        raise NotImplementedError

    def set_origin(self, position: GlobalPosition = None) -> None:
        """Sets origin to actual or individual coordinate.

        Args:
        ---
            position (GlobalPosition, optional): Position to be set. Defaults to None.
            
        Returns:
        ----------
            None
        """
        self.origin = position if position else self.get_position()

    def get_relative_position(self, gamma: float = 0.0) -> MetricPosition:
        """Calculates relative coordinate related to the defined origin and the rotation value gamma.

        Args:
        ---
            gamma (float, optional): Actual orientation. Defaults to 0.0.

        Raises:
        ---
            OriginNotSetError: Origin not set.

        Returns:
        ---
            MetricPosition: Relative coordinate related to the defined origin and the rotation value gamma.
        """
        if not self.origin: raise OriginNotSetError
        GlobalPosition.getDifference(self.origin, self.get_position())
    
class OriginNotSetError(Exception):
    """Origin not set yet.

    Args:
    ---
        Exception ([type]): [description] 
    """
    pass