# Architecture

Directed road graph → incident state (delay/closure) → effective travel times → shortest-path rerouting → route and travel-time explanation.

## Invariants
1. Closed roads must never be traversed.
2. Incident delay must affect effective travel time.
3. Unreachable destinations must be reported explicitly.
