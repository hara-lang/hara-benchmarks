import unittest
from pathlib import Path

from hara_bench.importers import import_language
from hara_bench.model import rank_runtimes, summarize, validate_run


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

    def test_geometric_ranking_uses_common_workloads(self):
        rows = [
            {"runtime": "a", "workload": "x", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [10]}},
            {"runtime": "a", "workload": "y", "status": "unsupported", "mode": "prepared"},
            {"runtime": "b", "workload": "x", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [20]}},
            {"runtime": "b", "workload": "y", "status": "ok", "mode": "prepared", "steady_state": {"samples_ns": [1]}},
        ]
        ranked = rank_runtimes(rows)
        self.assertEqual([row["runtime"] for row in ranked], ["a", "b"])
        self.assertEqual(ranked[0]["common"], ["x"])
        self.assertEqual((ranked[0]["supported"], ranked[0]["total"]), (1, 2))

    def test_seed_ranking_fixture(self):
        run = import_language(Path("seed/general-algorithms-comparison.json"))
        ranked = rank_runtimes(run["measurements"])
        scores = {row["runtime"]: row["score"] for row in ranked}
        self.assertEqual(ranked[0]["runtime"], "chez-prepared")
        self.assertAlmostEqual(scores["chez-prepared"], 1.428, places=3)
        self.assertAlmostEqual(scores["hara-rust-whole-wasm-prepared"], 2.540, places=3)
        self.assertEqual(len(ranked[0]["common"]), 7)


if __name__ == "__main__":
    unittest.main()
