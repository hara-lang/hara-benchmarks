import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");
const catalog = JSON.parse(await read("../../runtime/hara/catalog.json"));
const classEvidence = JSON.parse(
  await read("../../runtime/hara/results/class-reference.json")
);
const page = await read("../src/pages/index.astro");
const homepage = await read("../src/pages/homepage.json.ts");
const language = await read("../src/components/LanguagePanel.astro");
const classPanel = await read("../src/components/ClassPanel.astro");
const http = await read("../src/components/HttpPanel.astro");
const reference = await read("../src/components/RuntimeReference.astro");
const header = await read("../src/components/SiteHeader.astro");
const data = await read("../src/lib/benchmark-data.ts");
const languageStyles = await read("../src/styles/language.css");
const prepare = await read("../../scripts/prepare_presentation_data.py");
const workflow = await read("../../.github/workflows/pages.yml");
const mirror = await read("../scripts/mirror-origin.mjs");
const verifier = await read("../scripts/verify-build.mjs");
const packageJson = JSON.parse(await read("../package.json"));
const source = [page, language, classPanel, http, reference, header, data].join("\n");
const indexOf = (value) => {
  const index = language.indexOf(value);
  assert.notEqual(index, -1, `Expected language panel to contain ${value}`);
  return index;
};

test("uses the nine canonical internal artifacts", () => {
  assert.deepEqual(catalog.artifacts.map(({ id }) => id), [
    "hara-wasm-core", "hara-rust-vm", "hara-rust-full",
    "hara-wasm-vm", "hara-wasm-full", "hara-truffle-vm",
    "hara-truffle-full", "hara-jvm-vm", "hara-jvm-full"
  ]);
});

test("opens on a four-tab class-first presentation", () => {
  assert.equal((page.match(/<button role="tab"/g) ?? []).length, 4);
  assert.match(page, /aria-selected="true" aria-controls="class-comparison"/);
  assert.doesNotMatch(source, /aria-controls="methodology"|id="methodology"/);
});

test("serves every measured class, Lisp and reference runtime", () => {
  assert.deepEqual(catalog.class_competitors, ["luajit", "pypy", "node", "ruby-yjit", "clojure"]);
  assert.deepEqual(catalog.lisp_competitors, ["sbcl", "chez", "guile", "bb", "clojure"]);
  assert.deepEqual(catalog.reference_competitors, ["rust", "c", "java", "python"]);
  assert.match(classPanel, /id="class-comparison"/);
  assert.match(classPanel, /Rust, C, Java and Python/);
  assert.match(classPanel, /data-comparison-cell/);
  assert.match(classPanel, /data-matrix-detail/);
  assert.match(data, /haraClassRuntime = "hara-rust-whole-wasm-prepared"/);
  assert.match(data, /"rust-prepared": "Rust"/);
  for (const runtime of [
    "pypy-prepared", "node-prepared", "ruby-yjit-prepared",
    "clojure-prepared", "rust-prepared"
  ]) {
    assert.ok(classEvidence.runtime_order.includes(runtime), `missing ${runtime}`);
  }
  for (const runtime of classEvidence.runtime_order) {
    const covered = new Set(classEvidence.measurements
      .filter((row) => row.runtime === runtime)
      .map((row) => row.workload));
    assert.ok(covered.size >= 6, `${runtime} has only ${covered.size} workloads`);
  }
});

test("owns evidence transformation and publication inside hara-benchmarks", () => {
  assert.match(prepare, /published-evidence/);
  assert.match(prepare, /language_path/);
  assert.match(prepare, /class_path/);
  assert.doesNotMatch(prepare, /hara-www|HARA_WORKSPACE_ROOT/);
  assert.match(workflow, /prepare_presentation_data\.py/);
  assert.match(workflow, /npm test --prefix astro/);
  assert.match(workflow, /npm run verify --prefix astro/);
  assert.match(workflow, /Smoke-test benchmark origin and canonical route/);
  assert.doesNotMatch(workflow, /Publish embeddable www bundle|HEAD:benchmark-site/);
  assert.ok(packageJson.scripts.build.includes("mirror-origin.mjs"));
  assert.equal(packageJson.scripts.verify, "node scripts/verify-build.mjs");
  assert.match(mirror, /resolve\(dist, "benchmarks"\)/);
  assert.match(verifier, /origin root and \/benchmarks\//);
});

test("publishes a bounded homepage evidence endpoint", () => {
  assert.match(homepage, /hara\.benchmarks-homepage\/v1/);
  for (const runtime of ["python-prepared", "bb-prepared", "sbcl-prepared"]) {
    assert.match(homepage, new RegExp(runtime));
  }
  assert.match(homepage, /hoplite-request/);
  assert.match(homepage, /https:\/\/www\.hara-lang\.org\/benchmarks\//);
  assert.doesNotMatch(homepage, /readFile|HARA_WORKSPACE_ROOT|hara-www/);
});

test("turns the HTTP matrix into route-labelled server cards on mobile", () => {
  assert.ok(http.includes('class="tab-panel http-panel"'));
  assert.ok(http.includes('class="matrix-scroll http-matrix-scroll"'));
  assert.ok(http.includes('class="comparison-matrix http-comparison-matrix"'));
  assert.ok((http.match(/class="http-route-label"/g) ?? []).length >= 3);
  assert.ok(http.includes('aria-label={`${server}, ${route}: ${result.text}`}'));
  assert.ok(languageStyles.includes(".http-route-label { display:none; }"));
  assert.ok(languageStyles.includes(".http-matrix-scroll{max-width:none;overflow:visible"));
  assert.ok(languageStyles.includes(".http-comparison-matrix tbody{display:grid;gap:.75rem}"));
  assert.ok(languageStyles.includes(".http-comparison-matrix tbody tr{display:grid;width:100%"));
});

test("puts overview and insights before the drill-down matrix", () => {
  const overview = indexOf("Overview");
  const topInsights = indexOf("Top insights");
  const matrix = indexOf("Hara comparison matrix");
  const explanation = indexOf("What just happened");
  const haraInsights = indexOf("Hara insights");
  assert.ok(overview < topInsights && topInsights < matrix && matrix < explanation && explanation < haraInsights);
  assert.match(language, /data-comparison-cell/);
  assert.match(language, /data-matrix-detail/);
});

test("explains methodology below each result instead of in a separate tab", () => {
  assert.match(language, /Equivalent work[\s\S]*Prepared execution[\s\S]*One Hara baseline[\s\S]*Geometric mean/);
  assert.match(page, /RuntimePanel/);
  assert.match(page, /HttpPanel/);
});

test("moves the product-mode table to a collapsed reference at the end", () => {
  assert.match(reference, /<details>/);
  assert.match(reference, /<th>Java<\/th>[\s\S]*<th>Native<\/th>[\s\S]*<th>Web<\/th>/);
  assert.ok(page.indexOf("RuntimeReference") > page.indexOf("LanguagePanel"));
});

test("uses the shared Hara navigation and sign-in button", () => {
  assert.match(header, /aria-current="page" aria-disabled="true">Benchmarks/);
  assert.match(header, /Benchmarks[\s\S]*Docs[\s\S]*Specs/);
  assert.doesNotMatch(header, />Source<\/a>/);
  assert.match(header, /https:\/\/specs\.hara-lang\.org\//);
  assert.ok(header.includes('href="https://id.hara-lang.org/">Sign in</a>'));
  assert.doesNotMatch(source, /api\/session|auth\/github|return_to/);
});

test("uses a dedicated maximum-resolution benchmark social card", () => {
  assert.match(page, /og-hara-benchmarks\.jpg/);
  assert.match(page, /og:image:width" content="1200"/);
  assert.match(page, /og:image:height" content="630"/);
});

test("external comparisons use only the native full Hara tier", () => {
  assert.match(data, /haraRuntime = "hara-rust-full"/);
  assert.match(language, /Every external row is compared only with/);
  assert.doesNotMatch(source, /hara-rust-vm[^<]*compet/);
});
