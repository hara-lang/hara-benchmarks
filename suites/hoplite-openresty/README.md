# Hoplite HTTP benchmarks

This suite has two evidence tracks:

- `run.sh` is the controlled Hoplite versus OpenResty engineering benchmark.
- `external/the-benchmarker/` is a contribution scaffold for an independently maintained public HTTP suite.

The controlled lane should measure plaintext, route parameters, request/raw adapters, worker counts, latency percentiles, throughput, errors, idle/peak RSS, cold start and image size. Results from external suites must remain labelled with their own hardware and methodology rather than being mixed into the controlled aggregate.
