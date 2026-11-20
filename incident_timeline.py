from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import inf, isfinite


@dataclass(frozen=True)
class Incident:
    start_hour: float
    end_hour: float
    delay_minutes: float = 0.0
    closed: bool = False

    def __post_init__(self) -> None:
        if not isfinite(float(self.start_hour)) or not isfinite(float(self.end_hour)):
            raise ValueError("incident time bounds must be finite")
        if self.end_hour <= self.start_hour:
            raise ValueError("incident end_hour must be after start_hour")
        if not isfinite(float(self.delay_minutes)) or self.delay_minutes < 0:
            raise ValueError("incident delay must be finite and non-negative")
        if not isinstance(self.closed, bool):
            raise ValueError("closed must be boolean")

    def active(self, hour: float) -> bool:
        return self.start_hour <= hour < self.end_hour


@dataclass(frozen=True)
class TimedRoad:
    start: str
    end: str
    base_minutes: float
    incidents: tuple[Incident, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.start, str) or not self.start.strip() or not isinstance(self.end, str) or not self.end.strip():
            raise ValueError("road endpoints must be non-empty strings")
        if not isfinite(float(self.base_minutes)) or self.base_minutes <= 0:
            raise ValueError("base_minutes must be finite and positive")
        if any(not isinstance(item, Incident) for item in self.incidents):
            raise ValueError("incidents must contain Incident values")

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
        if any(not isinstance(road, TimedRoad) for road in roads):
            raise ValueError("roads must contain TimedRoad values")
        self.roads = list(roads)

    def route_at(self, start: str, goal: str, *, hour: float) -> dict:
        if not isinstance(start, str) or not start.strip() or not isinstance(goal, str) or not goal.strip():
            raise ValueError("start and goal must be non-empty strings")
        if not isfinite(float(hour)):
            raise ValueError("hour must be finite")
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
