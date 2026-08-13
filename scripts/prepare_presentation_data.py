#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

HARA_RUNTIME = "hara-rust-whole-wasm-prepared"
LEGACY_HARA_RUNTIME = "hara-rust-full"
MIN_SHARED_WORKLOADS = 6


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def timestamp(run: dict[str, Any]) -> str:
    return str(run.get("environment", {}).get("timestamp") or "")


def samples(row: dict[str, Any]) -> list[float]:
    values = row.get("steady_state", {}).get("samples_ns") or []
    return [
        float(value)
        for value in values
        if isinstance(value, (int, float)) and value > 0
    ]


def usable_count(run: dict[str, Any], runtime: str) -> int:
    return len({
        row.get("workload")
        for row in run.get("measurements", [])
        if row.get("runtime") == runtime
        and row.get("status") == "ok"
        and samples(row)
        and row.get("workload")
    })


def resolve_runtime(
    run: dict[str, Any],
    base: str,
    runtime_specs: dict[str, Any],
) -> str | None:
    available = {
        str(row.get("runtime"))
        for row in run.get("measurements", [])
        if row.get("runtime")
    }
    if base == "hara" and HARA_RUNTIME in available:
        return HARA_RUNTIME
    prefix = str(runtime_specs.get(base, {}).get("runtime_prefix") or f"{base}-")
    matches = sorted(
        runtime
        for runtime in available
        if runtime.startswith(prefix) and runtime.endswith("-prepared")
    )
    return matches[0] if matches else None


def resolve_measured_runtimes(
    run: dict[str, Any],
    runtime_specs: dict[str, Any],
    display_order: list[str],
    minimum: int,
) -> dict[str, str] | None:
    resolved: dict[str, str] = {}
    for base in ["hara", *display_order]:
        specification = runtime_specs.get(base, {})
        if base != "hara" and specification.get("status") != "measured":
            continue
        runtime = resolve_runtime(run, base, runtime_specs)
        if runtime is None or usable_count(run, runtime) < minimum:
            return None
        resolved[base] = runtime
    return resolved


def normalize_measurements(
    run: dict[str, Any],
    selected_runtimes: set[str],
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in run.get("measurements", []):
        runtime = row.get("runtime")
        workload = row.get("workload")
        if runtime not in selected_runtimes or not workload:
            continue
        item: dict[str, Any] = {
            "runtime": runtime,
            "workload": workload,
            "status": row.get("status", "failed"),
        }
        values = samples(row)
        if row.get("status") == "ok" and values:
            item["analysis"] = {"steady_ns": round(statistics.median(values))}
        normalized.append(item)
    return normalized


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def prepare(
    catalog_path: Path,
    runs_path: Path,
    language_path: Path,
    class_path: Path,
    minimum: int = MIN_SHARED_WORKLOADS,
) -> dict[str, Any]:
    catalog = read_json(catalog_path)
    runs = read_json(runs_path).get("runs", [])
    runtime_catalog = catalog.get("runtime_catalog", {})
    runtime_specs = runtime_catalog.get("runtimes", {})
    display_order = runtime_catalog.get("display_order", [])

    selected: tuple[dict[str, Any], dict[str, str]] | None = None
    for run in sorted(runs, key=timestamp, reverse=True):
        resolved = resolve_measured_runtimes(
            run,
            runtime_specs,
            display_order,
            minimum,
        )
        if resolved is not None:
            selected = (run, resolved)
            break

    if selected is None:
        raise SystemExit(
            f"no canonical run contains at least {minimum} verified workloads "
            "for every measured prepared runtime"
        )

    run, resolved = selected
    normalized = normalize_measurements(run, set(resolved.values()))
    peer_order = [
        resolved[base]
        for base in display_order
        if base in resolved and base != "hara"
    ]
    workload_ids = list(dict.fromkeys(
        row["workload"] for row in normalized if row.get("workload")
    ))
    environment = dict(run.get("environment", {}))
    environment["benchmark_data_source"] = (
        "hara-lang/hara-benchmarks:published-evidence"
    )
    common = {
        "schema_version": 2,
        "profile": run.get("run", {}).get("profile", "canonical"),
        "environment": environment,
        "versions": run.get("versions", {}),
        "workload_ids": workload_ids,
        "provenance": run.get("provenance", {}),
    }

    language_rows = []
    for row in normalized:
        item = dict(row)
        if item["runtime"] == HARA_RUNTIME:
            item["runtime"] = LEGACY_HARA_RUNTIME
        language_rows.append(item)

    language_payload = {
        **common,
        "runtime_order": [*peer_order, LEGACY_HARA_RUNTIME],
        "measurements": language_rows,
    }
    class_payload = {
        **common,
        "runtime_order": [HARA_RUNTIME, *peer_order],
        "measurements": normalized,
    }
    write_json(language_path, language_payload)
    write_json(class_path, class_payload)
    return {
        "run_id": run.get("run", {}).get("id", "canonical run"),
        "runtime_count": len(resolved),
        "workload_count": len(workload_ids),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the benchmark dashboard presentation inputs from "
            "published evidence."
        )
    )
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--language", type=Path, required=True)
    parser.add_argument("--classes", dest="classes", type=Path, required=True)
    parser.add_argument(
        "--minimum-workloads",
        type=int,
        default=MIN_SHARED_WORKLOADS,
    )
    arguments = parser.parse_args()
    if arguments.minimum_workloads < 1:
        parser.error("--minimum-workloads must be positive")
    result = prepare(
        arguments.catalog,
        arguments.runs,
        arguments.language,
        arguments.classes,
        arguments.minimum_workloads,
    )
    print(
        f"prepared presentation evidence from {result['run_id']}: "
        f"{result['runtime_count']} measured runtimes, "
        f"{result['workload_count']} workloads"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
