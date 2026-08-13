import assert from "node:assert/strict";
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dist = resolve(appRoot, "../dist");
const required = [
  "index.html",
  "homepage.json",
  "data/catalog.json",
  "data/runs.json",
  "assets/hara-favicon.svg",
  "og-hara-benchmarks.jpg",
  "benchmarks/index.html",
  "benchmarks/homepage.json",
  "benchmarks/data/catalog.json",
  "benchmarks/data/runs.json",
  "benchmarks/assets/hara-favicon.svg",
  "benchmarks/og-hara-benchmarks.jpg"
];

async function filesUnder(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) files.push(...await filesUnder(path));
    else if (entry.isFile()) files.push(path);
  }
  return files;
}

for (const path of required) {
  const info = await stat(resolve(dist, path));
  assert.ok(
    info.isFile() && info.size > 0,
    `missing non-empty benchmark artifact: ${path}`
  );
}

const root = await readFile(resolve(dist, "index.html"), "utf8");
const nested = await readFile(resolve(dist, "benchmarks/index.html"), "utf8");
assert.equal(
  nested,
  root,
  "origin root and /benchmarks/ must serve the same markup"
);
assert.match(
  root,
  /<link[^>]+rel=["']canonical["'][^>]+href=["']https:\/\/www\.hara-lang\.org\/benchmarks\/["']/i,
  "benchmark canonical URL must be exactly https://www.hara-lang.org/benchmarks/"
);
assert.match(root, /<title>Hara Benchmarks<\/title>/);
assert.match(root, /id=["']class-comparison["']/);
assert.match(root, /id=["']language-shootout["']/);
assert.match(root, /\/benchmarks\/_astro\//);
assert.doesNotMatch(root, /\/benchmarks\/benchmarks\//);
assert.doesNotMatch(root, /__VITE_ASSET__/);

const stylesheet = root.match(
  /href=["'](\/benchmarks\/_astro\/[^"']+\.css)["']/
)?.[1];
assert.ok(
  stylesheet,
  "benchmark page did not reference a canonical /benchmarks/_astro stylesheet"
);
const stylesheetPath = stylesheet.replace(/^\/benchmarks\//, "");
for (const path of [stylesheetPath, `benchmarks/${stylesheetPath}`]) {
  const info = await stat(resolve(dist, path));
  assert.ok(info.isFile() && info.size > 0, `missing built stylesheet: ${path}`);
}

const homepage = JSON.parse(
  await readFile(resolve(dist, "homepage.json"), "utf8")
);
const nestedHomepage = JSON.parse(
  await readFile(resolve(dist, "benchmarks/homepage.json"), "utf8")
);
assert.deepEqual(nestedHomepage, homepage);
assert.equal(homepage.schema, "hara.benchmarks-homepage/v1");
assert.equal(homepage.canonical_url, "https://www.hara-lang.org/benchmarks/");
assert.ok(homepage.workloads >= 6);
for (const runtime of ["python-prepared", "bb-prepared", "sbcl-prepared"]) {
  assert.equal(
    typeof homepage.ratios[runtime],
    "number",
    `missing homepage ratio for ${runtime}`
  );
}

const runs = JSON.parse(await readFile(resolve(dist, "data/runs.json"), "utf8"));
assert.ok(
  Array.isArray(runs.runs) && runs.runs.length > 0,
  "published benchmark history is empty"
);

const allFiles = await filesUnder(dist);
for (const path of allFiles.filter((value) =>
  /\.(?:css|html|js|json|mjs|xml)$/.test(value)
)) {
  const body = await readFile(path, "utf8");
  assert.doesNotMatch(
    body,
    /\/benchmarks\/benchmarks\//,
    `doubled base URL in ${relative(dist, path)}`
  );
  assert.doesNotMatch(
    body,
    /__VITE_ASSET__/,
    `unresolved Vite asset in ${relative(dist, path)}`
  );
}

const relativeFiles = allFiles.map((path) =>
  relative(dist, path).split(sep).join("/")
);
console.log(
  `verified ${relativeFiles.length} independent benchmark artifact files at ${dist}`
);
