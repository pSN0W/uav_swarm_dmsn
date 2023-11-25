import math
from typing import List

import numpy as np

from constants import CONFIG
from .misn import MISN
from .uav import UAV


class UAVSwarm:
    def __init__(self, misn: MISN) -> None:
        self.config = CONFIG
        self.misn = misn
        self.r = round(math.sqrt(CONFIG["radius"] ** 2 - CONFIG["height"] ** 2), 2)
        self.uavs = self.build_uav(
            center_x=0,
            center_y=0,
            edge_length=CONFIG["num_uav"],
            sides=CONFIG["radius"] * 2,
        )

    def generate_path_for_uav(self):
        best_route, best_distance = self.ant_colony_optimization(
            num_ants=self.config["num_ants"], num_iterations=self.config["num_epochs"]
        )

    def ant_colony_optimization(self, num_ants: int, num_iterations: int):
        cities = [sink_node for sink_node, _ in self.misn.sink_node_classification(self.r)]
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
            uavs.append(UAV(x=x_i, y=y_i, z=self.config["height"]))
        return uavs
