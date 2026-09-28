# Traffic Incident Routing Lab

> Incident-aware road-routing simulator supporting closures, delay penalties and dynamic rerouting.

## Status
**Reproducible prototype** with executable code, tests, CI, architecture, evaluation and roadmap documentation.

## Problem
Static shortest-path routing can fail during incidents. Closures and delay penalties need to change effective route cost without hiding why the route changed.

## Architecture
Directed road graph → incident state (delay/closure) → effective travel times → shortest-path rerouting → route and travel-time explanation.

## Run
```bash
python -m unittest discover -s tests -v
python traffic_incident_routing_lab.py
```

## Implemented
- Directed road graph
- Base travel time
- Incident delay penalty
- Closure flag
- Dijkstra rerouting
- Travel-time output
- Unreachable handling
- Tests and CI

## Research lineage
- *Smart Urban Infrastructures: AI-Enabled City Optimization*
- *AI for Climate Change: Modeling Micro-Level Energy Efficiency*
- *Reinforcement-Driven Optimization in Industrial AI*

## Evaluation
Tests confirm that incidents can change route choice and closures are respected.

## Limitations
- No live map feed
- No traffic prediction model
- Single-query routing
- No multi-vehicle congestion feedback yet

## License
MIT.

## Extended implementation

- `incident_timeline.py` adds time-bounded delays/closures and route selection at a requested hour.
