import tkinter as tk

from src.closed_loop.misn import MISN
from src.closed_loop.swarm import UAVSwarm
from src.constants import CONFIG


def draw_triangle(canvas, x, y, size=20):
    x1, y1 = x - size / 2, y + size / 2
    x2, y2 = x + size / 2, y + size / 2
    x3, y3 = x, y - size / 2

    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="blue")


if __name__ == "__main__":
    edge_length = CONFIG["max_dist_btw_sink_node"] * CONFIG['num_sink_node'] * 10 + 10
    misn = MISN()

    root = tk.Tk()
    root.title("UAV Swarm Optimization Algorithm")

    canvas = tk.Canvas(
        root,
        width=edge_length,
        height=edge_length,
        bg="white",
    )
    canvas.pack()
    uav_swarm = UAVSwarm(
        misn=misn,
        canvas=canvas
    )
    print(len(uav_swarm.uavs))
    # Draw triangles at specified coordinates
    for node in misn.sink_nodes:
        draw_triangle(canvas, *node.get_cords())

    root.mainloop()
