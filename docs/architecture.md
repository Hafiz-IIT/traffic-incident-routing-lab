# Architecture

```mermaid
flowchart LR
    N0[road network] --> N1
    N1[incident state] --> N2
    N2[edge travel times] --> N3
    N3[shortest path] --> N4
    N4[reroute] --> N5
    N5[travel-time output]
```

## Road model
Directed edges carry base travel time, incident delay, and closure state.

## Incident layer
Disruption changes effective edge cost or removes the edge.

## Router
Dijkstra finds the current minimum-travel-time path.

## Output
Returns route and total travel minutes for auditability.

## Principle
Make incident effects explicit in edge costs so route changes can be explained.
