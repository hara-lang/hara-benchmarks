import {
  comparisonRows,
  evidence,
  evidenceDate,
  workloads
} from "../lib/benchmark-data";

export const prerender = true;

const homepageRuntimes = ["python-prepared", "bb-prepared", "sbcl-prepared"];

export function GET() {
  const ratios = Object.fromEntries(
    homepageRuntimes.map((runtime) => [
      runtime,
      comparisonRows.find((row) => row.runtime === runtime)?.overallRatio ?? null
    ])
  );
  const hopliteHello = evidence?.http_measurements?.find((row) =>
    row.server === "hoplite-request"
    && row.route === "/hello"
    && row.status === "ok"
  );
  const payload = {
    schema: "hara.benchmarks-homepage/v1",
    canonical_url: "https://www.hara-lang.org/benchmarks/",
    published: evidenceDate,
    workloads: workloads.length,
    comparison_runtimes: comparisonRows.length,
    ratios,
    http: {
      server: "hoplite-request",
      route: "/hello",
      requests_per_second: hopliteHello?.requests_per_second ?? null
    }
  };
  return new Response(`${JSON.stringify(payload, null, 2)}\n`, {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=300"
    }
  });
}
