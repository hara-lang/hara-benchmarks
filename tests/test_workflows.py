import unittest
from pathlib import Path


class WorkflowContractTest(unittest.TestCase):
    def test_canonical_results_publish_after_relevant_main_pushes(self):
        workflow = Path(".github/workflows/benchmarks.yml").read_text(encoding="utf-8")
        self.assertIn("push:\n    branches: [main]", workflow)
        self.assertIn('if [ "${{ github.event_name }}" = "push" ]; then', workflow)
        self.assertIn("value=smoke", workflow)
        self.assertIn("- cron: '23 3 * * *'", workflow)
        self.assertIn("- cron: '41 4 * * 0'", workflow)
        self.assertIn("git push origin HEAD:benchmarks-data", workflow)

    def test_benchmark_data_push_rebuilds_pages_from_main(self):
        workflow = Path(".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("branches: [main, benchmarks-data]", workflow)
        self.assertIn("ref: main", workflow)
        self.assertIn(
            "git fetch origin benchmarks-data:refs/remotes/origin/benchmarks-data",
            workflow,
        )
        self.assertIn("git archive origin/benchmarks-data runs", workflow)
        self.assertNotIn("if: github.ref == 'refs/heads/main'", workflow)
        self.assertIn("uses: actions/deploy-pages@v4", workflow)


if __name__ == "__main__":
    unittest.main()
