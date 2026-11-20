# Routing model and limitations

Road travel times must be positive and incident delays non-negative. Incident intervals are half-open: active at `start_hour`, inactive at `end_hour`.

The time-aware router evaluates incident states at the requested departure hour and then runs a static shortest-path search. It does **not** integrate changing road conditions during a vehicle's traversal. A trip that crosses an incident start/end boundary is still scored using the departure-time snapshot. Results are therefore departure-time snapshots, not a fully time-dependent shortest-path solution.
