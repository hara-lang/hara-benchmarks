import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "suites/language/general-workloads.json"
RUST_SOURCES = ROOT / "suites/language/rust_workloads.json"
RUST_RUNNER = ROOT / "suites/language/rust_runner.py"


@unittest.skipUnless(shutil.which("rustc"), "Rust is not installed")
class RustRunnerTest(unittest.TestCase):
    def test_all_shared_workloads_match_checksums(self):
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))["workloads"]
        sources = json.loads(RUST_SOURCES.read_text(encoding="utf-8"))["workloads"]
        expected_ids = {workload["id"] for workload in corpus}
        self.assertEqual(set(sources), expected_ids)

        for workload in corpus:
            with self.subTest(workload=workload["id"]):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUST_RUNNER),
                        "prepared",
                        workload["id"],
                        sources[workload["id"]].encode().hex(),
                        workload["expected"],
                        "2",
                        "1",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=180,
                    check=True,
                )
                payload = json.loads(result.stdout.strip().splitlines()[-1])
                self.assertEqual(payload["runtime"], "rust")
                self.assertEqual(payload["workload"], workload["id"])
                self.assertGreater(payload["prepare_ns"], 0)
                self.assertGreater(payload["artifact_bytes"], 0)
                self.assertEqual(len(payload["samples_ns"]), 2)
                self.assertTrue(all(sample >= 0 for sample in payload["samples_ns"]))

    def test_eval_mode_is_rejected(self):
        result = subprocess.run(
            [sys.executable, str(RUST_RUNNER), "eval", "x", "00", "0", "1", "1"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prepared-only", result.stderr)


if __name__ == "__main__":
    unittest.main()
