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
        self.assertIn("git -C history push origin HEAD:benchmarks-data", workflow)

    def test_main_push_uses_the_complete_prepared_peer_set(self):
        workflow = Path(".github/workflows/benchmarks.yml").read_text(encoding="utf-8")
        prepared = (
            "hara-rust-whole-wasm-prepared", "luajit-prepared", "pypy-prepared",
            "node-prepared", "ruby-yjit-prepared", "clojure-prepared",
            "sbcl-prepared", "chez-prepared", "guile-prepared", "bb-prepared",
            "python-prepared", "c-prepared", "java-prepared",
        )
        for runtime in prepared:
            self.assertIn(f"--runtime {runtime}", workflow)
        runtime_line = next(
            line for line in workflow.splitlines()
            if line.strip().startswith('runtime_args="--runtime')
        )
        self.assertNotIn("-eval", runtime_line)
        self.assertIn("RUNTIME_ARGS: ${{ steps.profile.outputs.runtime_args }}", workflow)
        self.assertIn("$RUNTIME_ARGS", workflow)

    def test_canonical_container_installs_portable_java_clojure_and_chez(self):
        workflow = Path(".github/workflows/benchmarks.yml").read_text(encoding="utf-8")
        self.assertIn(
            "https://download.clojure.org/install/linux-install-1.12.5.1664.sh",
            workflow,
        )
        self.assertIn("repo.maven.apache.org/maven2/", workflow)
        self.assertIn("--retry 5 --retry-all-errors", workflow)
        self.assertIn("for attempt in 1 2 3 4 5", workflow)
        self.assertIn('echo "HARA_BENCH_JAVA_HOME=$java_home"', workflow)
        self.assertIn('ln -sf "$(command -v chezscheme)" /usr/local/bin/chez', workflow)
        self.assertIn("chez --version", workflow)
        self.assertIn('HARA_BENCHMARK_REVISION=$GITHUB_SHA', workflow)
        self.assertNotIn("cli: 1.12.5.1664", workflow)

    def test_smoke_exercises_java_chez_and_canonical_clojure_repository(self):
        workflow = Path(".github/workflows/smoke.yml").read_text(encoding="utf-8")
        self.assertIn("--runtime java-prepared", workflow)
        self.assertIn("--runtime chez-prepared", workflow)
        self.assertIn("apt-get install -y --no-install-recommends chezscheme", workflow)
        self.assertIn('ln -sf "$(command -v chezscheme)" /usr/local/bin/chez', workflow)
        self.assertIn("repo.maven.apache.org/maven2/", workflow)

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
