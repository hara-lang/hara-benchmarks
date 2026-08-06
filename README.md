# Hara Performance Observatory

Reproducible, inspectable performance evidence for Hara and Hoplite, published at `https://www.hara-lang.org/benchmarks/`.

The observatory is deliberately not a single global ranking. It presents Hara through separate comparison classes, then exposes the complete prepared field in a drill-down language shootout:

- **In-class dynamic JIT:** Hara, LuaJIT, PyPy, Node.js/V8, Ruby/YJIT and Clojure/HotSpot.
- **Lisp family:** Hara, SBCL, Chez Scheme, GNU Guile, Babashka and Clojure/HotSpot; Racket CS next.
- **Reference ceilings:** Rust and C as native references, and Java/HotSpot as the managed reference.
- **Interpreter baseline:** CPython and small-startup runtimes where useful.
- **HTTP:** a controlled Hoplite/OpenResty suite plus independently maintained public framework suites.

See [`docs/benchmark-strategy.md`](docs/benchmark-strategy.md) for the positioning, language programme and fairness rules.

## Evidence model

Every successful measurement can record:

- cold process total, preparation, first call, warm-up and steady-state samples;
- p50, p95, variability, convergence and verified operation counts;
- peak and idle RSS;
- source, generated artifact and compressed artifact size;
- runtime executable and runtime bundle size; and
- deployable container image size.

These dimensions remain separate. A tiny source file is not evidence of a tiny deployed runtime.

## Run locally

Check out Hara beside this repository or pass its path explicitly:

```sh
python -m hara_bench run \
  --suite algorithms \
  --profile smoke \
  --hara-root ../hara

python -m hara_bench import-language \
  results/local/language.json \
  results/local/normalized.json

python -m hara_bench validate results/local/normalized.json
python -m hara_bench build-site --data data --output dist
```

The resource-aware coordinator requires `/usr/bin/time`. PyPy is measured with the exact same source as CPython. Clojure/HotSpot is measured with the exact same Clojure forms as Babashka, using pinned Clojure dependencies and a separately reported JVM dependency bundle. Node.js is pinned to the Node 24 LTS line and records the underlying V8 version with every run. Ruby is pinned to Ruby 4.0.6, invokes every benchmark with `--yjit`, and refuses to publish if YJIT is unavailable or disabled. Rust is a prepared-only native lane: each workload is compiled with optimised `rustc`, its checksum is verified, and compiler time remains separate from repeated calls.

## Canonical GitHub evidence

Relevant pushes to `main` run the complete 14-lane prepared peer set inside an Ubuntu 24.04 job container with fixed CPU and memory limits. This includes every measured dynamic-JIT peer, every measured Lisp-family runtime, Rust, C, Java and CPython, but excludes source-eval and experimental Hara-tier lanes. Nightly and weekly schedules retain the larger lifecycle matrix. Validated runs are uploaded as workflow artifacts and promoted to the `benchmarks-data` branch automatically. A push to either `main` or `benchmarks-data` rebuilds GitHub Pages from the current site code plus the durable run history.

Hosted-runner results are comparative evidence. Machine identity, revisions, runtime versions and container identity remain attached to every run so results are not presented as universal absolutes.

## HTTP benchmarks

`./suites/hoplite-openresty/run.sh` is the controlled engineering lane. The contribution scaffold for The Benchmarker lives under:

```text
suites/hoplite-openresty/external/the-benchmarker/
```

TechEmpower is retained as a historical methodology reference, not an active submission target.

## Data contract

Normalized runs use [`schema/run.schema.json`](schema/run.schema.json). The current schema version is 3; older version 1 and 2 evidence remains readable.

## License

MIT License.
