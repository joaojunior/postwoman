from typing import Dict, List
import heapq

from geopy.distance import geodesic


class Graph():
    def __init__(self):
        self.adjacents = {}
        self._graph = {}

    @property
    def nodes(self):
        return self.adjacents.keys()

    def add_arc(self, source, destination, cost: float):
        source_adjacents = self.adjacents.get(source.id, [])
        heapq.heappush(source_adjacents, (abs(cost), destination))
        self.adjacents[source.id] = source_adjacents


class Path():
    def __init__(self):
        self.visited = {}

    def calculate_simple_path(self, graph: Graph, start):
        self.graph = graph
        self.route = [(str(start.id), start.__class__.__name__, 0)]
        self.visited = {}
        self.total_cost = 0
        for node_id in self.graph.nodes:
            self.visited[node_id] = False
        self.visit(start.id)

        return {'route': self.route, 'total_cost': self.total_cost}

    def visit(self, node_id: str):
        self.visited[node_id] = True
        distance, next_node = self.get_next_nearby_node_not_visited(node_id)

        if next_node is not None:
            self.visited[next_node.id] = True
            self.total_cost += distance
            self.route.append((str(next_node.id), next_node.__class__.__name__,
                              self.route[-1][2] + distance))
            self.visit(next_node.id)

    def get_next_nearby_node_not_visited(self, node_id: str):
        adjacents = self.graph.adjacents.get(node_id, [])
        while adjacents:
            distance, next_node = heapq.heappop(adjacents)
            if self.visited[next_node.id] is False:
                return distance, next_node
        return 0, None


def calculate_distance(node1, node2):
    point1 = (node1.latitude, node1.longitude)
    point2 = (node2.latitude, node2.longitude)
    return geodesic(point1, point2).km


def create_graph(start_point, letters: List, places_to_visit: List,
                 max_distance: float):
    graph = Graph()
    start_point_and_letters = [start_point] + letters
    for i, source in enumerate(start_point_and_letters):
        for j, destination in enumerate(start_point_and_letters[i+1:]):
            distance = calculate_distance(source, destination)
            graph.add_arc(source, destination, distance)
            graph.add_arc(destination, source, distance)
    for i, source in enumerate(letters):
        for j, destination in enumerate(places_to_visit):
            distance = calculate_distance(source, destination)
            if distance <= max_distance:
                graph.add_arc(source, destination, distance)
            graph.add_arc(destination, source, distance)
    return graph


def calculate_route(start_point, letters: List, places_to_visit: List,
                    max_distance: float) -> Dict:
    graph = create_graph(start_point, letters, places_to_visit, max_distance)
    path = Path()
    return path.calculate_simple_path(graph, start_point)
