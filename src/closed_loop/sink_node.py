import random
import time

from constants import CONFIG

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
        """Function to transfer data from sink node to UAVs
        """
        time_for_transfer = random.uniform(
            self.config['min_communication_time'],
            self.config['max_communication_time'])
        
        # transferance or data complete
        self.transfering_data = False
        
        return time_for_transfer
        
    def mark_for_transference(self) -> None:
        """Mark the sink node to transfer data
        """
        self.transfer_data = True
