import tkinter as tk

from src.closed_loop.misn import MISN
from src.closed_loop.swarm import UAVSwarm
from src.constants import CONFIG


if __name__ == "__main__":
    edge_length = CONFIG["max_dist_btw_sink_node"] * CONFIG['num_sink_node'] * 10 + 10

    root = tk.Tk()
    root.title("UAV Swarm Optimization Algorithm")

    canvas = tk.Canvas(
        root,
        width=edge_length,
        height=edge_length,
        bg="white",
    )
    canvas.pack()
    misn = MISN(canvas=canvas)
    uav_swarm = UAVSwarm(
        misn=misn,
        canvas=canvas
    )
    print(len(uav_swarm.uavs))

    root.mainloop()
