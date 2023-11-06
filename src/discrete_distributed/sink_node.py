from typing import Tuple

from ..constants import CONFIG
class SinkNode:
    def __init__(self, x: float, y: float) -> None:
        """Constructor for a sink node

        Args:
            x (float): x cordinate of the sink node
            y (float): y cordinate of the sink node
        """

        self.x = x
        self.y = y
    
    def get_location(self)->Tuple[float,float]:
        """Returns the x and y cordinate of sink node

        Returns:
            Tuple[float,float]: the x,y cordinates
        """
        return (self.x,self.y)
    
    def __eq__(self, __value: object) -> bool:
        return self.get_location() == __value.get_location()
    
    def __hash__(self) -> int:
        return hash(self.get_location())
