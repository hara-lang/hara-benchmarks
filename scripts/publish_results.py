#!/usr/bin/env python3
"""Promote validated workflow results into a durable benchmark history."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from hara_bench.model import read_json, validate_run, write_json


def safe(value: object) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "unknown")).strip("-")
    return text or "unknown"


def publish(inputs: Path, output: Path) -> list[Path]:
    written: list[Path] = []
    for source_path in sorted(inputs.rglob("normalized.json")):
        data = read_json(source_path)
        errors = validate_run(data)
        if errors:
            raise ValueError(f"{source_path}: " + "; ".join(errors))
        run = data.setdefault("run", {})
        env = data.setdefault("environment", {})
        provenance = data.setdefault("provenance", {})
        provenance.update({
            "github_repository": os.environ.get("GITHUB_REPOSITORY"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "workflow_sha": os.environ.get("GITHUB_SHA"),
        })
        target = output / "runs" / safe(env.get("os", env.get("platform"))) / safe(env.get("architecture", env.get("machine"))) / safe(run.get("profile")) / f"{safe(run.get('id'))}.json"
        write_json(target, data)
        written.append(target)
    manifest = {
        "schema_version": 1,
        "runs": [str(path.relative_to(output)) for path in sorted(written)],
    }
    write_json(output / "manifest.json", manifest)
    return written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    written = publish(args.inputs, args.output)
    print(f"published {len(written)} run(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
