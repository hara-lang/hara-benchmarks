from __future__ import annotations

import datetime as dt
import json
import math
import platform
import statistics
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


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
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
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


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

