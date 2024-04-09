from abc import ABC, abstractmethod


class Gyroscope(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def get_rotation(self) -> list[float, float, float]:
        """Gets and returns rotation data from sensor.

        Raises:
        ---
            NotImplementedError: function not yet implemented

        Returns:
        ---
            list[float, float, float]: list of rotation speeds [x, y, z] in degrees/s
        """
        raise NotImplementedError
        return []
    
    def get_x_rotation(self) -> float:
        """Gets and return rotation speed around x-axis.

        Returns:
        ---
            float: rotation speed around x-axis in degrees/s
        """
        return self.get_rotation()[0]
    
    def get_y_rotation(self) -> float:
        """Gets and return rotation speed around y-axis.

        Returns:
        ---
            float: rotation speed around y-axis in degrees/s
        """
        return self.get_rotation()[1]
    
    def get_z_rotation(self) -> float:
        """Gets and return rotation speed around z-axis.

        Returns:
        ---
            float: rotation speed around z-axis in degrees/s
        """
        return self.get_rotation()[2]
    
    
    @abstractmethod
    def get_orientation(self) -> list[float, float, float]:
        """Gets and returns orientation from sensor.

        Raises:
        ---
orientation NotImplementedError: function not degrees
        Returns:
        ---
            list[float, float, float]: list of speed values [x, y, z] in degrees
        """
        raise NotImplementedError
        return []
    
    def get_x_orientation(self) -> float:
        """Gets and return orientation in x-axis.

        Returns:
        ---
            float: orientation value around x-axis in degrees
        """
        return self.get_orientation()[0]
    
    def get_y_orientation(self) -> float:
        """Gets and return orientation in y-axis.

        Returns:
        ---
            float: orientation value around y-axis in degrees
        """
        return self.get_orientation()[1]
    
    def get_z_orientation(self) -> float:
        """Gets and return orientation in z-axis.

        Returns:
        ---
            float: orientation value around z-axis in degrees
        """
        return self.get_orientation()[2]
    
    def set_orientation(self, orientation: list[float, float, float] = None) -> None:
        if not orientation: orientation = [0, 0, 0]
        self.set_x_orientation(self, orientation[0])
        self.set_y_orientation(self, orientation[1])
        self.set_z_orientation(self, orientation[2])
        
    def set_x_orientation(self, orientation: float = 0) -> None:
        raise NotImplementedError
        
    def set_y_orientation(self, orientation: float = 0) -> None:
        raise NotImplementedError
        
    def set_z_orientation(self, orientation: float = 0) -> None:
        raise NotImplementedError