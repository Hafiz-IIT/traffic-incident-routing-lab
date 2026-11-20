from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import inf, isfinite


@dataclass(frozen=True)
class Road:
    to: str
    base_minutes: float
    incident_delay_minutes: float = 0.0
    closed: bool = False

    @property
    def travel_minutes(self) -> float:
        return self.base_minutes + self.incident_delay_minutes


class RoadNetwork:
    def __init__(self):
        self.adj: dict[str, list[Road]] = {}

    def add_road(self, start: str, end: str, base_minutes: float, *, delay: float = 0.0, closed: bool = False) -> None:
        if not isinstance(start, str) or not start.strip() or not isinstance(end, str) or not end.strip():
            raise ValueError("road endpoints must be non-empty strings")
        if not isfinite(float(base_minutes)) or base_minutes <= 0:
            raise ValueError("base_minutes must be finite and positive")
        if not isfinite(float(delay)) or delay < 0:
            raise ValueError("delay must be finite and non-negative")
        if not isinstance(closed, bool):
            raise ValueError("closed must be boolean")
        self.adj.setdefault(start, []).append(Road(end, float(base_minutes), float(delay), closed))

    def route(self, start: str, goal: str) -> dict:
        if not isinstance(start, str) or not start.strip() or not isinstance(goal, str) or not goal.strip():
            raise ValueError("start and goal must be non-empty strings")
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
    n = RoadNetwork()
    n.add_road("A", "B", 5, delay=10)
    n.add_road("A", "C", 7)
    n.add_road("C", "B", 2)
    print(n.route("A", "B"))
