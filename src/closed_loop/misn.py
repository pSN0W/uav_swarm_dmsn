import math
import random
from typing import List, Set, Tuple

import tkinter as tk

from ..constants import CONFIG
from .sink_node import SinkNode


class MISN:
    def __init__(self, canvas: tk.Canvas) -> None:
        """Constructor"""

        self.config = CONFIG
        self.canvas = canvas
        
        self.num_sink_node = self.config["num_sink_node"]
        self.sink_nodes = self.build_misn()

    def build_misn(self) -> list[SinkNode]:
        """Build a multiple isolated sensory network with the sink nodes

        Returns:
            list[SinkNode]: Sinknodes in the misn
        """

        points = []
        min_dist = self.config["min_dist_btw_sink_node"]
        max_dist = self.config["max_dist_btw_sink_node"]

        while len(points) < self.num_sink_node:
            point = self.generate_random_point()
            valid = True

            for existing_point in points:
                if min_dist <= self.distance(point, existing_point) <= max_dist:
                    valid = False
                    break

            if valid:
                points.append(point)

        return [
            SinkNode(round(point[0], 2), round(point[1], 2), canvas=self.canvas)
            for point in points
        ]

    def sink_node_classification(
        self, r: float
    ) -> List[Tuple[SinkNode, Set[SinkNode]]]:
        """classifies non overlapping sinknode in high and low density regions

        Args:
            r (float): The projection of drone on grpund

        Returns:
            List[Tuple[SinkNode,Set[SinkNode]]:  In the list you keep the representative sink node and set of all points in its neighborhood
        """
        sink_node_neighborhood: List[Tuple[SinkNode, Set[SinkNode]]] = []

        # Add the sink nodes below distance r in same neighborhood
        for i, current_sink_node in enumerate(self.sink_nodes):
            current_sink_node_nbrhood = set([current_sink_node])
            for sink_node in self.sink_nodes[:i]:
                if current_sink_node.distance(sink_node) < r:
                    current_sink_node_nbrhood.add(sink_node)

            sink_node_neighborhood.append(
                (current_sink_node, current_sink_node_nbrhood)
            )
        print(sink_node_neighborhood)
        # delete those sink node that are already part of other.
        # Add nbrhood with more then 2 neighbors to high and other to low
        required_neighborhood: List[Set[SinkNode]] = []
        for curr_idx, (curr_sink_node, current_sink_node_nbrhood) in enumerate(
            sink_node_neighborhood
        ):
            include = True
            for idx, (_, sink_node_nbrhood) in enumerate(sink_node_neighborhood):
                if idx != curr_idx and len(current_sink_node_nbrhood) == len(
                    current_sink_node_nbrhood.intersection(sink_node_nbrhood)
                ):
                    include = False
            print(include)
            if include:
                required_neighborhood.append(
                    (curr_sink_node, current_sink_node_nbrhood)
                )
        return required_neighborhood

    def generate_random_point(self) -> list[float, float]:
        """generate a random point for misn

        Returns:
            list[float,float]: x,y cordinate for the sink node
        """

        max_allowed_cordinate = (
            self.config["max_dist_btw_sink_node"] * self.num_sink_node * 10
        )

        return [
            random.uniform(0, max_allowed_cordinate),
            random.uniform(0, max_allowed_cordinate),
        ]

    def distance(self, point1: list[float, float], point2: list[float, float]) -> float:
        """Distance between two point

               Args:
                   point1 (list[float,float]): point 1
                   point2 (list[float,float]): point 2

               Returns:
                   float:import time
        eucladian distance between point1 and point 2
        """

        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __repr__(self) -> str:
        return f"MISN({','.join([str(node) for node in self.sink_nodes])})"
