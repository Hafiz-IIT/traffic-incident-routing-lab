# Traffic Incident Routing Lab

> **A synthetic road-network lab for studying how closures and disruption penalties change route choice.**

The Smart City and logistics discussions repeatedly included traffic optimization and incident-aware routing. This repository isolates that algorithmic core so disruptions can be reproduced without claiming live map data.

## Implemented
- directed road graph
- base travel time
- incident delay penalties
- road closures
- Dijkstra rerouting
- path reconstruction
- travel-time summary

## Run
```bash
python -m unittest discover -s tests -v
python traffic_incident_routing_lab.py
```

## Repository map
`traffic_incident_routing_lab.py` core · `tests/` tests · `examples/` fixtures · `docs/architecture.md` design · `docs/research-agenda.md` experiments · `STATUS.md` claims · `CITATION.cff` citation

## Pipeline
**road network → incident state → edge travel times → shortest path → reroute → travel-time output**

## Research lineage
This is a focused descendant of Smart City, traffic optimization, WhatsApp/incident-service, and logistics-routing work.

## Evaluation direction
Vary incident severity, closures, network topology, and information delay. Later compare static rerouting against predictive or robust policies.

## Maturity
**Research prototype.** Synthetic graph only. No live traffic provider, GPS telemetry, map API, emergency dispatch, or deployed city service is claimed.
