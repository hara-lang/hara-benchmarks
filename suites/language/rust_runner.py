#!/usr/bin/env python3
"""Compile and measure one checksum-verified Rust workload."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from pathlib import Path


TEMPLATE = r'''
use std::env;
use std::hint::black_box;
use std::time::Instant;

static mut BENCHMARK_SEED: i64 = 0;

#[inline(never)]
fn benchmark_seed() -> i64 {
    unsafe { std::ptr::read_volatile(std::ptr::addr_of!(BENCHMARK_SEED)) }
}

__SOURCE__

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 7 {
        eprintln!("compiled Rust benchmark expects ID EXPECTED WINDOWS CALLS PREPARE_NS ARTIFACT_BYTES");
        std::process::exit(2);
    }

    let id = &args[1];
    let expected: i64 = args[2].parse().expect("invalid expected checksum");
    let windows: usize = args[3].parse().expect("invalid window count");
    let calls: usize = args[4].parse().expect("invalid call count");
    let prepare_ns: u128 = args[5].parse().expect("invalid preparation time");
    let artifact_bytes: u64 = args[6].parse().expect("invalid artifact size");

    // The seed must be runtime-opaque. An immutable zero-valued static allowed
    // LLVM to constant-fold recursive and numeric workloads while still
    // preserving the volatile read. Writing an opaque value through a mutable
    // static keeps the workload input dynamic without changing its checksum.
    let seed = black_box(0_i64);
    unsafe {
        std::ptr::write_volatile(std::ptr::addr_of_mut!(BENCHMARK_SEED), seed);
    }

    let started = Instant::now();
    let mut value = black_box(benchmark());
    let first_ns = started.elapsed().as_nanos();
    if value != expected {
        eprintln!("{id}: expected {expected}, got {value}");
        std::process::exit(1);
    }

    print!(
        "{{\"runtime\":\"rust\",\"workload\":\"{}\",\"prepare_ns\":{},\"first_ns\":{},\"artifact_bytes\":{},\"samples_ns\":[",
        id, prepare_ns, first_ns, artifact_bytes
    );
    for window in 0..windows {
        let started = Instant::now();
        for _ in 0..calls {
            value = black_box(benchmark());
        }
        let sample_ns = started.elapsed().as_nanos() / calls.max(1) as u128;
        if value != expected {
            eprintln!("{id}: expected {expected}, got {value}");
            std::process::exit(1);
        }
        if window > 0 {
            print!(",");
        }
        print!("{}", sample_ns);
    }
    println!("]}}");
}
'''


def main() -> int:
    if len(sys.argv) != 7:
        raise SystemExit("rust_runner expects MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS")
    mode, workload, source_hex, expected, windows, calls = sys.argv[1:]
    if mode != "prepared":
        raise SystemExit("Rust is a prepared-only native reference lane")

    source = bytes.fromhex(source_hex).decode("utf-8")
    with tempfile.TemporaryDirectory(prefix="hara-rust-bench-") as directory:
        root = Path(directory)
        source_path = root / "benchmark.rs"
        binary = root / "benchmark"
        prepare_started = time.perf_counter_ns()
        source_path.write_text(TEMPLATE.replace("__SOURCE__", source), encoding="utf-8")
        subprocess.run(
            [
                "rustc",
                "--edition=2021",
                "-C",
                "opt-level=3",
                "-C",
                "codegen-units=1",
                str(source_path),
                "-o",
                str(binary),
            ],
            check=True,
        )
        prepare_ns = time.perf_counter_ns() - prepare_started
        completed = subprocess.run(
            [
                str(binary),
                workload,
                expected,
                windows,
                calls,
                str(prepare_ns),
                str(binary.stat().st_size),
            ],
            check=False,
        )
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
