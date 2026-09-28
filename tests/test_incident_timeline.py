import unittest

from incident_timeline import Incident, TimedRoad, TimedRoadNetwork


class IncidentTimelineTests(unittest.TestCase):
    def test_active_incident_changes_route(self):
        network = TimedRoadNetwork([
            TimedRoad("A", "B", 5, (Incident(8, 10, delay_minutes=10),)),
            TimedRoad("A", "C", 7),
            TimedRoad("C", "B", 2),
        ])
        self.assertEqual(network.route_at("A", "B", hour=9)["path"], ["A", "C", "B"])
        self.assertEqual(network.route_at("A", "B", hour=11)["path"], ["A", "B"])

    def test_active_closure_removes_road(self):
        network = TimedRoadNetwork([
            TimedRoad("A", "B", 1, (Incident(8, 10, closed=True),)),
            TimedRoad("A", "C", 2),
            TimedRoad("C", "B", 2),
        ])
        self.assertEqual(network.route_at("A", "B", hour=9)["travel_minutes"], 4)


if __name__ == "__main__":
    unittest.main()
