#!/usr/bin/env python3
"""Require benchmark lanes to contain real successful workload measurements."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def verify(path: Path, runtimes: list[str], minimum: int) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    counts = Counter(
        str(row.get("runtime"))
        for row in payload.get("measurements", [])
        if row.get("status") == "ok" and row.get("samples_ns")
    )
    missing = {
        runtime: counts.get(runtime, 0)
        for runtime in runtimes
        if counts.get(runtime, 0) < minimum
    }
    if missing:
        details = ", ".join(f"{runtime}={count}" for runtime, count in missing.items())
        raise ValueError(
            f"benchmark lanes have fewer than {minimum} successful workloads: {details}"
        )
    return {runtime: counts[runtime] for runtime in runtimes}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--runtime", action="append", required=True)
    parser.add_argument("--minimum", type=int, default=6)
    args = parser.parse_args()
    counts = verify(args.results, args.runtime, args.minimum)
    print("verified runtime coverage: " + ", ".join(
        f"{runtime}={count}" for runtime, count in counts.items()
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
