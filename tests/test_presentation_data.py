from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_presentation_data.py"
SPEC = importlib.util.spec_from_file_location("prepare_presentation_data", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PresentationDataTest(unittest.TestCase):
    def test_selects_latest_complete_run_and_emits_both_hara_identities(self):
        workloads = [f"workload-{index}" for index in range(6)]
        catalog = {
            "runtime_catalog": {
                "display_order": ["python", "bb", "racket"],
                "runtimes": {
                    "python": {
                        "status": "measured",
                        "runtime_prefix": "python-",
                    },
                    "bb": {
                        "status": "measured",
                        "runtime_prefix": "bb-",
                    },
                    "racket": {
                        "status": "planned",
                        "runtime_prefix": "racket-",
                    },
                },
            }
        }

        def rows(include_bb: bool) -> list[dict]:
            runtimes = [
                ("hara-rust-whole-wasm-prepared", 1),
                ("python-prepared", 4),
            ]
            if include_bb:
                runtimes.append(("bb-prepared", 2))
            return [
                {
                    "runtime": runtime,
                    "workload": workload,
                    "status": "ok",
                    "steady_state": {
                        "samples_ns": [factor * 10, factor * 11, factor * 12]
                    },
                }
                for runtime, factor in runtimes
                for workload in workloads
            ]

        incomplete = {
            "run": {"id": "newer-incomplete", "profile": "smoke"},
            "environment": {"timestamp": "2026-08-07T00:00:00Z"},
            "measurements": rows(False),
        }
        complete = {
            "run": {"id": "canonical-complete", "profile": "smoke"},
            "environment": {"timestamp": "2026-08-06T00:00:00Z"},
            "measurements": rows(True),
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "catalog.json"
            runs_path = root / "runs.json"
            language_path = root / "language.json"
            class_path = root / "classes.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            runs_path.write_text(
                json.dumps({"runs": [incomplete, complete]}),
                encoding="utf-8",
            )

            result = MODULE.prepare(
                catalog_path,
                runs_path,
                language_path,
                class_path,
            )
            language = json.loads(language_path.read_text(encoding="utf-8"))
            classes = json.loads(class_path.read_text(encoding="utf-8"))

        self.assertEqual(result["run_id"], "canonical-complete")
        self.assertEqual(result["runtime_count"], 3)
        self.assertEqual(result["workload_count"], 6)
        self.assertEqual(
            language["runtime_order"],
            ["python-prepared", "bb-prepared", "hara-rust-full"],
        )
        self.assertEqual(
            classes["runtime_order"],
            [
                "hara-rust-whole-wasm-prepared",
                "python-prepared",
                "bb-prepared",
            ],
        )
        self.assertEqual(
            language["environment"]["benchmark_data_source"],
            "hara-lang/hara-benchmarks:published-evidence",
        )
        self.assertFalse(any(
            row["runtime"] == "hara-rust-whole-wasm-prepared"
            for row in language["measurements"]
        ))
        self.assertTrue(any(
            row["runtime"] == "hara-rust-full"
            for row in language["measurements"]
        ))

    def test_rejects_history_without_a_complete_measured_peer_set(self):
        catalog = {
            "runtime_catalog": {
                "display_order": ["python"],
                "runtimes": {
                    "python": {
                        "status": "measured",
                        "runtime_prefix": "python-",
                    }
                },
            }
        }
        run = {
            "environment": {"timestamp": "2026-08-06T00:00:00Z"},
            "measurements": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "catalog.json").write_text(
                json.dumps(catalog),
                encoding="utf-8",
            )
            (root / "runs.json").write_text(
                json.dumps({"runs": [run]}),
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                MODULE.prepare(
                    root / "catalog.json",
                    root / "runs.json",
                    root / "language.json",
                    root / "classes.json",
                )


if __name__ == "__main__":
    unittest.main()
