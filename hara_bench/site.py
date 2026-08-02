from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .model import read_json, validate_run


ROOT = Path(__file__).resolve().parents[1]

LANGUAGES = {
    "hara": ("hara_source", "Hara", "suites/language/run.py"),
    "sbcl": ("cl_source", "Common Lisp", "suites/language/sbcl_runner.lisp"),
    "chez": ("scheme_source", "Scheme", "suites/language/chez_runner.scm"),
    "guile": ("scheme_source", "Scheme", "suites/language/guile_runner.scm"),
    "luajit": ("lua_source", "Lua", "adapters/luajit/lua_runner.lua"),
    "bb": ("bb_source", "Clojure", "suites/language/bb_runner.clj"),
    "python": ("python_source", "Python", "suites/language/python_runner.py"),
    "c": ("c_source", "C", "suites/language/c_runner.py"),
    "java": ("java_source", "Java", "suites/language/java_runner.py"),
}

CATEGORY = {
    "sieve-array": "Arrays & loops", "matrix-multiply": "Arrays & loops",
    "towers-recursive": "Recursion", "ackermann-deep": "Recursion", "tak-branching": "Recursion",
    "queens-backtracking": "Search & mutation", "heap-permute": "Search & mutation",
    "collatz-range": "Irregular control",
}


def source_catalog() -> dict[str, Any]:
    corpus = read_json(ROOT / "suites/language/general-workloads.json")
    workloads = []
    for workload in corpus["workloads"]:
        implementations = {}
        for runtime, (field, language, harness_path) in LANGUAGES.items():
            if field not in workload:
                continue
            harness = ROOT / harness_path
            implementations[runtime] = {
                "language": language, "source": workload[field],
                "harness": harness.read_text(encoding="utf-8"), "harness_path": harness_path,
                "prepare": preparation(runtime),
            }
        workloads.append({"id": workload["id"], "category": CATEGORY.get(workload["id"], workload.get("group")),
                          "group": workload.get("group"), "operations": workload.get("operations"),
                          "expected": workload["expected"], "implementations": implementations})
    return {"schema_version": 1, "methodology": corpus.get("methodology"), "workloads": workloads}


def preparation(runtime: str) -> dict[str, Any]:
    details = {
        "hara": ("Parse Hara → bytecode → whole-function Wasm → load module", "cargo build --release --features whole-wasm --bin hara-bytecode-benchmark"),
        "c": ("Generate translation unit and compile with cc -O3", "cc -O3 -std=c11 benchmark.c -o benchmark"),
        "java": ("Generate class and compile without debug metadata", "javac -g:none HaraAlgorithmBenchmark.java"),
        "python": ("compile(source, workload, 'exec'), then resolve benchmark", "python3 python_runner.py prepared …"),
        "sbcl": ("Read form and compile a zero-argument lambda", "sbcl --script sbcl_runner.lisp prepared …"),
        "chez": ("Read form and eval a zero-argument lambda", "chez --script chez_runner.scm prepared …"),
        "guile": ("Read form and eval a zero-argument lambda", "guile -s guile_runner.scm prepared …"),
        "luajit": ("Load source as a prepared Lua function", "luajit lua_runner.lua prepared …"),
        "bb": ("Read source and eval a zero-argument function", "bb bb_runner.clj prepared …"),
    }
    description, command = details[runtime]
    return {"description": description, "command": command}


def discover_runs(data_dir: Path) -> list[Path]:
    return sorted(p for p in data_dir.rglob("*.json") if p.name != "manifest.json")


def build(data_dir: Path, output: Path) -> int:
    runs = []
    for path in discover_runs(data_dir):
        data = read_json(path)
        if validate_run(data):
            continue
        runs.append(data)
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(ROOT / "site", output)
    (output / "data").mkdir()
    (output / "data" / "runs.json").write_text(
        json.dumps({"runs": runs}, separators=(",", ":")) + "\n", encoding="utf-8")
    (output / "data" / "catalog.json").write_text(
        json.dumps(source_catalog(), separators=(",", ":")) + "\n", encoding="utf-8")
    return len(runs)
