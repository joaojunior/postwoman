import unittest
from dataclasses import dataclass

from postwoman.route import calculate_route


@dataclass
class Node():
    id: str
    latitude: float
    longitude: float


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.max_distance = 10

    def test_calculate_route_with_only_start_point(self):
        start_point = Node('s', 0, 0)
        expected = {
            'route': [{'id': start_point.id, 'type': 'Node',
                       'accumulated distance': 0}],
            'total_cost': 0
        }
        self.assertEqual(expected, calculate_route(
            start_point, [], [], self.max_distance))

    def test_calculate_route_with_start_point_and_letters(self):
        start_point = Node('s', 0, 0)
        letters = [Node('l1', 1, 0), Node('l2', 0, 1)]
        expected = {
            'route': [{'accumulated distance': 0, 'id': 's', 'type': 'Node'},
                      {'accumulated distance': 110.57438855779878,
                       'id': 'l1', 'type': 'Node'},
                      {'accumulated distance': 267.4739568491391,
                       'id': 'l2', 'type': 'Node'}],
            'total_cost': 267.4739568491391}
        self.assertEqual(expected, calculate_route(
            start_point, letters, [], self.max_distance))

    def test_calculate_route_with_start_point_letters_and_place_to_visit(self):
        start_point = Node('s', 0, 0)
        letters = [Node('l1', 1, 0), Node('l2', 0, 1)]
        places_to_visit = [Node('pv1', 1, 0), Node('pv2', 50, 50)]

        expected = {
            'route': [{'accumulated distance': 0, 'id': 's', 'type': 'Node'},
                      {'accumulated distance': 110.57438855779878,
                       'id': 'l1', 'type': 'Node'},
                      {'accumulated distance': 110.57438855779878,
                       'id': 'pv1', 'type': 'Node'},
                      {'accumulated distance': 267.4739568491391,
                       'id': 'l2', 'type': 'Node'}],
            'total_cost': 267.4739568491391}
        self.assertEqual(expected, calculate_route(
                start_point, letters, places_to_visit, self.max_distance))

    def test_calculate_route_with_error(self):
        """
        This test verify the error in calculate_route when the coordiantes
        aren't in the range allowed
        """
        start_point = Node('s', 0, 0)
        letters = [Node('l1', -100, 50), Node('l2', 0, 190)]
        places_to_visit = [Node('pv1', 1, 0), Node('pv2', 50, 50)]

        with self.assertRaises(ValueError):
            calculate_route(
                start_point, letters, places_to_visit, self.max_distance)
