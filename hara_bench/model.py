from __future__ import annotations

import datetime as dt
import json
import math
import platform
import statistics
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 3


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
    if data.get("schema_version") not in (1, 2, SCHEMA_VERSION):
        errors.append(f"schema_version must be 1, 2 or {SCHEMA_VERSION}")
    measurements = data.get("measurements", [])
    if not isinstance(measurements, list):
        errors.append("measurements must be an array")
        return errors
    required = ("suite", "workload", "runtime", "status")
    byte_fields = (
        "peak_rss_bytes", "idle_rss_bytes", "source_bytes", "artifact_bytes",
        "compressed_artifact_bytes", "runtime_executable_bytes",
        "runtime_bundle_bytes", "container_image_bytes",
    )
    for index, row in enumerate(measurements):
        for key in required:
            if key not in row:
                errors.append(f"measurements[{index}] missing {key}")
        if row.get("status") == "ok":
            steady = row.get("steady_state", {})
            if not isinstance(steady.get("samples_ns"), list) or not steady["samples_ns"]:
                errors.append(f"measurements[{index}] has no steady-state samples")
        for key in byte_fields:
            value = row.get(key)
            if value is not None and (not isinstance(value, (int, float)) or value < 0):
                errors.append(f"measurements[{index}] {key} must be a non-negative number or null")
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


def compare_hara(
    measurements: list[dict[str, Any]],
    comparator: str,
    workloads: set[str] | None = None,
    hara_runtime: str | None = None,
) -> dict[str, Any]:
    """Compare Hara with one reference runtime over their common workloads."""
    prepared = [row for row in measurements if row.get("mode", "prepared") == "prepared"]
    runtimes = {row["runtime"] for row in prepared}
    if hara_runtime is None:
        candidates = sorted(runtime for runtime in runtimes if runtime.startswith("hara-"))
        hara_runtime = next(
            (runtime for runtime in candidates if "whole-wasm" in runtime),
            candidates[0] if candidates else None,
        )
    if hara_runtime is None or hara_runtime not in runtimes:
        raise ValueError("no prepared Hara runtime is present")
    if comparator not in runtimes or comparator.startswith("hara-"):
        raise ValueError(f"invalid reference runtime: {comparator}")
    available = workloads or {row["workload"] for row in prepared}
    index = {(row["runtime"], row["workload"]): row for row in prepared}
    common = sorted(workload for workload in available if
                    median_ns(index.get((hara_runtime, workload), {})) is not None and
                    median_ns(index.get((comparator, workload), {})) is not None)
    ratios = [median_ns(index[(hara_runtime, workload)]) /
              median_ns(index[(comparator, workload)]) for workload in common]
    return {
        "hara_runtime": hara_runtime,
        "comparator": comparator,
        "ratio": geometric_mean(ratios),
        "common": common,
        "excluded": sorted(set(available) - set(common)),
        "hara_supported": sum(median_ns(index.get((hara_runtime, workload), {})) is not None
                              for workload in available),
        "comparator_supported": sum(median_ns(index.get((comparator, workload), {})) is not None
                                    for workload in available),
        "total": len(available),
    }


def describe_hara_ratio(ratio: float | None) -> str:
    if ratio is None:
        return "No common measurements"
    if abs(ratio - 1.0) <= 0.01:
        return "Hara and the reference are approximately equal"
    if ratio < 1:
        return f"Hara is {1 / ratio:.2f}× faster"
    return f"Hara is {ratio:.2f}× slower"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
