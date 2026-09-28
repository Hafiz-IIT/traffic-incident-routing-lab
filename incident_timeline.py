from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import inf


@dataclass(frozen=True)
class Incident:
    start_hour: float
    end_hour: float
    delay_minutes: float = 0.0
    closed: bool = False

    def active(self, hour: float) -> bool:
        return self.start_hour <= hour < self.end_hour


@dataclass(frozen=True)
class TimedRoad:
    start: str
    end: str
    base_minutes: float
    incidents: tuple[Incident, ...] = ()

    def state_at(self, hour: float) -> tuple[bool, float]:
        closed = False
        delay = 0.0
        for incident in self.incidents:
            if incident.active(hour):
                closed = closed or incident.closed
                delay += incident.delay_minutes
        return closed, self.base_minutes + delay


class TimedRoadNetwork:
    def __init__(self, roads: list[TimedRoad]):
        self.roads = list(roads)

    def route_at(self, start: str, goal: str, *, hour: float) -> dict:
        adj: dict[str, list[tuple[str, float]]] = {}
        for road in self.roads:
            closed, minutes = road.state_at(hour)
            if not closed:
                adj.setdefault(road.start, []).append((road.end, minutes))

        dist = {start: 0.0}
        prev: dict[str, str] = {}
        queue = [(0.0, start)]

        while queue:
            cost, node = heapq.heappop(queue)
            if cost != dist.get(node):
                continue
            if node == goal:
                break
            for nxt, minutes in adj.get(node, []):
                candidate = cost + minutes
                if candidate < dist.get(nxt, inf):
                    dist[nxt] = candidate
                    prev[nxt] = node
                    heapq.heappush(queue, (candidate, nxt))

        if goal not in dist:
            raise ValueError("no route available")

        path = [goal]
        node = goal
        while node != start:
            node = prev[node]
            path.append(node)
        path.reverse()
        return {"path": path, "travel_minutes": dist[goal], "hour": hour}
