# Hara benchmark strategy

## Positioning

Hara should be evaluated first as a **dynamic language with adaptive execution**, not as a replacement for C. The dashboard therefore separates five questions:

1. **In class:** how Hara compares with dynamic languages that use a JIT.
2. **Lisp family:** how Hara compares with mature Lisp and Scheme implementations.
3. **Reference ceilings:** how far Hara is from native C and managed Java on the same work.
4. **Lifecycle cost:** what is paid for parsing, compilation, warm-up and first use.
5. **Deployment cost:** peak RSS, idle RSS, runtime/bundle size, generated artifact size and container image size.

C and Java stay visible, but they are rendered with reference colours and never included in an “in-class” aggregate.

## Runtime programme

### Measured now

| Lane | Runtime | Reason |
| --- | --- | --- |
| In class | Hara whole-Wasm | Product runtime under test. |
| In class | LuaJIT | Small, mature dynamic tracing JIT and a strong footprint comparator. |
| In class | PyPy | Reuses the exact Python implementations while replacing CPython with a tracing JIT. |
| In class + Lisp | Clojure / HotSpot | Runs the exact Clojure forms used by Babashka, with JVM warm-up, RSS and dependency-bundle size recorded separately. |
| Lisp | SBCL | High-performance Common Lisp implementation. |
| Lisp | Chez Scheme | Mature native-code Scheme implementation. |
| Lisp | GNU Guile | Dynamic Scheme implementation with a different runtime profile. |
| Lisp | Babashka | Small-startup Clojure-compatible baseline. |
| Baseline | CPython | Familiar dynamic interpreter baseline. |
| Reference | C | Ahead-of-time native ceiling. |
| Reference | Java / HotSpot | Mature managed-JIT ceiling. |

### Add next

1. **Node.js / V8** — the most recognisable dynamic-JIT reference and important for server-side adoption comparisons.
2. **Ruby / YJIT** — a dynamic object model with a modern production JIT; useful because its memory trade-off should be visible.
3. **Racket CS** — broadens the Lisp lane without pretending every Lisp has the same execution model.

PHP JIT and Julia should wait. PHP is dominated by request lifecycle/framework behaviour, while Julia specialises around numerical compilation and would pull the corpus away from Hara's general dynamic-language claim.

## Fair-comparison rules

- Compare only equivalent modes: prepared with prepared, eval with eval.
- Use the same checksum and operation count for every implementation.
- Keep language implementations idiomatic but prohibit algorithm substitutions.
- Record unsupported workloads rather than silently replacing them.
- Publish every runtime version, compiler flag, source, harness, Hara revision and benchmark revision.
- Use geometric means only over pairwise common workloads; never impute missing results.
- Show absolute values alongside ratios.
- Treat GitHub-hosted numbers as comparative evidence, not laboratory-grade absolute records.

## Metrics

### Execution

- cold process total
- preparation / compile time
- first call
- warm-up trace
- steady-state p50 and p95
- coefficient of variation and convergence window
- throughput derived from verified operation counts

### Footprint

- peak resident set size for each measured process
- idle resident set size for server runtimes
- runtime executable size
- runtime bundle/dependency size where a single executable is misleading
- source bytes
- generated artifact bytes and compressed artifact bytes
- OCI image compressed and unpacked size for deployable products

No single “smallest” score should mix these dimensions. A language can have a tiny source artifact and a large runtime, or the reverse.

## GitHub execution and publication

The canonical public lane runs inside a pinned Ubuntu 24.04 job container. Nightly and weekly workflows:

1. check out immutable Hara and benchmark revisions;
2. install the declared runtime set;
3. prime pinned Clojure dependencies before any process-start measurement;
4. run the corpus and collect resource metadata;
5. validate normalized JSON against the schema;
6. upload raw evidence as a workflow artifact;
7. promote validated results to the `benchmarks-data` branch; and
8. trigger the Pages build from `main` plus that data history.

The data promotion step is idempotent and uses the run identifier in its path. Failed or invalid runs remain workflow artifacts but are not published.

## HTTP evidence for Hoplite

Hoplite needs two distinct HTTP tracks:

### Controlled Hara track

Keep the existing Hoplite versus OpenResty suite for rapid engineering feedback. Extend it with:

- plaintext and JSON responses
- route parameter extraction
- request-map and raw adapters
- one and multiple workers
- latency percentiles, requests/second, errors and peak/idle RSS
- image size and cold start

### Independent public track

Prepare Hoplite for **The Benchmarker Web Frameworks Benchmark**. It is Docker-based and defines three small compatibility routes (`GET /`, `GET /user/:id`, `POST /user`). The repository includes a submission scaffold under `suites/hoplite-openresty/external/the-benchmarker/`.

TechEmpower remains valuable as a historical methodology reference, but its repository was archived in March 2026 and should not be presented as an active submission destination.

External results should be linked and labelled as independently maintained. They should not be merged into the same aggregate as the controlled GitHub runner because hardware, tuning and test definitions differ.
