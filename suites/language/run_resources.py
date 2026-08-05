#!/usr/bin/env python3
"""Run the language corpus with process resource measurements.

This is a thin wrapper around ``run.py`` so the benchmark coordinator remains
usable on developer machines while CI can add RSS, executable-size and source-
size evidence. It enables PyPy, Node.js/V8, Ruby/YJIT and Clojure/HotSpot while
keeping runtime-specific sources explicit and inspectable.
"""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
COORDINATOR = HERE / "run.py"
CLOJURE_VERSION = "1.12.5"
CLOJURE_DEPS = (
    '{:mvn/repos {"central" {:url "https://repo.maven.apache.org/maven2/"}} '
    ':deps {org.clojure/clojure {:mvn/version "' + CLOJURE_VERSION + '"}}}'
)


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


@lru_cache(maxsize=1)
def clojure_bundle_bytes() -> int | None:
    """Measure the pinned Clojure dependency classpath, excluding directories."""
    try:
        result = subprocess.run(
            ["clojure", "-Sdeps", CLOJURE_DEPS, "-Spath"],
            text=True,
            capture_output=True,
            timeout=120,
            check=True,
            cwd=HERE,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    total = 0
    found = False
    for item in result.stdout.strip().split(os.pathsep):
        path = Path(item)
        try:
            if path.is_file():
                total += path.stat().st_size
                found = True
        except OSError:
            continue
    return total if found else None


def runtime_bundle_bytes(command: list[str]) -> int | None:
    return clojure_bundle_bytes() if command and command[0] == "clojure" else None


def output_path(argv: list[str], default: Path) -> Path:
    try:
        index = argv.index("--output")
        return Path(argv[index + 1]).resolve()
    except (ValueError, IndexError):
        return default.resolve()


def command_version(command: list[str], *, cwd: Path | None = None) -> str:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def node_version() -> str:
    return command_version([
        "node",
        "-p",
        "`Node ${process.version} / V8 ${process.versions.v8}`",
    ])


def ruby_version() -> str:
    return command_version([
        "ruby",
        "--yjit",
        "-e",
        'print "#{RUBY_DESCRIPTION} / YJIT #{RubyVM::YJIT.enabled? ? "enabled" : "disabled"}"',
    ])


def main() -> int:
    coordinator = load_coordinator()
    configured_chez = os.environ.get("HARA_BENCH_CHEZ_EXECUTABLE")
    if configured_chez:
        coordinator.LANGUAGE_RUNTIMES["chez"]["command"][0] = configured_chez
        coordinator.LANGUAGE_RUNTIMES["chez"]["binary"] = configured_chez
    coordinator.LANGUAGE_RUNTIMES["pypy"] = {
        "command": ["pypy3", str(coordinator.PYTHON_RUNNER)],
        "source_field": "python_source",
        "binary": "pypy3",
    }
    coordinator.LANGUAGE_RUNTIMES["clojure"] = {
        "command": [
            "clojure",
            "-Sdeps",
            CLOJURE_DEPS,
            "-M",
            str(HERE / "clojure_runner.clj"),
        ],
        "source_field": "bb_source",
        "binary": "clojure",
    }

    external_specs = {
        "node": {
            "command": ["node", str(HERE / "node_runner.mjs")],
            "sources": json.loads(
                (HERE / "node_workloads.json").read_text(encoding="utf-8")
            )["workloads"],
        },
        "ruby-yjit": {
            "command": ["ruby", "--yjit", str(HERE / "ruby_runner.rb")],
            "sources": json.loads(
                (HERE / "ruby_workloads.json").read_text(encoding="utf-8")
            )["workloads"],
        },
    }
    base_adapters = coordinator.adapters

    def adapters_with_external_runtimes():
        result = base_adapters()

        def external_adapter(
            spec: dict[str, Any],
            mode: str,
            workload: dict[str, Any],
            windows: int,
            calls: int,
        ) -> list[str]:
            source = spec["sources"].get(workload["id"])
            if source is None:
                raise KeyError(f"external source missing for {workload['id']}")
            return [
                *spec["command"],
                mode,
                workload["id"],
                source.encode().hex(),
                workload["expected"],
                str(windows),
                str(calls),
            ]

        for runtime, spec in external_specs.items():
            for mode in ("eval", "prepared"):
                result[f"{runtime}-{mode}"] = (
                    lambda workload, windows, calls, spec=spec, mode=mode:
                    external_adapter(spec, mode, workload, windows, calls)
                )
        return result

    coordinator.adapters = adapters_with_external_runtimes

    def timed_with_resources(command: list[str]):
        timer = "/usr/bin/time"
        if not Path(timer).exists():
            raise RuntimeError("/usr/bin/time is required for resource measurements")
        linux = platform.system() == "Linux"
        started = time.perf_counter_ns()
        run_cwd = HERE if command and command[0] == "clojure" else coordinator.ROOT
        time_path: Path | None = None
        try:
            if linux:
                handle = tempfile.NamedTemporaryFile(
                    prefix="hara-bench-time-", suffix=".txt", delete=False
                )
                time_path = Path(handle.name)
                handle.close()
                timed_command = [timer, "-v", "-o", str(time_path), *command]
            else:
                timed_command = [timer, "-l", *command]
            result = subprocess.run(
                timed_command,
                cwd=run_cwd,
                text=True,
                capture_output=True,
                timeout=1200,
                check=False,
            )
            elapsed = time.perf_counter_ns() - started
            timing_output = (
                time_path.read_text(encoding="utf-8")
                if time_path is not None and time_path.exists()
                else result.stderr
            )
        finally:
            if time_path is not None:
                time_path.unlink(missing_ok=True)
        if result.returncode:
            # GNU time writes its measurements to a separate file, preserving the
            # adapter's real stderr so CI reports compilation and runtime errors.
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
        payload["peak_rss_bytes"] = parse_peak_rss(timing_output)
        payload["runtime_executable_bytes"] = executable_bytes(command)
        payload["runtime_bundle_bytes"] = runtime_bundle_bytes(command)
        payload["source_bytes"] = source_bytes(command)
        return elapsed, payload

    coordinator.timed = timed_with_resources
    result = coordinator.main()

    path = output_path(sys.argv, coordinator.ROOT / "target/lisp-hara-benchmark.json")
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        versions = data.setdefault("versions", {})
        versions["pypy"] = coordinator.version(["pypy3", "--version"])
        versions["node"] = node_version()
        versions["ruby"] = ruby_version()
        try:
            clojure_version = subprocess.run(
                [
                    "clojure",
                    "-Sdeps",
                    CLOJURE_DEPS,
                    "-M",
                    "-e",
                    "(println (clojure-version))",
                ],
                cwd=HERE,
                text=True,
                capture_output=True,
                timeout=120,
                check=True,
            ).stdout.strip().splitlines()[0]
        except (OSError, subprocess.SubprocessError, IndexError):
            clojure_version = "unavailable"
        versions["clojure"] = clojure_version
        environment = data.setdefault("environment", {})
        environment.update({
            "container_image": os.environ.get("HARA_BENCH_CONTAINER_IMAGE"),
            "runner": os.environ.get("RUNNER_NAME"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        })
        if os.environ.get("HARA_BENCHMARK_REVISION"):
            environment["benchmark_revision"] = os.environ["HARA_BENCHMARK_REVISION"]
        if os.environ.get("HARA_REVISION"):
            environment["git_revision"] = os.environ["HARA_REVISION"]
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
