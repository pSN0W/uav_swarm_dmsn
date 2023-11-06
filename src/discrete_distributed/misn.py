import math
import random
from typing import Tuple,List, Set

from ..constants import CONFIG
from .sink_node import SinkNode


class MISN:

    def __init__(self) -> None:
        """Constructor
        """

        self.config = CONFIG
        self.num_sink_node = self.config['num_sink_node']
        self.sink_nodes = self.build_misn()

    def build_misn(self) -> List[SinkNode]:
        """Build a multiple isolated sensory network with the sink nodes

        Returns:
            list[SinkNode]: Sinknodes in the misn
        """

        points = []
        min_dist = self.config['min_dist_btw_sink_node']
        max_dist = self.config['max_dist_btw_sink_node']

        while len(points) < self.num_sink_node:
            point = self.generate_random_point()
            valid = True

            for existing_point in points:
                if min_dist <= self.distance(point,
                                             existing_point) <= max_dist:
                    valid = False
                    break

            if valid:
                points.append(point)

        return [SinkNode(point[0], point[1]) for point in points]
    
    def sink_node_classification(self, r: float) -> Tuple[List[Tuple[SinkNode,Set[SinkNode]]], List[Tuple[SinkNode,Set[SinkNode]]]]:
        """classifies non overlapping sinknode in high and low density regions

        Args:
            r (float): The projection of drone on grpund

        Returns:
            Tuple[List[Tuple[SinkNode,Set[SinkNode]]], List[Tuple[SinkNode,Set[SinkNode]]]: Set of High and Low sink nodes. In the list you keep the representative sink node and set of all points in its neighborhood
        """
        sink_node_neighborhood: List[Tuple[SinkNode,Set[SinkNode]]] = []
        
        # Add the sink nodes below distance r in same neighborhood
        for i,current_sink_node in enumerate(self.sink_nodes):
            current_sink_node_nbrhood = set([current_sink_node])
            for sink_node in self.sink_nodes[:i]:
                if self.distance(current_sink_node.get_location(),sink_node.get_location()) < r:
                    current_sink_node_nbrhood.add(sink_node)
            
            sink_node_neighborhood.append((current_sink_node,current_sink_node_nbrhood))
            
        # delete those sink node that are already part of other. 
        # Add nbrhood with more then 2 neighbors to high and other to low
        high_density_neighborhood: List[Set[SinkNode]] = []
        low_density_neighborhood: List[Set[SinkNode]] = []
        for curr_idx,curr_sink_node,current_sink_node_nbrhood in enumerate(sink_node_neighborhood):
            include = True
            for idx,_,sink_node_nbrhood in enumerate(sink_node_neighborhood):
                if idx != curr_idx and len(current_sink_node_nbrhood) == len(current_sink_node_nbrhood.intersection(sink_node_nbrhood)):
                    include = False
        if include:
            if len(current_sink_node_nbrhood) > 2:
                high_density_neighborhood.append((curr_sink_node,current_sink_node_nbrhood))
            else:
                low_density_neighborhood.append((curr_sink_node,current_sink_node_nbrhood))
        
        return high_density_neighborhood,low_density_neighborhood

    def generate_random_point(self) -> Tuple[float, float]:
        """generate a random point for misn

        Returns:
            list[float,float]: x,y cordinate for the sink node
        """

        max_allowed_cordinate = self.config[
            'max_dist_btw_sink_node'] * self.num_sink_node * 10

        return [
            random.uniform(0, max_allowed_cordinate),
            random.uniform(0, max_allowed_cordinate)
        ]

    def distance(point1: Tuple[float, float], point2: Tuple[float,
                                                          float]) -> float:
        """Distance between two point

        Args:
            point1 (list[float,float]): point 1
            point2 (list[float,float]): point 2

        Returns:
            float: eucladian distance between point1 and point 2
        """

        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
