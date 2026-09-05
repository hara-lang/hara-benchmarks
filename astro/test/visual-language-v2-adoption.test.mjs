import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");
const acceptedRevision = "a2ab66d0fde79edb1cee46b79528098b3fda68cf";

test("benchmark publication pins and materialises the accepted visual-language contract", async () => {
  const [workflow, prepare, packageJson] = await Promise.all([
    read("../../.github/workflows/pages.yml"),
    read("../scripts/prepare-visual-language.mjs"),
    read("../package.json")
  ]);
  assert.match(workflow, /repository: hara-lang\/visual-language/);
  assert.match(workflow, new RegExp(`ref: ${acceptedRevision}`));
  assert.match(prepare, new RegExp(acceptedRevision));
  for (const value of ["./v2.css", "./v2-data.css", "V2-GUIDE.md", "V2-DATA-VISUALISATION.md"]) {
    assert.match(prepare, new RegExp(value.replaceAll(".", "\\.")));
  }
  assert.match(prepare, /manifest\.files/);
  assert.match(prepare, /await cp\(from, to, \{ recursive: true, dereference: true \}\)/);
  assert.match(prepare, /materialised @hara-lang\/visual-language/);
  assert.match(packageJson, /prepare:visual-language/);
});

test("the checked-out package source is not treated as benchmark application source", async () => {
  const tsconfig = JSON.parse(await read("../tsconfig.json"));
  assert.ok(tsconfig.exclude?.includes("packages/visual-language/**"));
  assert.equal(tsconfig.compilerOptions?.allowJs, true);
  assert.equal(tsconfig.compilerOptions?.checkJs, false);
});

test("the dashboard opts into v2 while preserving benchmark interaction authority", async () => {
  const [page, header, siteCss, adoption] = await Promise.all([
    read("../src/pages/index.astro"),
    read("../src/components/SiteHeader.astro"),
    read("../src/styles/site.css"),
    read("../src/styles/v2-adoption.css")
  ]);
  assert.match(siteCss, /@hara-lang\/visual-language\/v2\.css/);
  assert.match(siteCss, /@hara-lang\/visual-language\/v2-data\.css/);
  assert.match(page, /body class="hara-v2 benchmark-product"/);
  assert.match(page, /benchmark-skip-link/);
  assert.match(page, /mainId="benchmark-content"/);
  assert.match(page, /benchmark-evidence-contract/);
  assert.match(header, /astro\/v2\/Header\.astro/);
  assert.match(page, /history\.replaceState/);
  assert.match(page, /data-comparison-cell/);
  assert.doesNotMatch(adoption, /--hara-v2-[A-Za-z0-9_-]+\s*:/, "Benchmarks may consume but not redefine protected v2 tokens");
});

test("the product mapping preserves touch, focus, contained matrices and reduced motion", async () => {
  const css = await read("../src/styles/v2-adoption.css");
  assert.match(css, /min-height:\s*44px/);
  assert.match(css, /:focus-visible/);
  assert.match(css, /\.benchmark-product \.matrix-scroll\s*\{/);
  assert.match(css, /overflow:\s*auto/);
  assert.match(css, /scroll-margin-top/);
  assert.match(css, /@media \(prefers-reduced-motion: reduce\)/);
});
