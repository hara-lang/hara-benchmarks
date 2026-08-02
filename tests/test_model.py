import unittest
from pathlib import Path

from hara_bench.importers import import_language
from hara_bench.model import compare_hara, describe_hara_ratio, summarize, validate_run


class ModelTest(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(summarize([1, 2, 3])["p50"], 2)
        self.assertEqual(summarize([1, 2, 3])["p95"], 3)

    def test_valid_run(self):
        run = {"schema_version": 1, "run": {"id": "x", "profile": "smoke"},
               "environment": {}, "measurements": [{"suite": "a", "workload": "w",
               "runtime": "r", "status": "ok", "steady_state": {"samples_ns": [1]}}]}
        self.assertEqual(validate_run(run), [])

    def test_success_requires_samples(self):
        run = {"schema_version": 1, "run": {}, "environment": {}, "measurements": [
            {"suite": "a", "workload": "w", "runtime": "r", "status": "ok",
             "steady_state": {"samples_ns": []}}]}
        self.assertTrue(any("no steady-state" in e for e in validate_run(run)))

    def test_hara_comparison_uses_pairwise_common_workloads(self):
        rows = [
            {"runtime": "hara-rust-whole-wasm-prepared", "workload": "x", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [10]}},
            {"runtime": "hara-rust-whole-wasm-prepared", "workload": "y", "status": "unsupported", "mode": "prepared"},
            {"runtime": "c-prepared", "workload": "x", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [20]}},
            {"runtime": "c-prepared", "workload": "y", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [1]}},
        ]
        result = compare_hara(rows, "c-prepared")
        self.assertEqual(result["common"], ["x"])
        self.assertEqual(result["excluded"], ["y"])
        self.assertEqual((result["hara_supported"], result["comparator_supported"]), (1, 2))
        self.assertEqual(result["ratio"], 0.5)
        self.assertEqual(describe_hara_ratio(result["ratio"]), "Hara is 2.00× faster")

    def test_seed_hara_comparison_fixture(self):
        run = import_language(Path("seed/general-algorithms-comparison.json"))
        result = compare_hara(run["measurements"], "chez-prepared")
        self.assertAlmostEqual(result["ratio"], 1.778, places=3)
        self.assertEqual(len(result["common"]), 7)
        self.assertEqual(result["excluded"], ["sieve-array"])

    def test_ratio_language(self):
        self.assertEqual(describe_hara_ratio(2), "Hara is 2.00× slower")
        self.assertEqual(describe_hara_ratio(1.005), "Hara and the reference are approximately equal")


if __name__ == "__main__":
    unittest.main()
