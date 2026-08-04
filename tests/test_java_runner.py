import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "suites/language/java_runner.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("hara_java_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class JavaRunnerTest(unittest.TestCase):
    def test_invalid_configured_home_falls_back_to_path(self):
        runner = load_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            javac = root / "javac"
            java = root / "java"
            javac.touch()
            java.touch()
            with mock.patch.dict(
                os.environ,
                {"HARA_BENCH_JAVA_HOME": str(root / "missing")},
                clear=False,
            ), mock.patch.object(
                runner.shutil,
                "which",
                side_effect=lambda name: str(javac if name == "javac" else java),
            ):
                self.assertEqual(runner.java_tools(), (str(javac), str(java)))

    def test_valid_configured_home_is_preferred(self):
        runner = load_runner()
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            binary = home / "bin"
            binary.mkdir()
            javac = binary / "javac"
            java = binary / "java"
            javac.touch()
            java.touch()
            with mock.patch.dict(
                os.environ,
                {"HARA_BENCH_JAVA_HOME": str(home)},
                clear=False,
            ), mock.patch.object(runner.shutil, "which") as which:
                self.assertEqual(runner.java_tools(), (str(javac), str(java)))
                which.assert_not_called()


if __name__ == "__main__":
    unittest.main()
