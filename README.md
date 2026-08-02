# Hara Benchmarks

This repository is the reproducible performance laboratory for
[Hara](https://github.com/hara-lang/hara). It keeps benchmark machinery out of
the language implementation while preserving the exact Hara revision, runtime
versions, platform, raw samples, and unsupported features behind every chart.

Published results: **https://benchmarks.hara-lang.org**

## What is measured

The initial corpus covers recursive control flow, backtracking, permutation,
integer-heavy algorithms, array mutation, persistent data structures, matrix
work, runtime startup/warm-up, native and Wasm boundaries, and the Hoplite HTTP
interface. Runtime adapters currently cover Hara's interpreter, bytecode,
tracing, whole-function Wasm and Truffle lanes alongside C, Java, Python,
LuaJIT, Babashka, SBCL, Chez and Guile where supported.

Each normalized result can report:

- process cold start, first call, warm-up samples and steady-state samples;
- p50/p95 and coefficient of variation derived from raw nanosecond samples;
- peak resident memory, executable/artifact size and compressed size;
- explicit `unsupported` results with a reason, never a substituted workload;
- absolute Hara time and a pairwise ratio between Hara and each reference
  runtime over their common successful workloads.

Hosted CI is useful comparative evidence, not a stable performance laboratory.
Pull requests therefore gate correctness and schema validity, while trends are
published without failing a change because a shared runner was noisy.

## Quick start

```sh
git clone https://github.com/hara-lang/hara
git clone https://github.com/hara-lang/hara-benchmarks
cd hara-benchmarks
python3 -m unittest discover -v
python3 -m hara_bench run --suite algorithms --profile smoke --hara-root ../hara
python3 -m hara_bench validate data
python3 -m hara_bench build-site
```

The language coordinators also accept larger `algorithm` and `standard`
profiles. Automation maps these to three tiers:

| Tier | Trigger | Platforms | Purpose |
|---|---|---|---|
| smoke | pull request/push | Ubuntu | correctness and a short representative sample |
| nightly | schedule/manual | Ubuntu x86-64, macOS arm64 | complete ordinary corpus and history |
| weekly | schedule/manual | Ubuntu x86-64, macOS arm64 | expensive cold-start, memory and boundary repetitions |

## Repository map

- `suites/language/` — general algorithms and language adapters
- `suites/runtime/` — Hara tier, startup and warm-up comparisons
- `suites/boundary/` — host/Wasm call-boundary measurements
- `suites/hoplite-openresty/` — HTTP/FFI integration measurements
- `adapters/` — shared runtime-specific adapters
- `schema/` — stable normalized result contract
- `hara_bench/` — CLI, normalization, validation and site builder
- `site/` — dependency-free static dashboard
- `data/` — seed/current data on `main`; long history is on `benchmarks-data`

## Result integrity

Workloads must return their expected value before timing is accepted. Collection
benchmarks must preserve equivalent semantics (for example mutable object/array
work is not labelled as a persistent-map comparison). A result file is
append-only evidence: reruns use a new run id and attempt rather than overwriting
history.

## Dashboard views

The published observatory leads with Hara's absolute results and shows neutral,
pairwise comparisons between Hara and each reference runtime. Overall and
category ratios use the geometric mean of the common successful workload set
for that individual pair; coverage and unsupported features remain visible.
Lifecycle and code views compare Hara with one selected reference while keeping
exact source, preparation commands, runtime versions, and run provenance.

See each suite README for runtime prerequisites and methodology.
