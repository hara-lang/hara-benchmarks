import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const base = process.env.HARA_BENCHMARK_BASE || "/benchmarks";
const site = "https://www.hara-lang.org";
const outDir = process.env.HARA_BENCHMARK_OUT_DIR || "../dist";
const appRoot = dirname(fileURLToPath(import.meta.url));
const sharedHeaderController = resolve(appRoot, "packages/hara-ui/foundation/v2/header.js");

export default defineConfig({
  site,
  base,
  output: "static",
  outDir,
  integrations: [sitemap()],
  vite: {
    resolve: {
      alias: {
        "@hara-lang/ui/v2/header.js": sharedHeaderController
      }
    }
  }
});
