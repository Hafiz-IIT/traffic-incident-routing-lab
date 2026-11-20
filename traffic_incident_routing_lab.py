from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
from math import inf


def _finite_nonnegative(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite non-negative number")
    return float(value)


@dataclass(frozen=True)
class Road:
    to: str
    base_minutes: float
    incident_delay_minutes: float = 0.0
    closed: bool = False

    def __post_init__(self):
        if not isinstance(self.to, str) or not self.to.strip():
            raise ValueError("destination must be a non-empty string")
        _finite_nonnegative("base_minutes", self.base_minutes)
        _finite_nonnegative("incident_delay_minutes", self.incident_delay_minutes)
        if not isinstance(self.closed, bool):
            raise ValueError("closed must be boolean")

    @property
    def travel_minutes(self) -> float:
        total = self.base_minutes + self.incident_delay_minutes
        if not math.isfinite(total):
            raise OverflowError("road travel time is not finite")
        return total


class RoadNetwork:
    def __init__(self):
        self.adj: dict[str, list[Road]] = {}

    def add_road(self, start: str, end: str, base_minutes: float, *, delay: float = 0.0, closed: bool = False) -> None:
        if not isinstance(start, str) or not start.strip():
            raise ValueError("start must be a non-empty string")
        self.adj.setdefault(start, []).append(Road(end, base_minutes, delay, closed))

    def route(self, start: str, goal: str) -> dict:
        if not isinstance(start, str) or not start.strip() or not isinstance(goal, str) or not goal.strip():
            raise ValueError("start and goal must be non-empty strings")
        if start == goal:
            return {"path": [start], "travel_minutes": 0.0}
        dist = {start: 0.0}
        prev: dict[str, str] = {}
        queue = [(0.0, start)]

        while queue:
            current, node = heapq.heappop(queue)
            if current != dist.get(node):
                continue
            if node == goal:
                break
            for road in self.adj.get(node, []):
                if road.closed:
                    continue
                candidate = current + road.travel_minutes
                if candidate < dist.get(road.to, inf):
                    dist[road.to] = candidate
                    prev[road.to] = node
                    heapq.heappush(queue, (candidate, road.to))

        if goal not in dist:
            raise ValueError("no route available")

        path = [goal]
        node = goal
        while node != start:
            node = prev[node]
            path.append(node)
        path.reverse()
        return {"path": path, "travel_minutes": dist[goal]}


if __name__ == "__main__":
    # Demonstrate the time-dependent earliest-arrival model, not only the
    # legacy departure-snapshot baseline above.
    from incident_timeline import Incident, TimedRoad, TimedRoadNetwork

    network = TimedRoadNetwork([
        TimedRoad("A", "B", 60),
        TimedRoad("B", "D", 10, (Incident(1, 2, delay_minutes=30),)),
        TimedRoad("A", "C", 75),
        TimedRoad("C", "D", 10),
    ])
    print(network.route_at("A", "D", hour=0))
