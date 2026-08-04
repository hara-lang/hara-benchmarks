from __future__ import annotations

from pathlib import Path
from typing import Any

from .model import SCHEMA_VERSION, environment, read_json


RESOURCE_FIELDS = (
    "peak_rss_bytes", "idle_rss_bytes", "source_bytes", "artifact_bytes",
    "compressed_artifact_bytes", "runtime_executable_bytes",
    "runtime_bundle_bytes", "container_image_bytes",
)


def import_language(path: Path) -> dict[str, Any]:
    source = read_json(path)
    measurements = []
    for row in source.get("measurements", []):
        samples = row.get("samples_ns", [])
        status = row.get("status", "ok" if samples else "unsupported")
        normalized = {
            "suite": "algorithms",
            "workload": row.get("workload", "unknown"),
            "runtime": row.get("runtime", "unknown"),
            "mode": "eval" if row.get("runtime", "").endswith("-eval") else "prepared",
            "status": status,
            "reason": row.get("reason"),
            "cold_total_ns": source.get("startup", {}).get(row.get("runtime"), {}).get("p50_ns"),
            "prepare_ns": row.get("prepare_ns"),
            "first_call_ns": row.get("first_ns"),
            "warmup_samples_ns": row.get("samples_ns", [])[:5],
            "steady_state": {"samples_ns": samples},
            "converged_window": row.get("analysis", {}).get("converged_window"),
        }
        normalized.update({field: row.get(field) for field in RESOURCE_FIELDS})
        measurements.append(normalized)
    return {
        "schema_version": SCHEMA_VERSION,
        "run": {
            "id": source.get("environment", {}).get("timestamp", "imported").replace(":", "-"),
            "profile": source.get("profile", "imported"),
            "source": "imported-language-runner",
        },
        "environment": source.get("environment", environment()),
        "versions": source.get("versions", {}),
        "provenance": {
            "benchmark_revision": source.get("environment", {}).get("benchmark_revision"),
            "hara_revision": source.get("environment", {}).get("git_revision"),
            "hara_dirty": source.get("environment", {}).get("git_dirty"),
        },
        "measurements": measurements,
    }
