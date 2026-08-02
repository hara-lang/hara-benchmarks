import unittest

from hara_bench.model import summarize, validate_run


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


if __name__ == "__main__":
    unittest.main()

