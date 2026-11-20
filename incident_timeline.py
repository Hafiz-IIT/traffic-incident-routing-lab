from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import inf, isfinite


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} must be a finite number")
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
        if end <= start or delay < 0:
            raise ValueError("incident end must follow start and delay must be non-negative")
        if not isinstance(self.closed, bool):
            raise ValueError("closed must be a boolean")

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
        if any(not isinstance(value, str) or not value.strip() for value in (self.start, self.end)):
            raise ValueError("road endpoints must be non-empty strings")
        if _finite("base_minutes", self.base_minutes) < 0:
            raise ValueError("base travel time must be non-negative")
        if not isinstance(self.incidents, tuple) or any(not isinstance(item, Incident) for item in self.incidents):
            raise ValueError("incidents must be a tuple of Incident values")

    def state_at(self, hour: float) -> tuple[bool, float]:
        hour = _finite("hour", hour)
        closed = False
        delay = 0.0
        for incident in self.incidents:
            if incident.active(hour):
                closed = closed or incident.closed
                delay += incident.delay_minutes
        total = self.base_minutes + delay
        if not isfinite(total):
            raise OverflowError("incident-adjusted travel time is not finite")
        return closed, total


class TimedRoadNetwork:
    def __init__(self, roads: list[TimedRoad]):
        if not isinstance(roads, list) or any(not isinstance(road, TimedRoad) for road in roads):
            raise ValueError("roads must be a list of TimedRoad instances")
        self.roads = list(roads)
        self.adj: dict[str, list[TimedRoad]] = {}
        for road in self.roads:
            self.adj.setdefault(road.start, []).append(road)

    @staticmethod
    def _earliest_edge_arrival(road: TimedRoad, available_hour: float) -> tuple[float, float, float] | None:
        # With waiting allowed, the earliest arrival on an edge is attained at
        # the current time or at an incident boundary where its state changes.
        available_hour = _finite("available_hour", available_hour)
        candidates = {available_hour}
        for incident in road.incidents:
            if incident.start_hour >= available_hour:
                candidates.add(incident.start_hour)
            if incident.end_hour >= available_hour:
                candidates.add(incident.end_hour)

        best = None
        for entry_hour in sorted(candidates):
            closed, driving_minutes = road.state_at(entry_hour)
            if closed:
                continue
            arrival_hour = entry_hour + driving_minutes / 60.0
            if best is None or arrival_hour < best[1]:
                best = (entry_hour, arrival_hour, driving_minutes)
        return best

    def route_at(self, start: str, goal: str, *, hour: float) -> dict:
        """Find the earliest-arrival route, allowing waits for incident changes.

        Incident state is sampled when a road is entered. An incident that begins
        after entry does not interrupt an in-progress traversal. Waiting is
        allowed at nodes; this makes the edge-arrival function FIFO for Dijkstra.
        """
        if any(not isinstance(value, str) or not value.strip() for value in (start, goal)):
            raise ValueError("route endpoints must be non-empty strings")
        hour = _finite("departure hour", hour)
        if start == goal:
            return {"path": [start], "travel_minutes": 0.0, "driving_minutes": 0.0,
                    "waiting_minutes": 0.0, "departure_hour": hour, "arrival_hour": hour}

        arrival = {start: hour}
        previous: dict[str, tuple[str, float, float]] = {}
        queue = [(hour, start)]

        while queue:
            current_arrival, node = heapq.heappop(queue)
            if current_arrival != arrival.get(node):
                continue
            if node == goal:
                break
            for road in self.adj.get(node, []):
                edge = self._earliest_edge_arrival(road, current_arrival)
                if edge is None:
                    continue
                entry_hour, candidate_arrival, driving_minutes = edge
                if candidate_arrival < arrival.get(road.end, inf):
                    arrival[road.end] = candidate_arrival
                    previous[road.end] = (node, entry_hour, driving_minutes)
                    heapq.heappush(queue, (candidate_arrival, road.end))

        if goal not in arrival:
            raise ValueError("no route available")

        path = [goal]
        driving = 0.0
        waiting = 0.0
        node = goal
        while node != start:
            parent, entry_hour, driving_minutes = previous[node]
            waiting += max(0.0, (entry_hour - arrival[parent]) * 60.0)
            driving += driving_minutes
            path.append(parent)
            node = parent
        path.reverse()
        total = (arrival[goal] - hour) * 60.0
        return {
            "path": path,
            "travel_minutes": round(total, 6),
            "driving_minutes": round(driving, 6),
            "waiting_minutes": round(waiting, 6),
            "departure_hour": hour,
            "arrival_hour": arrival[goal],
        }
