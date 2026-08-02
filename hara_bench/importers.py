from __future__ import annotations

from pathlib import Path
from typing import Any

from .model import SCHEMA_VERSION, environment, read_json


def import_language(path: Path) -> dict[str, Any]:
    source = read_json(path)
    measurements = []
    for row in source.get("measurements", []):
        samples = row.get("samples_ns", [])
        status = row.get("status", "ok" if samples else "unsupported")
        measurements.append({
            "suite": "algorithms",
            "workload": row.get("workload", "unknown"),
            "runtime": row.get("runtime", "unknown"),
            "status": status,
            "reason": row.get("reason"),
            "cold_start_ns": source.get("startup", {}).get(row.get("runtime"), {}).get("p50_ns"),
            "first_call_ns": row.get("first_ns"),
            "warmup_samples_ns": row.get("samples_ns", [])[:5],
            "steady_state": {"samples_ns": samples},
            "peak_rss_bytes": row.get("peak_rss_bytes"),
            "artifact_bytes": row.get("artifact_bytes"),
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "run": {
            "id": source.get("environment", {}).get("timestamp", "imported").replace(":", "-"),
            "profile": source.get("profile", "imported"),
            "source": "imported-language-runner",
        },
        "environment": source.get("environment", environment()),
        "versions": source.get("versions", {}),
        "measurements": measurements,
    }

