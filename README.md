# Traffic Incident Routing Lab

<p align="center"><strong>Routing Through Changing Road Conditions</strong><br/><sub>Closures and delay incidents become explicit state, not hidden assumptions.</sub></p>

<p align="center"><img src="https://img.shields.io/badge/status-reproducible%20simulation-blue" alt="Simulation"/> <img src="https://img.shields.io/badge/focus-dynamic%20routing-orange" alt="Dynamic routing"/></p>

## Question

**When an incident changes the network, how should a route change—and can we explain why?**

```
Road graph
   +
Incident timeline
   ↓
Effective travel time / closure
   ↓
Shortest-path rerouting
   ↓
Path + travel-time explanation
```

## Try it

```bash
python traffic_incident_routing_lab.py
python -m unittest discover -s tests -v
```

`incident_timeline.py` supports time-bounded delays and closures and routes the network at a requested hour.

## Implemented

- directed road graph
- base travel times
- incident delay penalties
- time-bounded closures
- Dijkstra rerouting
- explicit unreachable handling
- deterministic CI

## Research boundary

A simulation laboratory, not a live traffic service or city-scale routing engine.

Related: [Logistics Optimization Lab](https://github.com/Hafiz-IIT/logistics-optimization-lab)
