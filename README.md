# Hara Performance Observatory

Reproducible, inspectable performance evidence for Hara and Hoplite, published at `benchmarks.hara-lang.org`.

The observatory is deliberately not a single global ranking. It presents Hara through separate comparison classes:

- **In-class dynamic JIT:** Hara, LuaJIT and PyPy now; Node/V8, Ruby/YJIT and Clojure/HotSpot next.
- **Lisp family:** Hara, SBCL, Chez Scheme, GNU Guile and Babashka; Clojure and Racket CS next.
- **Reference ceilings:** C as the native reference and Java/HotSpot as the managed reference.
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

The resource-aware coordinator requires `/usr/bin/time`. PyPy is measured with the exact same source as CPython.

## Canonical GitHub evidence

The scheduled workflow runs inside an Ubuntu 24.04 job container with fixed CPU and memory limits. Validated runs are uploaded as workflow artifacts and then promoted to the `benchmarks-data` branch. A push to either `main` or `benchmarks-data` rebuilds GitHub Pages from the current site code plus the durable run history.

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
