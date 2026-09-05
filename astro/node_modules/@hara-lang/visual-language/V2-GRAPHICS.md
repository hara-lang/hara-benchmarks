# Hara v2 graphics contract

The v2 graphics layer adds original monumental, painterly-industrial technology to Hara without turning the interface language into entertainment artwork or generic science-fiction UI.

Published laboratory:

**https://hara-lang.github.io/visual-language/v2/graphics/**

## Raster delivery library

`assets/cinematic/manifest.json` catalogues ten real high-resolution WebP graphics. These are the primary v2 art assets; the older SVG studies remain only for compatibility.

### Background masters

The six backgrounds live under `assets/cinematic/raster/backgrounds/` and are all `4096 × 2304`:

1. `monolith-gate.webp`
2. `desert-foundry.webp`
3. `nocturne-lattice.webp`
4. `reliquary-engine.webp`
5. `storm-archive.webp`
6. `ink-conduit.webp`

Use them for heroes, launch surfaces, editor canvases, covers, documentation bands, runtime fallbacks, and social crops.

### Texture masters

The four material textures live under `assets/cinematic/raster/textures/` and are all `4096 × 4096`:

1. `silica-drift.webp`
2. `oxide-patina.webp`
3. `carbon-weave.webp`
4. `phase-glass.webp`

They provide mineral, oxidised metal, woven-carbon, and optical-glass surface variation for panels, editor surrounds, document covers, inspection surfaces, and close crops.

The checked-in low-resolution seeds under `assets/cinematic/raster/seeds/` preserve reproducibility. Run `npm run assets:raster` to materialise or verify the 4K masters. The committed 4K outputs are the delivery assets used by the catalogue and GitHub Pages.

## Invariants

- The block H and signal dot remain fixed.
- Signal blue remains functional and visually sparse.
- Light and dark modes remain equivalent presentations of the same identity.
- Surfaces remain inspectable and compatible with working tools.
- Still raster imagery carries the complete composition before motion is enabled.
- Motion is progressive enhancement and never communicates required state by itself.

Avoid recognisable franchise characters, costumes, logos, signature props, decorative particle clouds, rainbow light, biological apertures, and continuous motion that does not reveal structure.

## Material atmospheres

| Atmosphere | Character |
| --- | --- |
| `monolith` | graphite mass, hard thresholds, isolated signal |
| `silica` | dry mineral light, long horizons, optical heat |
| `foundry` | inked carbon, rough process, machined containment |
| `nocturne` | operational night, structural ribs, sparse telemetry |
| `reliquary` | pale ceramic armour, archival seams, protected core |
| `storm` | directional pressure, vault geometry, charged atmosphere |

## Static raster use

```css
.hero {
  background:
    linear-gradient(90deg, rgba(5, 6, 8, .86), rgba(5, 6, 8, .12)),
    url("/cinematic/raster/backgrounds/monolith-gate.webp") center / cover no-repeat;
}

.editor-canvas {
  background:
    color-mix(in srgb, var(--hara-v2-panel) 92%, transparent),
    url("/cinematic/raster/textures/carbon-weave.webp") center / 720px auto repeat;
}
```

## WebGL shader fields

`ShaderField.astro` compiles real vertex and fragment shaders in the browser. Available modes are `strata`, `ink`, `monolith`, `lattice`, `shimmer`, and `field`.

```astro
<ShaderField
  mode="strata"
  atmosphere="silica"
  motion={true}
  interactive={true}
  fallback="/cinematic/raster/backgrounds/desert-foundry.webp"
  label="Dry Hara strata moving across a calibrated execution route"
/>
```

`motion` and `interactive` default to `false`.

The component pauses while off screen, caps device pixel ratio, honours reduced motion, updates with Hara light/dark changes, and retains a matched high-resolution raster image if WebGL is unavailable.

## Composition

Prefer one dominant field per viewport. Leave quiet zones around headings, prose, code, and controls. Signal blue should occupy less than five percent of most frames.

Raster imagery carries meaning. Shader motion may deepen the field, but must never be required to understand navigation, selection, runtime state, or content.
