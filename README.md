# Traffic Incident Routing Lab

A small incident-aware routing simulator for studying how closures and disruption penalties change route choice.

## Implemented
- directed road graph
- base travel time
- incident delay penalty
- road closures
- Dijkstra rerouting
- route-time summary
- deterministic tests

## Run
```bash
python -m unittest discover -s tests -v
python traffic_incident_routing_lab.py
```

Synthetic network only; this does not claim live traffic feeds, map-provider integration, or production dispatch.
