import math
import numpy as np

from ..constants import CONFIG

# Define a function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

class MinSwarmOptimizer:
    def __init__(self, misn) -> None:
        self.height = CONFIG['height']
        self.radius = CONFIG['radius']
        self.misn = misn
        self.sink_nodes_location = self.get_sink_nodes_cordinates()
        self.distances = self.distance_matrix()
        
    # Perform hierarchical clustering using the single-linkage method
    def get_num_required_uav(self):
        data = self.sink_nodes_location
        distances = self.distances
        num_samples = len(data)
        clusters = [[i] for i in range(num_samples)]
        num_uav = 0
        
        while len(clusters) > 1:
            min_dist = float('inf')
            merge_clusters = (0, 0)
            
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    cluster1 = clusters[i]
                    cluster2 = clusters[j]
                    d = min(distances[p1][p2] for p1 in cluster1 for p2 in cluster2)
                    if d < min_dist:
                        min_dist = d
                        merge_clusters = (i, j)
            
            i, j = merge_clusters
            num_uav += math.ceil(min_dist/2*self.radius)
            clusters[i].extend(clusters[j])
            del clusters[j]
        
        return num_uav
        
    def get_sink_nodes_cordinates(self):
        high_density,low_density = self.misn.sink_node_classification((self.radius**2-self.height**2)**1/2)
        high_density_cords = [sink_node.get_location() for sink_node,_ in high_density]
        low_density_cords = [sink_node.get_location() for sink_node,_ in low_density]
        return high_density_cords + low_density_cords
    
    # Define a function to calculate the distance matrix
    def distance_matrix(self):
        data = self.sink_nodes_location
        n = len(data)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                dist_matrix[i, j] = euclidean_distance(data[i], data[j])
                dist_matrix[j, i] = dist_matrix[i, j]
        
        return dist_matrix
    # Define a function to calculate the distance matrix
    def distance_matrix(data):
        n = len(data)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                dist_matrix[i, j] = euclidean_distance(data[i], data[j])
                dist_matrix[j, i] = dist_matrix[i, j]
        
        return dist_matrix