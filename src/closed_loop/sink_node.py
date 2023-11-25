import math
import random
from typing import Tuple

import tkinter as tk

from ..constants import CONFIG


class SinkNode:
    def __init__(self, x: float, y: float, canvas: tk.Canvas) -> None:
        """Constructor for a sink node

        Args:
            x (float): x cordinate of the sink node
            y (float): y cordinate of the sink node
        """
        self.canvas = canvas

        self.x = x
        self.y = y
        self.config = CONFIG

        self.transfering_data = False
        self.time_for_transfer = random.uniform(
            self.config["min_communication_time"], self.config["max_communication_time"]
        )
        self.triangle_id = self.draw_triangle(self.x, self.y)

    def draw_triangle(self, x, y, size=20):
        x1, y1 = x - size / 2, y + size / 2
        x2, y2 = x + size / 2, y + size / 2
        x3, y3 = x, y - size / 2

        return self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="blue")

    def mark_for_transference(self) -> None:
        """Mark the sink node to transfer data"""
        self.transfer_data = True
        self.canvas.itemconfig(self.triangle_id, fill="yellow")
        self.canvas.update()

    def complete_transfer(self):
        self.transfer_data = False
        self.canvas.itemconfig(self.triangle_id, fill="blue")
        self.canvas.update()

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

    def __repr__(self) -> str:
        return f"SinkNode {self.get_cords()}"
