from __future__ import annotations

import datetime as dt
import json
import math
import platform
import statistics
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 2


def percentile(values: list[int | float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, math.ceil(fraction * len(ordered)) - 1)
    return float(ordered[max(0, index)])


def summarize(values: list[int | float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "p50": None, "p95": None, "mean": None, "cv": None}
    mean = statistics.fmean(values)
    return {
        "count": len(values),
        "p50": float(statistics.median(values)),
        "p95": percentile(values, 0.95),
        "mean": mean,
        "cv": statistics.pstdev(values) / mean if len(values) > 1 and mean else 0.0,
    }


def environment() -> dict[str, Any]:
    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "os": platform.system().lower(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
    }


def validate_run(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "run", "environment", "measurements"):
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    if data.get("schema_version") not in (1, SCHEMA_VERSION):
        errors.append(f"schema_version must be 1 or {SCHEMA_VERSION}")
    measurements = data.get("measurements", [])
    if not isinstance(measurements, list):
        errors.append("measurements must be an array")
        return errors
    required = ("suite", "workload", "runtime", "status")
    for index, row in enumerate(measurements):
        for key in required:
            if key not in row:
                errors.append(f"measurements[{index}] missing {key}")
        if row.get("status") == "ok":
            steady = row.get("steady_state", {})
            if not isinstance(steady.get("samples_ns"), list) or not steady["samples_ns"]:
                errors.append(f"measurements[{index}] has no steady-state samples")
    return errors


def median_ns(row: dict[str, Any]) -> float | None:
    if row.get("status") != "ok":
        return None
    return summarize(row.get("steady_state", {}).get("samples_ns", []))["p50"]


def geometric_mean(values: list[float]) -> float | None:
    positive = [value for value in values if value > 0]
    if not positive or len(positive) != len(values):
        return None
    return math.exp(sum(math.log(value) for value in positive) / len(positive))


def rank_runtimes(measurements: list[dict[str, Any]], workloads: set[str] | None = None) -> list[dict[str, Any]]:
    """Rank prepared runtimes on their common successful workload set."""
    prepared = [row for row in measurements if row.get("mode", "prepared") == "prepared"]
    runtimes = sorted({row["runtime"] for row in prepared})
    available = workloads or {row["workload"] for row in prepared}
    index = {(row["runtime"], row["workload"]): row for row in prepared}
    common = sorted(workload for workload in available if all(
        median_ns(index.get((runtime, workload), {})) is not None for runtime in runtimes))
    fastest = {workload: min(median_ns(index[(runtime, workload)]) for runtime in runtimes)
               for workload in common}
    ranked = []
    for runtime in runtimes:
        ratios = [median_ns(index[(runtime, workload)]) / fastest[workload] for workload in common]
        supported = sum(median_ns(index.get((runtime, workload), {})) is not None for workload in available)
        wins = sum(abs(ratio - 1.0) < 1e-12 for ratio in ratios)
        ranked.append({"runtime": runtime, "score": geometric_mean(ratios), "wins": wins,
                       "supported": supported, "total": len(available), "common": common})
    ranked.sort(key=lambda row: (row["score"] is None, row["score"] or math.inf, -row["supported"]))
    for position, row in enumerate(ranked, 1):
        row["rank"] = position
    return ranked


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
