from __future__ import annotations

import json
import shutil
from pathlib import Path

from .model import read_json, validate_run


ROOT = Path(__file__).resolve().parents[1]


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
    return len(runs)

