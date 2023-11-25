import math
import random
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
        self.transfering_data = False
        self.config = CONFIG

    def transfer_data(self) -> None:
        """Function to transfer data from sink node to UAVs"""
        time_for_transfer = random.uniform(
            self.config["min_communication_time"], self.config["max_communication_time"]
        )

        # transferance or data complete
        self.transfering_data = False

        return time_for_transfer

    def mark_for_transference(self) -> None:
        """Mark the sink node to transfer data"""
        self.transfer_data = True

    def get_cords(self) -> Tuple[float, float]:
        """Return the cordinates of the sink node

        Returns:
            Tuple[float,float]: The x and y cordinates
        """
        return self.x, self.y

    def distance(self, other) -> float:
        """Get distance of another sink node from this one

        Args:
            other (SinkNode): The other sink node

        Returns:
            float: The distance between the two sink node
        """
        x1, y1 = self.get_cords()
        x2, y2 = other.get_cords()
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
