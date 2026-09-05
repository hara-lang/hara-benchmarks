# Hara Open Graph imagery

Hara social cards use six maximum-resolution material scenes on a `3840 × 2016`
canvas. The ratio is exactly `40:21`, matching the standard `1200 × 630` Open
Graph crop while preserving a high-resolution source for modern displays.

The family combines quiet precision-machined graphite with a restrained number
of substantial, hand-cut glass pieces. Cyan → blue → violet communicates live
state, evaluation, and emergence. Visible dark joins keep the glass physical and
inspectable. The treatment deliberately avoids generic cyberpunk dashboards,
orbital atoms, grid floors, particle noise, security clichés, crypto symbolism,
and unrelated warm accent colours.

| Scene | Meaning | Cards |
| --- | --- | --- |
| Evaluation | One value crossing an inspectable evaluation boundary | Hara |
| Syntax | A nested form becoming a readable tree | Docs, Specifications |
| Workbench | Source, evaluation, and output as rearrangeable layers | Playground, CLI |
| Registry | Versioned modules forming one verifiable path | Packages, Registry API, Identity |
| Measure | A calibrated aperture with visible runtime phases | Benchmarks, Status |
| Materials | Edge, aperture, and rack as one component family | UI, Visual language |

Text and the canonical interlocking Hara mark are composed deterministically by
`scripts/build-og.mjs`; generated scene artwork never contains embedded copy.
Run `npm run assets:og` after changing a master or card definition. The build
requires Inkscape and ImageMagick's `convert` command.
