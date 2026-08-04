from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from .importers import import_language
from .model import read_json, validate_run, write_json
from .site import build, discover_runs


ROOT = Path(__file__).resolve().parents[1]


def command_validate(args: argparse.Namespace) -> int:
    paths = [Path(args.path)] if Path(args.path).is_file() else discover_runs(Path(args.path))
    failures = 0
    for path in paths:
        errors = validate_run(read_json(path))
        if errors:
            failures += 1
            print(f"{path}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
    print(f"validated {len(paths)} run(s); {failures} invalid")
    return 1 if failures else 0


def command_import(args: argparse.Namespace) -> int:
    result = import_language(Path(args.input))
    errors = validate_run(result)
    if errors:
        raise SystemExit("invalid imported run: " + "; ".join(errors))
    write_json(Path(args.output), result)
    print(args.output)
    return 0


def command_site(args: argparse.Namespace) -> int:
    count = build(Path(args.data), Path(args.output))
    print(f"built {args.output} from {count} run(s)")
    return 0


def command_run(args: argparse.Namespace) -> int:
    hara_root = Path(args.hara_root or os.environ.get("HARA_ROOT", ROOT / "vendor/hara")).resolve()
    if not (hara_root / "rust/Cargo.toml").exists():
        print(f"Hara checkout not found at {hara_root}; pass --hara-root or set HARA_ROOT", file=sys.stderr)
        return 2
    if args.suite == "algorithms":
        coordinator = ROOT / "suites/language/run_resources.py"
        profile = {"nightly": "algorithm", "weekly": "standard"}.get(args.profile, args.profile)
        output = ROOT / "results/local/language.json"
        cmd = [sys.executable, str(coordinator), "--profile", profile,
               "--corpus", str(ROOT / "suites/language/general-workloads.json"),
               "--output", str(output)]
        for runtime in args.runtime or []:
            cmd.extend(("--runtime", runtime))
    elif args.suite == "runtime":
        coordinator = ROOT / "suites/runtime/run.py"
        cmd = [sys.executable, str(coordinator), "--profile", "smoke" if args.profile == "smoke" else "standard"]
    elif args.suite == "boundary":
        coordinator = ROOT / "suites/boundary/run.mjs"
        cmd = ["node", str(coordinator)] + (["--standard"] if args.profile != "smoke" else [])
    elif args.suite == "hoplite":
        coordinator = ROOT / "suites/hoplite-openresty/run.sh"
        cmd = ["bash", str(coordinator)]
    else:
        print(f"unknown suite: {args.suite}", file=sys.stderr)
        return 2
    env = {**os.environ, "HARA_ROOT": str(hara_root), "HARA_BENCH_ROOT": str(ROOT)}
    return subprocess.call(cmd, cwd=hara_root, env=env)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="hara-bench")
    sub = result.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="run a benchmark suite")
    run.add_argument("--suite", choices=("algorithms", "runtime", "boundary", "hoplite"), required=True)
    run.add_argument("--profile", choices=("smoke", "algorithm", "standard", "nightly", "weekly"), default="smoke")
    run.add_argument("--hara-root")
    run.add_argument("--runtime", action="append", help="limit to a runtime adapter (repeatable)")
    run.set_defaults(func=command_run)
    validate = sub.add_parser("validate", help="validate normalized run JSON")
    validate.add_argument("path", nargs="?", default="data")
    validate.set_defaults(func=command_validate)
    imported = sub.add_parser("import-language", help="normalize a legacy language-runner result")
    imported.add_argument("input")
    imported.add_argument("output")
    imported.set_defaults(func=command_import)
    site = sub.add_parser("build-site", help="build the static results dashboard")
    site.add_argument("--data", default="data")
    site.add_argument("--output", default="dist")
    site.set_defaults(func=command_site)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return args.func(args)
