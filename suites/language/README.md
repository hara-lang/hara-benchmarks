# Language corpus

The language corpus answers three separate questions rather than producing one undifferentiated league table.

## In-class dynamic JIT

Measured now:

- Hara whole-Wasm
- LuaJIT
- PyPy, using the identical Python source used by CPython
- Node.js / V8, using explicit JavaScript implementations of the shared algorithms
- Ruby / YJIT, with YJIT required rather than inferred from the Ruby build
- Clojure / HotSpot, using the identical Clojure source used by Babashka

## Lisp family

Measured now:

- Hara
- SBCL
- Chez Scheme
- GNU Guile
- Babashka
- Clojure / HotSpot

Racket CS is the next Lisp-family addition.

## References and baselines

- C is the ahead-of-time native reference.
- Java / HotSpot is the managed JIT reference.
- CPython is the familiar dynamic interpreter baseline.

C and Java remain visible, but are categorised and coloured separately from Hara's in-class dynamic-JIT comparison.

## Modes

- `prepared` measures already parsed/compiled work and is the primary steady-state comparison.
- `eval` includes source evaluation and remains a lifecycle result.
- C and Java are prepared-only because their compiler step is recorded separately.

## Node.js / V8 lane

`node_workloads.json` contains one idiomatic JavaScript implementation for every workload in the shared corpus. `node_runner.mjs` compiles the selected source into a benchmark function and then invokes it repeatedly in one Node process, allowing the warm-up samples to expose V8 optimisation rather than hiding it behind a single aggregate. Every run records:

- the exact Node and V8 versions
- process cold start
- source compilation and first-call cost
- warm-up samples and convergence
- steady-state timing
- peak RSS
- Node executable size
- source bytes

The canonical lane pins Node 24 LTS rather than following the moving Current release.

## Ruby / YJIT lane

`ruby_workloads.json` contains an idiomatic Ruby implementation for each shared workload. `ruby_runner.rb` is always invoked through `ruby --yjit` and exits with an error unless `RubyVM::YJIT.enabled?` is true. The prepared lane evaluates source once, resolves the benchmark method and then samples repeated calls so compilation and warm-up remain visible. Every run records:

- the exact Ruby release and YJIT-enabled state
- process cold start
- source evaluation and first-call cost
- warm-up samples and convergence
- steady-state timing
- peak RSS
- Ruby executable size
- source bytes

Ruby is pinned to 4.0.6 in canonical CI. RSS remains a first-class result because YJIT intentionally consumes extra memory for generated code and metadata.

## Clojure lane

The Clojure runner wraps each `bb_source` form in a zero-argument function, compiles it through Clojure 1.12.5, and invokes it repeatedly in one JVM so HotSpot can optimise hot paths. Dependency resolution is primed before startup measurement. The result records:

- process cold start
- preparation and first-call cost
- warm-up samples and convergence
- steady-state timing
- peak RSS
- Clojure dependency-classpath size
- source bytes

Because Babashka and Clojure consume the same source field, their difference is the host/runtime rather than a rewritten algorithm.

## Resource collection

`run_resources.py` wraps the existing coordinator with `/usr/bin/time`, records peak RSS, runtime executable size, runtime bundle size and source size, and adds the PyPy, Node, Ruby and Clojure adapters. The normalized schema keeps source, runtime, bundle, generated artifact and image sizes separate.
