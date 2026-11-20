# Routing model and assumptions

## Static routing
RoadNetwork uses Dijkstra over non-negative static travel-time weights. Closed roads are omitted from the graph search.

## Time-dependent routing
TimedRoadNetwork computes earliest arrival with waiting allowed at nodes. Each road's delay/closure state is sampled when the road is entered; a closure beginning after entry does not interrupt a traversal. Candidate entry times are the current arrival time and the boundaries of incident intervals. This is a piecewise-constant, deterministic model.

## Assumptions
- Travel times and incident intervals are deterministic and known.
- Waiting at nodes is permitted.
- Road travel time is non-negative.
- A road's incident state is constant during an individual traversal.
- The model has no turn restrictions, vehicle classes, road capacity, stochastic traffic, spatial geometry, or live feeds.

## Interpretation
The output is a model result under these assumptions, not a real traffic ETA. The incident schedule is a fixture, not a live source.
