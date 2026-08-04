import json
import tempfile
import unittest
from pathlib import Path

from scripts.publish_results import publish


class PublishResultsTest(unittest.TestCase):
    def test_valid_run_is_promoted_to_stable_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs, output = root / "inputs", root / "history"
            inputs.mkdir()
            run = {
                "schema_version": 3,
                "run": {"id": "2026-08-05T01-02-03+00-00", "profile": "nightly"},
                "environment": {"os": "linux", "architecture": "x86_64"},
                "measurements": [],
            }
            (inputs / "normalized.json").write_text(json.dumps(run))
            written = publish(inputs, output)
            self.assertEqual(len(written), 1)
            self.assertEqual(written[0].relative_to(output).parts[:4], ("runs", "linux", "x86_64", "nightly"))
            self.assertTrue((output / "manifest.json").exists())

    def test_invalid_run_is_not_published(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs, output = root / "inputs", root / "history"
            inputs.mkdir()
            (inputs / "normalized.json").write_text('{}')
            with self.assertRaises(ValueError):
                publish(inputs, output)


if __name__ == "__main__":
    unittest.main()
