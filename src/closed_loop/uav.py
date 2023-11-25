import multiprocessing as mp
import tkinter as tk

from ..constants import CONFIG
from .sink_node import SinkNode


class UAV:
    def __init__(
        self, canvas: tk.Canvas, x: float, y: float, z: float, r: float
    ) -> None:
        """Constructor

        Args:
            canvas(tk.Canvas): tkinter canvas
            x (float): x cordinate for UAV
            y (float): y cordinate of UAV
            z (float): z cordinate of UAV
            r (float): projection on ground
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        
        size = self.r/3
        self.square_id = canvas.create_rectangle(
            x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill="red"
        )
        self.circle_id = canvas.create_oval(
            x - self.r, y - self.r, x + self.r, y + self.r, outline="green", width=2
        )

    def move(self, delta_x: float, delta_y: float) -> None:
        """Move the UAV to a new cordinate

        Args:
            delta_x (float): delta in x to move
            delta_y (float): delta in y to move
        """
        self.x += delta_x
        self.y += delta_y
        self.canvas.move(self.square_id,delta_x, delta_y)
        self.canvas.move(self.circle_id,delta_x, delta_y)
    
    def extract_data_from_node(self, sink_node: SinkNode) -> None:
        """Extract data from sink node

        Args:
            sink_node (SinkNode): Sink Node
        """
        sink_node.transfer_data()

    def accept_data(self, sink_nodes: list[SinkNode]) -> None:
        """Transsfer data from the drone

        Args:
            sink_nodes (list[SinkNode]): Sink nodes in range of UAV
        """
        with mp.Pool(len(sink_nodes)) as pool:
            pool.map(self.extract_data_from_node, sink_nodes)
