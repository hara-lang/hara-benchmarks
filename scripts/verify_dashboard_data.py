#!/usr/bin/env python3
"""Fail a Pages build unless it contains real, comparable benchmark evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_PREPARED_RUNTIMES = (
    "hara-rust-whole-wasm-prepared",
    "luajit-prepared",
    "pypy-prepared",
    "node-prepared",
    "ruby-yjit-prepared",
    "clojure-prepared",
    "sbcl-prepared",
    "chez-prepared",
    "guile-prepared",
    "bb-prepared",
    "python-prepared",
    "c-prepared",
    "java-prepared",
)
MIN_SHARED_WORKLOADS = 6
SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


def latest_run(payload: dict[str, Any]) -> dict[str, Any]:
    runs = payload.get("runs") or []
    if not runs:
        raise ValueError("dashboard contains no benchmark runs")
    return max(
        runs,
        key=lambda run: str(run.get("environment", {}).get("timestamp", "")),
    )


def usable_workloads(run: dict[str, Any], runtime: str) -> set[str]:
    return {
        str(row["workload"])
        for row in run.get("measurements", [])
        if row.get("runtime") == runtime
        and row.get("status") == "ok"
        and row.get("steady_state", {}).get("samples_ns")
        and row.get("workload")
    }


def verify(payload: dict[str, Any]) -> dict[str, Any]:
    run = latest_run(payload)
    environment = run.get("environment", {})
    revision = str(environment.get("benchmark_revision") or "")
    if not SHA_PATTERN.fullmatch(revision):
        raise ValueError(
            "latest run has no immutable benchmark revision: "
            f"{revision or 'missing'}"
        )

    hara_runtime = REQUIRED_PREPARED_RUNTIMES[0]
    hara_workloads = usable_workloads(run, hara_runtime)
    if len(hara_workloads) < MIN_SHARED_WORKLOADS:
        raise ValueError(
            f"{hara_runtime} has only {len(hara_workloads)} usable workloads"
        )

    shared_counts: dict[str, int] = {}
    for runtime in REQUIRED_PREPARED_RUNTIMES[1:]:
        workloads = usable_workloads(run, runtime)
        if not workloads:
            raise ValueError(f"latest run has no usable measurements for {runtime}")
        shared = hara_workloads & workloads
        shared_counts[runtime] = len(shared)
        if len(shared) < MIN_SHARED_WORKLOADS:
            raise ValueError(
                f"{runtime} shares only {len(shared)} workloads with {hara_runtime}"
            )

    return {
        "run_id": run.get("run", {}).get("id"),
        "timestamp": environment.get("timestamp"),
        "benchmark_revision": revision,
        "hara_workloads": len(hara_workloads),
        "minimum_shared_workloads": min(shared_counts.values()),
        "runtime_count": len(REQUIRED_PREPARED_RUNTIMES),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs_json", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.runs_json.read_text(encoding="utf-8"))
    summary = verify(payload)
    print(
        "verified dashboard comparison run "
        f"{summary['run_id']} at {summary['timestamp']}: "
        f"{summary['runtime_count']} prepared runtimes, "
        f"{summary['hara_workloads']} Hara workloads, "
        f"minimum {summary['minimum_shared_workloads']} shared workloads"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
