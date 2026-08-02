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


if __name__ == "__main__":
    unittest.main()
