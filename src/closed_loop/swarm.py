import math
from typing import List
import time

import numpy as np
import tkinter as tk

from ..constants import CONFIG
from .misn import MISN
from .uav import UAV


class UAVSwarm:
    def __init__(self, misn: MISN, canvas: tk.Canvas) -> None:
        self.x = 50
        self.y = 50
        self.speed = 30
        self.time_of_move = 100
        self.canvas = canvas

        self.config = CONFIG
        self.r = round(math.sqrt(CONFIG["radius"] ** 2 - CONFIG["height"] ** 2), 2)
        self.uavs = self.build_uav(
            center_x=self.x,
            center_y=self.y,
            edge_length=CONFIG["radius"] * 2,
            sides=CONFIG["num_uav"],
        )

        self.misn = misn
        self.node_classification = self.misn.sink_node_classification(self.r)
        self.time_of_transfer_at_node = self.get_wait_time_at_each_misn()
        self.nbr_of_node = {
            node: list(node_nbrhood) for node, node_nbrhood in self.node_classification
        }

        self.path = self.generate_path_for_uav()[:-1]
        self.misn_to_reach_idx = 0
        self.move()

    def get_wait_time_at_each_misn(self):
        time_to_transfer = {
            sink_node: sink_node.time_for_transfer
            for sink_node, _ in self.node_classification
        }
        for sink_node, sink_node_nbrhood in self.node_classification:
            for nbr in list(sink_node_nbrhood):
                time_to_transfer[sink_node] = max(
                    [time_to_transfer[sink_node], nbr.time_for_transfer]
                )
        return time_to_transfer

    def generate_path_for_uav(self):
        best_route, best_distance = self.ant_colony_optimization(
            num_ants=self.config["num_ants"], num_iterations=self.config["num_epochs"]
        )
        print("Minimum distance required ", best_distance)
        for sinknode1, sinknode2 in zip(best_route[:-1], best_route[1:]):
            x1, y1 = sinknode1.get_cords()
            x2, y2 = sinknode2.get_cords()
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=5, arrow=tk.LAST)
        return best_route

    def ant_colony_optimization(self, num_ants: int, num_iterations: int):
        cities = [sink_node for sink_node, _ in self.node_classification]
        best_tour = None
        best_distance = math.inf
        for iteration in range(num_iterations):
            ants = []
            for ant in range(num_ants):
                ant_tour = [cities[np.random.randint(len(cities))]]
                unvisited_cities = cities.copy()
                unvisited_cities.remove(ant_tour[0])
                while len(unvisited_cities) > 0:
                    current_city = ant_tour[-1]
                    next_city = self.find_nearest_city(current_city, unvisited_cities)
                    ant_tour.append(next_city)
                    unvisited_cities.remove(next_city)
                ants.append(ant_tour)

            for ant_tour in ants:
                total_distance = self.calculate_total_distance(ant_tour)
                if total_distance < best_distance:
                    best_tour = ant_tour.copy()
                    best_distance = total_distance

        # Add the starting city to the end of the tour
        best_tour.append(best_tour[0])

        return best_tour, best_distance

    def calculate_total_distance(self, tour):
        total_distance = 0
        for i in range(len(tour)):
            if i == len(tour) - 1:
                next_city = tour[0]
            else:
                next_city = tour[i + 1]
            total_distance += tour[i].distance(next_city)
        return total_distance

    def find_nearest_city(self, current_city, unvisited_cities):
        nearest_city = None
        nearest_distance = math.inf
        for city in unvisited_cities:
            current_distance = current_city.distance(city)
            if current_distance < nearest_distance:
                nearest_city = city
                nearest_distance = current_distance
        return nearest_city

    def build_uav(
        self, center_x: float, center_y: float, edge_length: float, sides: int
    ) -> List[UAV]:
        uavs = []

        angle_increment = 360 / sides

        # Calculate the radius (distance from the center to a vertex)
        radius = edge_length / (2 * math.sin(math.radians(180 / sides)))

        for i in range(sides):
            angle_rad = math.radians(i * angle_increment)
            x_i = center_x + radius * math.cos(angle_rad)
            y_i = center_y + radius * math.sin(angle_rad)
            uavs.append(
                UAV(
                    x=round(x_i, 2),
                    y=round(y_i, 2),
                    z=self.config["height"],
                    canvas=self.canvas,
                    r=self.r,
                )
            )
        return uavs

    def get_next_move(self):
        to_reach = self.path[self.misn_to_reach_idx].get_cords()
        dist_x = to_reach[0] - self.x
        dist_y = to_reach[1] - self.y
        distance = math.sqrt(dist_x**2 + dist_y**2)
        if distance > self.speed / 2:
            unit_direction_x = dist_x / distance
            unit_direction_y = dist_y / distance
            delta_x, delta_y = (
                self.speed * unit_direction_x,
                self.speed * unit_direction_y,
            )
            self.x += delta_x
            self.y += delta_y
            return delta_x, delta_y
        else:
            for node in self.nbr_of_node[self.path[self.misn_to_reach_idx]]:
                node.mark_for_transference()
            time.sleep(self.time_of_transfer_at_node[self.path[self.misn_to_reach_idx]])
            for node in self.nbr_of_node[self.path[self.misn_to_reach_idx]]:
                node.complete_transfer()

            self.misn_to_reach_idx += 1
            if self.misn_to_reach_idx == len(self.path):
                self.misn_to_reach_idx = 0
            return self.get_next_move()

    def move(self):
        delta_x, delta_y = self.get_next_move()
        if delta_x is None:
            return
        for uav in self.uavs:
            uav.move(delta_x, delta_y)
        self.canvas.after(self.time_of_move, self.move)
