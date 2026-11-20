from __future__ import annotations
from dataclasses import dataclass
import heapq
from math import inf, isfinite

def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)

@dataclass(frozen=True)
class Incident:
    start_hour: float
    end_hour: float
    delay_minutes: float = 0.0
    closed: bool = False
    def __post_init__(self):
        start = _finite("start_hour", self.start_hour)
        end = _finite("end_hour", self.end_hour)
        delay = _finite("delay_minutes", self.delay_minutes)
        if start >= end: raise ValueError("incident end_hour must be after start_hour")
        if delay < 0: raise ValueError("delay_minutes must be non-negative")
        if not isinstance(self.closed, bool): raise ValueError("closed must be boolean")
    def active(self, hour: float) -> bool:
        hour = _finite("hour", hour)
        return self.start_hour <= hour < self.end_hour

@dataclass(frozen=True)
class TimedRoad:
    start: str
    end: str
    base_minutes: float
    incidents: tuple[Incident, ...] = ()
    def __post_init__(self):
        if not isinstance(self.start, str) or not self.start.strip() or not isinstance(self.end, str) or not self.end.strip():
            raise ValueError("road endpoints must be non-empty strings")
        if _finite("base_minutes", self.base_minutes) < 0:
            raise ValueError("base_minutes must be non-negative")
        if not isinstance(self.incidents, tuple) or any(not isinstance(i, Incident) for i in self.incidents):
            raise ValueError("incidents must be a tuple of Incident values")
    def state_at(self, hour: float) -> tuple[bool, float]:
        hour = _finite("hour", hour)
        closed, delay = False, 0.0
        for incident in self.incidents:
            if incident.active(hour):
                closed = closed or incident.closed
                delay += incident.delay_minutes
        return closed, self.base_minutes + delay

class TimedRoadNetwork:
    def __init__(self, roads: list[TimedRoad]):
        if not isinstance(roads, list) or any(not isinstance(r, TimedRoad) for r in roads):
            raise ValueError("roads must be a list of TimedRoad values")
        self.roads = list(roads)
    def route_at(self, start: str, goal: str, *, hour: float) -> dict:
        if not isinstance(start, str) or not start.strip() or not isinstance(goal, str) or not goal.strip():
            raise ValueError("start and goal must be non-empty strings")
        hour = _finite("hour", hour)
        if start == goal: return {"path": [start], "travel_minutes": 0.0, "hour": hour}
        adj: dict[str, list[tuple[str, float]]] = {}
        for road in self.roads:
            closed, minutes = road.state_at(hour)
            if not closed: adj.setdefault(road.start, []).append((road.end, minutes))
        dist, prev, queue = {start: 0.0}, {}, [(0.0, start)]
        while queue:
            cost, node = heapq.heappop(queue)
            if cost != dist.get(node): continue
            if node == goal: break
            for nxt, minutes in adj.get(node, []):
                candidate = cost + minutes
                if candidate < dist.get(nxt, inf):
                    dist[nxt], prev[nxt] = candidate, node
                    heapq.heappush(queue, (candidate, nxt))
        if goal not in dist: raise ValueError("no route available")
        path, node = [goal], goal
        while node != start:
            node = prev[node]
            path.append(node)
        path.reverse()
        return {"path": path, "travel_minutes": dist[goal], "hour": hour}
