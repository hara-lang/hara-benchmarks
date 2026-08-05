import unittest

from scripts.verify_dashboard_data import (
    MIN_SHARED_WORKLOADS,
    REQUIRED_PREPARED_RUNTIMES,
    verify,
)


class VerifyDashboardDataTest(unittest.TestCase):
    def payload(self):
        measurements = []
        for runtime in REQUIRED_PREPARED_RUNTIMES:
            for index in range(MIN_SHARED_WORKLOADS):
                measurements.append({
                    "runtime": runtime,
                    "workload": f"workload-{index}",
                    "status": "ok",
                    "steady_state": {"samples_ns": [100 + index]},
                })
        return {
            "runs": [{
                "run": {"id": "test-run"},
                "environment": {
                    "timestamp": "2026-08-05T00:00:00+00:00",
                    "benchmark_revision": "a" * 40,
                },
                "measurements": measurements,
            }]
        }

    def test_accepts_complete_comparison_run(self):
        summary = verify(self.payload())
        self.assertEqual(summary["runtime_count"], len(REQUIRED_PREPARED_RUNTIMES))
        self.assertEqual(summary["minimum_shared_workloads"], MIN_SHARED_WORKLOADS)

    def test_rejects_missing_peer_measurements(self):
        payload = self.payload()
        missing = REQUIRED_PREPARED_RUNTIMES[-1]
        payload["runs"][0]["measurements"] = [
            row for row in payload["runs"][0]["measurements"]
            if row["runtime"] != missing
        ]
        with self.assertRaisesRegex(ValueError, missing):
            verify(payload)

    def test_rejects_invalid_benchmark_revision(self):
        payload = self.payload()
        payload["runs"][0]["environment"]["benchmark_revision"] = "fatal: dubious ownership"
        with self.assertRaisesRegex(ValueError, "immutable benchmark revision"):
            verify(payload)


if __name__ == "__main__":
    unittest.main()
