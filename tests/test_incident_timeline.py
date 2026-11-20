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

    def test_incidents_are_evaluated_when_each_road_is_entered(self):
        network = TimedRoadNetwork([
            TimedRoad("A", "B", 60),
            TimedRoad("B", "D", 10, (Incident(1, 2, delay_minutes=30),)),
            TimedRoad("A", "C", 75),
            TimedRoad("C", "D", 10),
        ])
        result = network.route_at("A", "D", hour=0)
        self.assertEqual(result["path"], ["A", "C", "D"])
        self.assertEqual(result["travel_minutes"], 85)

    def test_waiting_until_road_reopens_is_counted(self):
        network = TimedRoadNetwork([
            TimedRoad("A", "B", 10, (Incident(0, 1, closed=True),)),
        ])
        result = network.route_at("A", "B", hour=0)
        self.assertEqual(result["waiting_minutes"], 60)
        self.assertEqual(result["driving_minutes"], 10)
        self.assertEqual(result["travel_minutes"], 70)

    def test_nan_and_boolean_time_values_are_rejected(self):
        for value in (float("nan"), True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Incident(value, value + 1)
        with self.assertRaises(ValueError):
            TimedRoad("A", "B", float("inf"))

    def test_invalid_incident_and_road_values_are_rejected(self):
        with self.assertRaises(ValueError):
            Incident(2, 1)
        with self.assertRaises(ValueError):
            TimedRoad("A", "B", -1)


if __name__ == "__main__":
    unittest.main()
