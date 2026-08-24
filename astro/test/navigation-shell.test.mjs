import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");
const haraUiRevision = "0e8a9d3d0f6ba9c9aedb8e6ddb48d758a40517a5";

test("publication checks out the merged shared Hara header contract without scanning the package source", async () => {
  const [workflow, config, tsconfig] = await Promise.all([
    read("../../.github/workflows/pages.yml"),
    read("../astro.config.mjs"),
    read("../tsconfig.json")
  ]);

  assert.match(workflow, /repository: hara-lang\/hara-ui/);
  assert.match(workflow, new RegExp(`ref: ${haraUiRevision}`));
  assert.match(workflow, /path: astro\/packages\/hara-ui/);
  assert.match(config, /@hara-lang\/ui\/v2\/header\.js/);
  assert.match(config, /packages\/hara-ui\/foundation\/v2\/header\.js/);
  assert.match(tsconfig, /"@hara-lang\/ui\/v2\/header\.js"/);
  assert.match(tsconfig, /"packages\/hara-ui\/foundation\/v2\/header\.js"/);
  assert.match(tsconfig, /"packages\/hara-ui\/\*\*"/);
});

test("the benchmark shell uses one product hamburger and one all-width context line", async () => {
  const [page, header, secondary] = await Promise.all([
    read("../src/pages/index.astro"),
    read("../src/components/SiteHeader.astro"),
    read("../src/components/BenchmarkSecondaryNav.astro")
  ]);

  assert.match(page, /<SiteHeader \/>[\s\S]*<BenchmarkSecondaryNav \/>/);
  assert.match(header, /packages\/hara-ui\/foundation\/astro\/v2\/Header\.astro/);
  assert.match(header, /menuMode="product"/);
  assert.match(header, /menuControls="benchmark-product-menu"/);
  assert.match(header, /hara:header-menu-request/);
  assert.match(header, /data-benchmark-menu-close/);
  assert.match(header, /title="Close benchmark menu"/);

  assert.match(secondary, /data-suite-open="false"/);
  assert.match(secondary, /data-evidence-open="false"/);
  assert.match(secondary, /if \(open\) setEvidenceOpen\(false\)/);
  assert.match(secondary, /if \(open\) setSuiteOpen\(false\)/);
  assert.match(secondary, /event\.key !== "Escape"/);
  assert.match(secondary, /\[role="tab"\]\[aria-controls=/);
  assert.doesNotMatch(secondary, /matchMedia/);
});

test("the context shell stays compact and non-floating at every viewport", async () => {
  const css = await read("../src/styles/shell.css");
  const shellStart = css.indexOf(".benchmark-secondary {");
  const shellEnd = css.indexOf("}", shellStart);
  const shellRule = css.slice(shellStart, shellEnd + 1);

  assert.match(shellRule, /position: relative/);
  assert.match(shellRule, /isolation: isolate/);
  assert.match(shellRule, /min-height: 48px/);
  assert.match(shellRule, /max-height: 48px/);
  assert.doesNotMatch(shellRule, /position:\s*(?:sticky|fixed)/);
  assert.doesNotMatch(shellRule, /top:\s*var\(--hara-v2-header-height\)/);
  assert.match(css, /\.benchmark-secondary__line \{[\s\S]*?display: flex;[\s\S]*?max-height: 48px;/);
  assert.match(css, /\.benchmark-secondary__panel \{[\s\S]*?position: absolute;[\s\S]*?top: 100%;[\s\S]*?left: clamp\(12px, 2vw, 28px\);[\s\S]*?width: min\(360px, calc\(100vw - 56px\)\);/);
  assert.match(css, /@media \(max-width: 840px\)[\s\S]*?\.benchmark-secondary__panel \{[\s\S]*?right: 0;[\s\S]*?left: 0;[\s\S]*?width: 100%;/);
  assert.match(css, /min-height: 44px/);
  assert.match(css, /@media \(prefers-reduced-motion: reduce\)/);
  assert.doesNotMatch(css, /\.tabs \{[\s\S]*?position:\s*sticky/);
  assert.match(css, /scroll-margin-top: calc\(var\(--hara-v2-header-height\) \+ 1rem\)/);
  assert.doesNotMatch(css, /--hara-v2-[A-Za-z0-9_-]+\s*:/, "Benchmarks may consume but not redefine protected v2 tokens");
});

test("secondary navigation points at real benchmark evidence without changing tab authority", async () => {
  const [page, secondary, reference] = await Promise.all([
    read("../src/pages/index.astro"),
    read("../src/components/BenchmarkSecondaryNav.astro"),
    read("../src/components/RuntimeReference.astro")
  ]);

  for (const id of ["benchmark-summary", "evidence-contract", "benchmark-results"]) {
    assert.match(page, new RegExp(`id="${id}"`));
    assert.match(secondary, new RegExp(id));
  }
  assert.match(reference, /id="runtime-reference"/);
  assert.match(secondary, /runtime-reference/);
  for (const id of ["class-comparison", "language-shootout", "http-results", "hara-artifacts"]) {
    assert.match(page, new RegExp(`aria-controls="${id}"`));
    assert.match(secondary, new RegExp(id));
  }
  assert.match(page, /history\.replaceState/);
});
