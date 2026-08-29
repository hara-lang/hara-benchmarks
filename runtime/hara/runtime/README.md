# Cross-runtime benchmark

`workloads.json` is the canonical corpus. Every adapter receives the exact same
`source` string and validates its displayed result before reporting timing.

```shell
packaging/scripts/run-runtime-benchmarks --profile smoke
packaging/scripts/run-runtime-benchmarks --profile standard --reference
packaging/scripts/run-runtime-benchmarks --profile standard --check-regressions \
  --runtime bb \
  --runtime hara-rust-vm \
  --runtime hara-rust-full \
  --runtime hara-rust-trace-checked \
  --runtime hara-rust-trace-native
```

The runner records process startup, first evaluation, warm-up samples,
convergence, steady-state throughput, peak resident memory when available, and
runtime payload size. Workloads with an `iterations` field also report normalized
nanoseconds per iteration.

The Rust execution tiers are built into separate target directories. This
prevents a later Cargo feature build from silently changing the binary measured
by an earlier adapter:

- `hara-rust-vm` — plain bytecode VM;
- `hara-rust-full` — whole-function Wasm compiled through Wasmtime;
- `hara-rust-trace-checked` — guarded checked Trace IR;
- `hara-rust-trace-native` — guarded Wasmtime/Cranelift trace backend.

These four engine tiers compile once and time `execute-only`. Namespace,
macro, and protocol registry installation is intentionally outside their warm
samples: it is integration/setup work, not opcode execution. The benchmark
driver retains `runtime-registry-execute` as a separate diagnostic mode for
embedders; its cost must not be compared with the VM/JIT ratios below.

Absolute performance values are machine-specific evidence. The optional rules
in `regression-baselines.json` compare runtimes measured in the same invocation,
using ratios rather than historical wall-clock values. They are intended for
the standard profile; smoke results are diagnostic only.

## Integer representation evidence

`integer-representation-workloads.json` is the paired corpus for Hara issue
[#1145](https://github.com/hara-lang/hara/issues/1145). Each workload expands
into a `split` and a `unified` row. Kernel rows use identical Hara source so
the compact-i64/promoting-BigInt implementation is held constant; surface rows
use the current `long?` and a documented `number?` proxy for the undecided
future `integer?` surface. The proxy is deliberately not a language-contract
change.

The runner carries `pair_id`, `candidate`, `lane`, value class, source bytes,
artifact bytes when an adapter reports them, and any supported allocation
metric into the raw result. It also emits `candidate_comparisons` with the
unified/split ratio. These ratios are evidence only: no performance threshold
or API recommendation is applied automatically. Use the normal profiles with
the corpus path explicitly:

```shell
scripts/hara-runtime/run-runtime-benchmarks \
  --profile smoke \
  --corpus runtime/hara/runtime/integer-representation-workloads.json \
  --runtime hara-jvm-vm \
  --runtime hara-jvm-full \
  --runtime hara-rust-vm \
  --runtime hara-rust-full
```

The browser adapter consumes the same expanded rows through Hara’s dedicated
Playwright spec. Machine-specific JSON and Markdown reports belong in workflow
artifacts, not in this repository’s durable source tree.
