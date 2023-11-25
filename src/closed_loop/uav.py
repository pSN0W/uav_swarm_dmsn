import multiprocessing as mp

from ..constants import CONFIG
from .sink_node import SinkNode


class UAV:
    def __init__(
        self, canvas: "Canvas", x: float, y: float, z: float, r: float, size:int = 20
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
        self.square_id = canvas.create_rectangle(
            x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill="red"
        )
        self.circle_id = canvas.create_oval(
            x - size, y - size, x + size, y + size, outline="green", width=2
        )

    def move(self, delta_x: float, delta_y: float, delta_z: float) -> None:
        """Move the UAV to a new cordinate

        Args:
            delta_x (float): delta in x to move
            delta_y (float): delta in y to move
            delta_z (float): delta in z to move
        """
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

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
