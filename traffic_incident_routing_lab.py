from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import inf


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
        self.adj.setdefault(start, []).append(Road(end, base_minutes, delay, closed))

    def route(self, start: str, goal: str) -> dict:
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
