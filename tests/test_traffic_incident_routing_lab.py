import unittest

from traffic_incident_routing_lab import RoadNetwork


class TrafficRoutingTests(unittest.TestCase):
    def test_incident_can_change_route(self):
        n = RoadNetwork()
        n.add_road("A", "B", 5, delay=10)
        n.add_road("A", "C", 7)
        n.add_road("C", "B", 2)
        self.assertEqual(n.route("A", "B")["path"], ["A", "C", "B"])

    def test_closed_road_ignored(self):
        n = RoadNetwork()
        n.add_road("A", "B", 1, closed=True)
        n.add_road("A", "C", 2)
        n.add_road("C", "B", 2)
        self.assertEqual(n.route("A", "B")["travel_minutes"], 4)

    def test_unreachable_raises(self):
        n = RoadNetwork()
        with self.assertRaises(ValueError):
            n.route("A", "B")


if __name__ == "__main__":
    unittest.main()
