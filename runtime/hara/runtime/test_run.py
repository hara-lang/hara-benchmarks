import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("run.py")
SPEC = importlib.util.spec_from_file_location("runtime_benchmark", MODULE_PATH)
BENCHMARK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BENCHMARK)


def measurement(runtime, workload, steady_ns):
    return {
        "runtime": runtime,
        "workload": workload,
        "analysis": {"steady_ns": steady_ns},
    }


class RegressionRulesTest(unittest.TestCase):
    def test_expands_candidate_pairs_with_candidate_specific_expected_values(self):
        rows = BENCHMARK.expand_workloads([{
            "id": "predicate",
            "lane": "surface",
            "expected": {"split": "false", "unified": "true"},
            "candidates": {
                "split": {"source": "(split 1)"},
                "unified": {"source": "(unified 1)"},
            },
        }])
        self.assertEqual([row["id"] for row in rows], ["predicate/split", "predicate/unified"])
        self.assertEqual([row["pair_id"] for row in rows], ["predicate", "predicate"])
        self.assertEqual([row["candidate"] for row in rows], ["split", "unified"])
        self.assertEqual([row["expected"] for row in rows], ["false", "true"])

    def test_candidate_comparisons_are_evidence_without_a_threshold(self):
        measurements = [
            {"runtime": "hara-rust-vm", "pair_id": "predicate", "candidate": "split",
             "lane": "surface", "analysis": {"steady_ns": 100}},
            {"runtime": "hara-rust-vm", "pair_id": "predicate", "candidate": "unified",
             "lane": "surface", "analysis": {"steady_ns": 125}},
        ]
        comparison = BENCHMARK.candidate_comparisons(measurements)[0]
        self.assertEqual(comparison["pair_id"], "predicate")
        self.assertEqual(comparison["unified_over_split"], 1.25)
        self.assertEqual(comparison["faster_candidate"], "split")

    def test_candidate_comparisons_ignore_unsupported_rows(self):
        measurements = [
            {"runtime": "hara-rust-full", "pair_id": "wide", "candidate": "split",
             "lane": "kernel", "status": "unsupported"},
            {"runtime": "hara-rust-full", "pair_id": "wide", "candidate": "unified",
             "lane": "kernel", "status": "unsupported"},
        ]
        self.assertEqual(BENCHMARK.candidate_comparisons(measurements), [])

    def test_candidate_comparisons_report_ties_without_picking_a_candidate(self):
        measurements = [
            {"runtime": "hara-rust-vm", "pair_id": "literal", "candidate": "split",
             "lane": "kernel", "analysis": {"steady_ns": 100}},
            {"runtime": "hara-rust-vm", "pair_id": "literal", "candidate": "unified",
             "lane": "kernel", "analysis": {"steady_ns": 100}},
        ]
        self.assertEqual(
            BENCHMARK.candidate_comparisons(measurements)[0]["faster_candidate"],
            "tie",
        )

    def test_integer_representation_corpus_has_two_rows_per_pair(self):
        path = Path(__file__).with_name("integer-representation-workloads.json")
        payload, rows = BENCHMARK.load_corpus(path)
        self.assertEqual(payload["benchmark"], "integer-representation")
        self.assertEqual(payload["issue"], "hara-lang/hara#1145")
        self.assertEqual(len(rows), len(payload["workloads"]) * 2)
        self.assertEqual({row["candidate"] for row in rows}, {"split", "unified"})
        self.assertTrue(all(row["id"].endswith(("/split", "/unified")) for row in rows))

    def test_integer_representation_corpus_matches_its_profile_contract(self):
        path = Path(__file__).with_name("integer-representation-workloads.json")
        payload = json.loads(path.read_text())
        self.assertEqual(payload["profiles"]["smoke"], {
            "startup_samples": 2, "windows": 3, "calls": 1,
        })
        self.assertEqual(payload["profiles"]["standard"], {
            "startup_samples": 30, "windows": 60, "calls": 10,
        })
        for workload in payload["workloads"]:
            self.assertEqual(set(workload["candidates"]), {"split", "unified"})
            self.assertIn(workload["lane"], {"kernel", "surface"})
            self.assertIn(workload["representation"], {"compact", "bigint"})

    def test_runtime_specific_sources_are_explicit_and_never_fall_back_silently(self):
        workload = {
            "id": "mutable-map-build",
            "source": "unused",
            "sources": {"bb": "(transient {})", "hara-rust-bytecode": "(to-mutable {})"},
        }
        self.assertEqual(
            BENCHMARK.workload_for_runtime(workload, "bb")["source"],
            "(transient {})",
        )
        self.assertIsNone(BENCHMARK.workload_for_runtime(workload, "hara-truffle"))

    def test_accepts_ratio_at_threshold(self):
        data = {"measurements": [
            measurement("bb", "arithmetic", 100),
            measurement("hara-rust-bytecode", "arithmetic", 90),
        ]}
        baseline = {"rules": [{
            "runtime": "hara-rust-bytecode",
            "workload": "arithmetic",
            "relative_to": "bb",
            "max_ratio": 0.90,
        }]}
        self.assertEqual(BENCHMARK.check_regressions(data, baseline), [])

    def test_reports_regression_and_missing_measurements(self):
        data = {"measurements": [
            measurement("bb", "arithmetic", 100),
            measurement("hara-rust-bytecode", "arithmetic", 95),
        ]}
        baseline = {"rules": [
            {"runtime": "hara-rust-bytecode", "workload": "arithmetic",
             "relative_to": "bb", "max_ratio": 0.90},
            {"runtime": "hara-rust-trace-checked", "workload": "arithmetic",
             "relative_to": "bb", "max_ratio": 0.60},
        ]}
        failures = BENCHMARK.check_regressions(data, baseline)
        self.assertIn("ratio 0.950 exceeds 0.900", failures[0])
        self.assertIn("missing measurement", failures[1])


if __name__ == "__main__":
    unittest.main()
