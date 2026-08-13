import { cp, mkdir, readdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dist = resolve(appRoot, "../dist");
const mirror = resolve(dist, "benchmarks");

await rm(mirror, { recursive: true, force: true });
await mkdir(mirror, { recursive: true });

let copied = 0;
for (const entry of await readdir(dist, { withFileTypes: true })) {
  if (entry.name === "benchmarks") continue;
  await cp(resolve(dist, entry.name), resolve(mirror, entry.name), {
    recursive: entry.isDirectory()
  });
  copied += 1;
}

console.log(`mirrored ${copied} benchmark artifact entries under ${mirror}`);
