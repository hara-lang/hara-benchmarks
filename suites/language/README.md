# Language corpus

The language corpus answers three separate questions rather than producing one undifferentiated league table.

## In-class dynamic JIT

Measured now:

- Hara whole-Wasm
- LuaJIT
- PyPy, using the identical Python source used by CPython

Planned adapters:

- Node.js / V8
- Ruby / YJIT
- Clojure / HotSpot

## Lisp family

Measured now:

- Hara
- SBCL
- Chez Scheme
- GNU Guile
- Babashka

Clojure / HotSpot and Racket CS are the next additions.

## References and baselines

- C is the ahead-of-time native reference.
- Java / HotSpot is the managed JIT reference.
- CPython is the familiar dynamic interpreter baseline.

C and Java remain visible, but are categorised and coloured separately from Hara's in-class dynamic-JIT comparison.

## Modes

- `prepared` measures already parsed/compiled work and is the primary steady-state comparison.
- `eval` includes source evaluation and remains a lifecycle result.
- C and Java are prepared-only because their compiler step is recorded separately.

## Resource collection

`run_resources.py` wraps the existing coordinator with `/usr/bin/time`, records peak RSS, runtime executable size and source size, and adds the PyPy adapter. The normalized schema keeps source, runtime, bundle, generated artifact and image sizes separate.
