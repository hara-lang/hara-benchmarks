import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "suites/language/general-workloads.json"
NODE_SOURCES = ROOT / "suites/language/node_workloads.json"
NODE_RUNNER = ROOT / "suites/language/node_runner.mjs"


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class NodeRunnerTest(unittest.TestCase):
    def test_all_shared_workloads_match_checksums(self):
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))["workloads"]
        sources = json.loads(NODE_SOURCES.read_text(encoding="utf-8"))["workloads"]
        expected_ids = {workload["id"] for workload in corpus}
        self.assertEqual(set(sources), expected_ids)

        for workload in corpus:
            with self.subTest(workload=workload["id"]):
                result = subprocess.run(
                    [
                        "node",
                        str(NODE_RUNNER),
                        "prepared",
                        workload["id"],
                        sources[workload["id"]].encode().hex(),
                        workload["expected"],
                        "3",
                        "1",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=60,
                    check=True,
                )
                payload = json.loads(result.stdout.strip().splitlines()[-1])
                self.assertEqual(payload["runtime"], "node")
                self.assertEqual(payload["workload"], workload["id"])
                self.assertEqual(len(payload["samples_ns"]), 3)
                self.assertTrue(all(sample >= 0 for sample in payload["samples_ns"]))


if __name__ == "__main__":
    unittest.main()
