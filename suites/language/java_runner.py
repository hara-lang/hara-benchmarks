#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


TEMPLATE = '''public final class HaraAlgorithmBenchmark {{
  {source}
  public static void main(String[] args) {{
    String id = args[0];
    long expected = Long.parseLong(args[1]);
    int windows = Integer.parseInt(args[2]), calls = Integer.parseInt(args[3]);
    long prepareNs = Long.parseLong(args[4]);
    long started = System.nanoTime();
    long value = benchmark();
    long first = System.nanoTime() - started;
    if (value != expected) throw new AssertionError(id + ": expected " + expected + ", got " + value);
    StringBuilder out = new StringBuilder("{{\\\"runtime\\\":\\\"java\\\",\\\"workload\\\":\\\"").append(id)
      .append("\\\",\\\"prepare_ns\\\":").append(prepareNs).append(",\\\"first_ns\\\":").append(first).append(",\\\"samples_ns\\\":[");
    for (int window = 0; window < windows; window++) {{
      started = System.nanoTime();
      for (int call = 0; call < calls; call++) value = benchmark();
      long sample = (System.nanoTime() - started) / calls;
      if (value != expected) throw new AssertionError(id + ": checksum changed");
      if (window != 0) out.append(',');
      out.append(sample);
    }}
    System.out.println(out.append("]}}").toString());
  }}
}}
'''


def main():
    if len(sys.argv) != 7:
        raise SystemExit("java_runner expects MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS")
    _, workload, source_hex, expected, windows, calls = sys.argv[1:]
    source = bytes.fromhex(source_hex).decode()
    java_home = os.environ.get("HARA_BENCH_JAVA_HOME")
    homebrew = Path("/opt/homebrew/opt/openjdk@21/bin")
    if java_home:
        javac, java = str(Path(java_home) / "bin/javac"), str(Path(java_home) / "bin/java")
    elif homebrew.is_dir():
        javac, java = str(homebrew / "javac"), str(homebrew / "java")
    else:
        javac, java = shutil.which("javac"), shutil.which("java")
    if not javac or not java:
        raise SystemExit("java and javac must be on PATH or HARA_BENCH_JAVA_HOME must be set")
    with tempfile.TemporaryDirectory(prefix="hara-java-bench-") as directory:
        root = Path(directory)
        source_path = root / "HaraAlgorithmBenchmark.java"
        prepare_started = time.perf_counter_ns()
        source_path.write_text(TEMPLATE.format(source=source))
        subprocess.run([javac, "-g:none", str(source_path)], check=True)
        prepare_ns = time.perf_counter_ns() - prepare_started
        completed = subprocess.run([java, "-cp", str(root), "HaraAlgorithmBenchmark",
                                    workload, expected, windows, calls, str(prepare_ns)])
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
