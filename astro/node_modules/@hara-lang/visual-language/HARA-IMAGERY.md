# Hara imagery and material system

Hara imagery is engineered rather than illustrated. It should feel like a
language kernel housed in an exact instrument: machined, inspectable, severe,
and built to survive sustained use.

The reference character is the **Rack** treatment used on the Hara benchmarks
hero. Edge, Aperture, and Rack remain the three primary environments. New
backgrounds and effects extend their material grammar; they do not replace or
reinterpret them.

## Live laboratory

The published visual language is available at:

**https://hara-lang.github.io/visual-language/**

The Pages site is rebuilt from `main` by `.github/workflows/pages.yml`.

## Direction

Hara combines four qualities:

- **precision engineering** — calibrated spacing, exact seams, routed conduits,
  instrument ticks, and visible construction;
- **military-grade restraint** — graphite, frost, brushed metal, one functional
  signal colour, and very little ornament;
- **gothic structure** — pointed vaults, lancet frames, ribs, tracery, and
  vertical tension;
- **alien intelligence** — unfamiliar proportions and non-human geometry
  without soft biological forms or fantasy decoration.

The identity is not whimsical, psychedelic, playful, organic, or cyberpunk.
Avoid auroras, multi-colour gradients, decorative particle fields, soft glowing
blobs, rotating orbits, breathing logos, and mascot-like motifs.

## Core material palette

- **Signal** `#2F7CFF` — state, focus, execution, and active instrumentation
- **Signal soft** `#8DB2FF` — sparse secondary illumination
- **Void** `#050608` — dark ground
- **Frost** `#F4F6F8` — light ground and dark-mode text
- **Graphite plate** `#11151A` — dark engineered surface
- **Pale plate** `#E7EBEF` — light engineered surface

Signal blue is singular and functional. It should occupy less than five percent
of most compositions.

## Primary motifs

### Edge

A machined boundary, plate seam, or exact transition between systems. Edge is
directional and should imply tolerance, force, and controlled separation.

### Aperture

An instrument opening, inspection port, or calibrated lens. Aperture should feel
mechanical and exact, never like an eye, flower, or organic iris.

### Rack

A receding structural frame, equipment bay, or vault. Rack is the main reference
for large Hara heroes, including the benchmark page.

The original 4096px masters and responsive AVIF/WebP assets for all three motifs
are preserved. Do not replace them with biological reinterpretations.

## Static backgrounds

Every background is an adaptive SVG on a `4096 × 2304` design canvas. SVG is
resolution-independent, so the same source can be exported at 4K, 8K, print, or
smaller responsive sizes without losing sharpness.

| Asset | Material interpretation |
| --- | --- |
| `assets/backgrounds/evaluation-field.svg` | Armoured evaluation seam and calibrated execution point |
| `assets/backgrounds/ast-field.svg` | Routed syntax conduits inside a lancet frame |
| `assets/backgrounds/symbol-lattice.svg` | Machined gothic tracery and H-bracing |
| `assets/backgrounds/dataflow-orbit.svg` | Instrument aperture with linear data rails |
| `assets/backgrounds/kernel-depth.svg` | Receding rack vault and execution core |

The files use `prefers-color-scheme` internally, include accessible titles and
descriptions, and contain no embedded display text.

## Live effects

```astro
---
import Backdrop from "@hara-lang/visual-language/astro/Backdrop.astro";
import "@hara-lang/visual-language/theme.css";
import "@hara-lang/visual-language/effects.css";
---

<section class="hero">
  <Backdrop effect="kernel" intensity="quiet" />
  <div class="hero__content">
    <h1>Precision under load.</h1>
  </div>
</section>
```

Available effects are `evaluation`, `syntax`, `lattice`, `flow`, and `kernel`.
Intensity may be `quiet`, `balanced`, or `dense`.

Motion is **off by default**. Opt-in motion is limited to a small calibration
scan and stepped indicator change. No effect rotates, breathes, floats, or
scales. `prefers-reduced-motion` disables all opt-in animation.

For a meaningful illustration rather than a decorative field, provide a label:

```astro
<Backdrop
  effect="flow"
  label="Calibrated state passing through a Hara instrument aperture"
/>
```

## Composition rules

Use one primary material environment per viewport. Leave broad areas of
uninterrupted surface around headings and code. Align seams, rails, and vault
axes to the content grid. Use the `quiet` intensity behind reading material.

Rounded glass cards, bright gradient buttons, and decorative glows weaken the
system. Prefer exact borders, small radii, inset highlights, hard alignment, and
one active signal.

The intended character is **alien precision, grounded in material**.
