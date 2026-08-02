import json
import tempfile
import unittest
from pathlib import Path

from hara_bench.site import build


class SiteTest(unittest.TestCase):
    def test_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "run.json").write_text(json.dumps({"schema_version": 1,
                "run": {"id": "x", "profile": "smoke"}, "environment": {},
                "measurements": []}))
            self.assertEqual(build(data, root / "dist"), 1)
            self.assertTrue((root / "dist/index.html").exists())
            catalog = json.loads((root / "dist/data/catalog.json").read_text())
            self.assertEqual(len(catalog["workloads"]), 8)
            self.assertIn("harness", catalog["workloads"][0]["implementations"]["hara"])

    def test_hara_centric_language_and_brand_tokens(self):
        html = Path("site/index.html").read_text()
        script = Path("site/app.js").read_text()
        css = Path("site/styles.css").read_text()
        self.assertIn("Hara against each reference", html)
        self.assertIn("Hara is", script)
        for forbidden in ("Runtime rankings", "fastest runtime", "win${", "cell-rank"):
            self.assertNotIn(forbidden, html + script)
        for token in ("#020408", "#071018", "#41f5e4", "#a7fff7", "#e4eff7", "#8da2b4", "#526a7b"):
            self.assertIn(token, css)
        self.assertIn(
            "const REFERENCE_ORDER=['c','java','chez','sbcl','luajit','python','bb','guile']",
            script,
        )
        for key in (
            "view", "run", "platform", "units", "category", "workload",
            "lifecycleComparator", "codeComparator", "phase",
        ):
            self.assertIn(f"p.set('{key}'", script)


if __name__ == "__main__":
    unittest.main()
