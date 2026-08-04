import json
import tempfile
import unittest
from pathlib import Path

from hara_bench.site import build, runtime_catalog


class SiteTest(unittest.TestCase):
    def test_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "run.json").write_text(json.dumps({"schema_version": 3,
                "run": {"id": "x", "profile": "smoke"}, "environment": {},
                "measurements": []}))
            self.assertEqual(build(data, root / "dist"), 1)
            catalog = json.loads((root / "dist/data/catalog.json").read_text())
            self.assertEqual(len(catalog["workloads"]), 8)
            self.assertIn("runtime_catalog", catalog)
            for workload in catalog["workloads"]:
                implementations = workload["implementations"]
                self.assertIn("pypy", implementations)
                self.assertIn("clojure", implementations)
                self.assertIn("node", implementations)
                self.assertEqual(
                    implementations["bb"]["source"],
                    implementations["clojure"]["source"],
                )

    def test_runtime_taxonomy(self):
        catalog = runtime_catalog()
        self.assertEqual(catalog["runtimes"]["hara"]["groups"], ["dynamic-jit", "lisp"])
        self.assertIn("dynamic-jit", catalog["runtimes"]["pypy"]["groups"])
        self.assertEqual(catalog["runtimes"]["node"]["status"], "measured")
        self.assertEqual(catalog["runtimes"]["node"]["groups"], ["dynamic-jit"])
        self.assertEqual(catalog["runtimes"]["clojure"]["status"], "measured")
        self.assertEqual(
            catalog["runtimes"]["clojure"]["groups"],
            ["dynamic-jit", "lisp"],
        )
        self.assertIn("reference-native", catalog["runtimes"]["c"]["groups"])
        self.assertIn("reference-managed", catalog["runtimes"]["java"]["groups"])

    def test_class_language_and_brand_tokens(self):
        html = Path("site/index.html").read_text()
        script = Path("site/app.js").read_text()
        css = Path("site/styles.css").read_text() + Path("site/classes.css").read_text()
        self.assertIn("Hara against dynamic JIT peers", html)
        self.assertIn("Lisp family", html)
        self.assertIn("Reference ceilings", html)
        self.assertIn("runtime_catalog", script)
        self.assertIn("Hara is", script)
        for forbidden in ("Runtime rankings", "fastest runtime", "cell-rank"):
            self.assertNotIn(forbidden, html + script)
        for token in ("#020408", "#071018", "#41f5e4", "#e4eff7", "#8da2b4", "#526a7b"):
            self.assertIn(token, css)
        for key in ("view", "run", "units", "workload", "lifecycleComparator", "codeComparator", "phase"):
            self.assertIn(f"params.set('{key}'", script)


if __name__ == "__main__":
    unittest.main()
