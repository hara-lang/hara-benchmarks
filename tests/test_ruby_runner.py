import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "suites/language/general-workloads.json"
RUBY_SOURCES = ROOT / "suites/language/ruby_workloads.json"
RUBY_RUNNER = ROOT / "suites/language/ruby_runner.rb"


def yjit_available() -> bool:
    if not shutil.which("ruby"):
        return False
    try:
        return subprocess.run(
            [
                "ruby",
                "--yjit",
                "-e",
                "exit(defined?(RubyVM::YJIT) && RubyVM::YJIT.enabled? ? 0 : 1)",
            ],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


@unittest.skipUnless(yjit_available(), "Ruby with YJIT is not installed")
class RubyRunnerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads(CORPUS.read_text(encoding="utf-8"))["workloads"]
        cls.sources = json.loads(RUBY_SOURCES.read_text(encoding="utf-8"))["workloads"]

    def test_all_shared_workloads_match_checksums(self):
        expected_ids = {workload["id"] for workload in self.corpus}
        self.assertEqual(set(self.sources), expected_ids)

        for workload in self.corpus:
            with self.subTest(workload=workload["id"]):
                result = subprocess.run(
                    [
                        "ruby",
                        "--yjit",
                        str(RUBY_RUNNER),
                        "prepared",
                        workload["id"],
                        self.sources[workload["id"]].encode().hex(),
                        workload["expected"],
                        "3",
                        "1",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=120,
                    check=True,
                )
                payload = json.loads(result.stdout.strip().splitlines()[-1])
                self.assertEqual(payload["runtime"], "ruby-yjit")
                self.assertEqual(payload["workload"], workload["id"])
                self.assertTrue(payload["yjit_enabled"])
                self.assertEqual(len(payload["samples_ns"]), 3)
                self.assertTrue(all(sample >= 0 for sample in payload["samples_ns"]))

    def test_runner_rejects_disabled_yjit(self):
        workload = self.corpus[0]
        result = subprocess.run(
            [
                "ruby",
                str(RUBY_RUNNER),
                "prepared",
                workload["id"],
                self.sources[workload["id"]].encode().hex(),
                workload["expected"],
                "0",
                "1",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("YJIT is not enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
