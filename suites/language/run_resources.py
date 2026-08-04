#!/usr/bin/env python3
"""Run the language corpus with process resource measurements.

This is a thin wrapper around ``run.py`` so the benchmark coordinator remains
usable on developer machines while CI can add RSS, executable-size and source-
size evidence. It also enables PyPy by reusing the exact Python implementation.
"""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
COORDINATOR = HERE / "run.py"


def load_coordinator():
    spec = importlib.util.spec_from_file_location("hara_language_coordinator", COORDINATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {COORDINATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_peak_rss(stderr: str) -> int | None:
    """Return peak RSS in bytes from GNU or BSD ``time`` output."""
    for line in stderr.splitlines():
        if "Maximum resident set size (kbytes):" in line:
            return int(line.rsplit(":", 1)[1].strip()) * 1024
    lines = [line.strip() for line in stderr.splitlines()]
    for index, line in enumerate(lines):
        if line.endswith("maximum resident set size"):
            try:
                return int(line.split()[0])
            except (ValueError, IndexError):
                return None
        if line == "maximum resident set size" and index:
            try:
                return int(lines[index - 1].split()[0])
            except (ValueError, IndexError):
                return None
    return None


def executable_bytes(command: list[str]) -> int | None:
    binary = command[0]
    resolved = Path(binary) if os.path.sep in binary else Path(shutil.which(binary) or "")
    try:
        return resolved.stat().st_size if resolved.is_file() else None
    except OSError:
        return None


def source_bytes(command: list[str]) -> int | None:
    # Every adapter ends in MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS.
    if len(command) < 6:
        return None
    try:
        return len(bytes.fromhex(command[-4]))
    except (ValueError, TypeError):
        return None


def output_path(argv: list[str], default: Path) -> Path:
    try:
        index = argv.index("--output")
        return Path(argv[index + 1]).resolve()
    except (ValueError, IndexError):
        return default.resolve()


def main() -> int:
    coordinator = load_coordinator()
    coordinator.LANGUAGE_RUNTIMES["pypy"] = {
        "command": ["pypy3", str(coordinator.PYTHON_RUNNER)],
        "source_field": "python_source",
        "binary": "pypy3",
    }

    def timed_with_resources(command: list[str]):
        timer = "/usr/bin/time"
        if not Path(timer).exists():
            raise RuntimeError("/usr/bin/time is required for resource measurements")
        flag = "-v" if platform.system() == "Linux" else "-l"
        started = time.perf_counter_ns()
        result = subprocess.run(
            [timer, flag, *command],
            cwd=coordinator.ROOT,
            text=True,
            capture_output=True,
            timeout=1200,
            check=False,
        )
        elapsed = time.perf_counter_ns() - started
        if result.returncode:
            raise subprocess.CalledProcessError(
                result.returncode, command, output=result.stdout, stderr=result.stderr
            )
        line = next(
            (line for line in reversed(result.stdout.splitlines()) if line.startswith("{")),
            None,
        )
        if line is None:
            raise RuntimeError(f"adapter emitted no JSON: {' '.join(command)}")
        payload: dict[str, Any] = json.loads(line)
        payload["peak_rss_bytes"] = parse_peak_rss(result.stderr)
        payload["runtime_executable_bytes"] = executable_bytes(command)
        payload["source_bytes"] = source_bytes(command)
        return elapsed, payload

    coordinator.timed = timed_with_resources
    result = coordinator.main()

    path = output_path(sys.argv, coordinator.ROOT / "target/lisp-hara-benchmark.json")
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("versions", {})["pypy"] = coordinator.version(["pypy3", "--version"])
        data.setdefault("environment", {}).update({
            "container_image": os.environ.get("HARA_BENCH_CONTAINER_IMAGE"),
            "runner": os.environ.get("RUNNER_NAME"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        })
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
