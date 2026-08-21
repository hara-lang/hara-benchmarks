import { access, cp, mkdir, readFile, rm } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const acceptedRevision = "a2ab66d0fde79edb1cee46b79528098b3fda68cf";
const packageRoot = resolve(appRoot, "packages/visual-language");
const installedRoot = resolve(appRoot, "node_modules/@hara-lang/visual-language");
const requiredExports = [
  "./theme.css",
  "./motifs.css",
  "./v2.css",
  "./v2-data.css",
  "./theme.js",
  "./astro/ThemeToggle.astro",
  "./astro/v2/Header.astro"
];
const requiredDocuments = ["V2-GUIDE.md", "V2-DATA-VISUALISATION.md"];

const exists = async (path) => {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
};

const manifestPath = resolve(packageRoot, "package.json");
if (!(await exists(manifestPath))) {
  throw new Error(
    `missing accepted @hara-lang/visual-language checkout at ${packageRoot}; ` +
    `CI checks out ${acceptedRevision} before benchmark presentation validation`
  );
}

const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
if (manifest.name !== "@hara-lang/visual-language") {
  throw new Error(`wrong visual-language package at ${packageRoot}: ${manifest.name}`);
}
for (const name of requiredExports) {
  const exported = manifest.exports?.[name];
  if (typeof exported !== "string" || !(await exists(resolve(packageRoot, exported)))) {
    throw new Error(`accepted visual-language revision is missing ${name}`);
  }
}
for (const name of requiredDocuments) {
  if (!(await exists(resolve(packageRoot, name)))) {
    throw new Error(`accepted visual-language revision is missing ${name}`);
  }
}

const packageEntries = ["package.json", ...new Set(manifest.files ?? [])];
await rm(installedRoot, { recursive: true, force: true });
await mkdir(installedRoot, { recursive: true });
for (const entry of packageEntries) {
  if (typeof entry !== "string" || entry.includes("*") || entry.includes("\0")) {
    throw new Error(`unsupported visual-language package entry: ${String(entry)}`);
  }
  const from = resolve(packageRoot, entry);
  const to = resolve(installedRoot, entry);
  if (from !== packageRoot && !from.startsWith(`${packageRoot}${sep}`)) {
    throw new Error(`visual-language package entry escapes its root: ${entry}`);
  }
  if (!(await exists(from))) throw new Error(`visual-language package entry is missing: ${entry}`);
  await mkdir(dirname(to), { recursive: true });
  await cp(from, to, { recursive: true, dereference: true });
}

console.log(
  `using materialised @hara-lang/visual-language ${manifest.version} at ${acceptedRevision} ` +
  `(${packageEntries.length} published entries)`
);
