import math
import random

from constants import CONFIG
from sink_node import SinkNode


class MISN:
    def __init__(self) -> None:
        """Constructor"""

        self.config = CONFIG
        self.num_sink_node = self.config["num_sink_node"]
        self.sink_nodes = self.build_misn()

    def get_sink_node_in_range(
        self, uav_projection: list[float, float], max_dist: float
    ) -> list[SinkNode]:
        """Get all the sink node that are inside a distance max_dist from the projection

        Args:
            uav_projection (list[float,float]): The projection of UAV on the ground
            max_dist (float): Distance from projection to include the sink node

        Returns:
            list[SinkNode]: Nodes that are inside the area
        """
        nodes_covered: list[SinkNode] = []

        for node in self.sink_nodes:
            sink_node_loc = [node.x, node.y]
            if (
                self.distance(sink_node_loc, uav_projection) <= max_dist
                and not node.mark_for_transference
            ):
                nodes_covered.append(node)

        return nodes_covered

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

        return [SinkNode(point[0], point[1]) for point in points]

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

    def distance(point1: list[float, float], point2: list[float, float]) -> float:
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
