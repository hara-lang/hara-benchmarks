import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_language_coverage import verify


class VerifyLanguageCoverageTest(unittest.TestCase):
    def write(self, measurements):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "language.json"
        path.write_text(json.dumps({"measurements": measurements}), encoding="utf-8")
        return path

    def test_accepts_real_measurements(self):
        rows = [
            {"runtime": runtime, "status": "ok", "samples_ns": [1]}
            for runtime in ("c-prepared", "chez-prepared")
            for _ in range(6)
        ]
        counts = verify(self.write(rows), ["c-prepared", "chez-prepared"], 6)
        self.assertEqual(counts, {"c-prepared": 6, "chez-prepared": 6})

    def test_rejects_all_unsupported_lane(self):
        rows = [
            {"runtime": "chez-prepared", "status": "unsupported", "reason": "failed"}
            for _ in range(8)
        ]
        with self.assertRaisesRegex(ValueError, "chez-prepared=0"):
            verify(self.write(rows), ["chez-prepared"], 6)


if __name__ == "__main__":
    unittest.main()
