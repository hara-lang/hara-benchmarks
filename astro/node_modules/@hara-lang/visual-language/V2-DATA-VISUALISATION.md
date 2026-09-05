# Hara visual language v2 — data visualisation and evidence graphics

## Status

The reference guide lives at `/v2/data/`. The additive public stylesheet is exported as `@hara-lang/visual-language/v2-data.css`.

The guide uses deterministic benchmark, package-compatibility and runtime fixtures. They are not current performance, support or production telemetry claims.

## Purpose

Hara products need one evidence grammar for charts, matrices, distributions, timelines and operational telemetry. The grammar must make uncertainty and evidence boundaries easier to inspect, not merely make data look technical.

## Non-negotiable rules

1. Name the metric, unit, direction and baseline next to the graphic.
2. Keep exact source, methodology, environment and revision references visible.
3. Use position and length before area, volume or decorative perspective.
4. Pair colour with words, symbols, patterns or structural placement.
5. Keep confidence, ranges and sample counts visible with point estimates.
6. Render missing, stale, partial, unsupported and incomparable as different facts.
7. Provide an accessible table or ordered textual alternative for every evidence graphic.
8. Let products own data and methodology; the package owns presentation grammar only.

## Reference composition 1 — benchmark evidence

A benchmark comparison includes:

- workload and metric identity;
- unit and whether lower or higher is better;
- visible baseline and full scale domain;
- measured point;
- confidence or range;
- sample count;
- exact run/evidence reference;
- environment and methodology;
- explicit incomparable state where boundaries differ;
- accessible data table.

Small multiples keep one scale per workload visible and must not imply cross-panel comparability when domains differ. Distribution views retain ranges and counts rather than reducing every result to one median.

Decorative 3D bars, perspective projection and unlabeled truncated baselines are excluded.

## Reference composition 2 — package compatibility

A compatibility cell contains a state symbol, state word, target, exact package/release revision and evidence text.

The supported state is not the default absence state. These meanings remain separate:

- **supported** — exact implementation evidence supports the declared release;
- **partial** — only a named subset is supported;
- **unsupported** — the target cannot provide the required capability;
- **missing** — expected evidence has not been received;
- **incomparable** — the target or method does not share an equivalent boundary.

At narrow widths the matrix yields to textual package cards. It does not squeeze cells until their evidence becomes unreadable.

## Reference composition 3 — runtime telemetry

Runtime telemetry uses one fenced envelope:

```text
session
+ generation
+ source revision
+ backend
+ capability revision
+ monotonic event sequence
+ timestamp or offset
+ state word
+ observation detail
```

The sequence is primary. High-frequency telemetry is not streamed through an assertive live region. Products may announce concise lifecycle transitions separately.

Stale, partial and unsupported observations remain visible and are never converted to zero.

## Evidence-state grammar

### Missing

The expected value was not received. Show the absent fact and the source boundary that should have supplied it.

### Stale

A value exists but is older than the declared freshness window. Show its timestamp and the threshold.

### Partial

Only a named subset is available. State the numerator, denominator or missing dimensions.

### Unsupported

The implementation or target cannot produce the measurement. Do not render this as zero or failure.

### Incomparable

The values do not share equivalent units, boundaries or methodology. Do not force them onto one competitive scale.

## Accessibility contract

- Every graphic has a useful heading and readable summary.
- Meaning is available without colour.
- Bar values, states and confidence ranges appear in text.
- Tables use captions, column headers and row headers.
- Scrollable tables are keyboard reachable and labelled.
- Small text remains supporting metadata rather than the only carrier of meaning.
- Narrow views preserve the primary evidence and move secondary detail below it.
- Reduced motion removes transitions and animated updates without removing state feedback.
- Zoom and reflow must not create document-level horizontal overflow; dense tables and timelines scroll locally.

## Theme contract

Light and dark modes use the same scale, hierarchy, symbols and state words. Dark mode does not compensate for weak hierarchy by adding more grid lines. Light mode is not an inverted chart screenshot.

## Ownership boundary

### Visual Language owns

- evidence layout and surface grammar;
- scale, axis and legend presentation;
- confidence/range presentation;
- evidence-state symbols and words;
- accessible table and textual alternatives;
- responsive containment and reduced-motion treatment.

### Benchmarks owns

- workloads, measurements, baselines, units and exclusions;
- confidence method and sample policy;
- environments, raw evidence and methodology revisions.

### Package registry owns

- coordinates and release identity;
- target support and compatibility claims;
- deprecation, withdrawal, revocation and publication receipts.

### Runtime owns

- session, generation, source revision and backend;
- capabilities, observations, timestamps, event sequence and receipts.

## Adoption

Downstream products import the stylesheet and bind the grammar to authoritative data:

```css
@import "@hara-lang/visual-language/v2-data.css";
```

They must not copy the guide fixtures or present them as current product data. Adoption PRs should pin a merged Visual Language revision and include exact light/dark, keyboard, 320-pixel, missing-state and accessible-table evidence.

## Verification

The package retains tests for:

- active catalogue route and static page;
- deterministic fixture identities and revisions;
- visible units, baseline, confidence and evidence references;
- distinct missing, stale, partial, unsupported and incomparable states;
- benchmark, package and runtime ownership boundaries;
- accessible tables and textual alternatives;
- no decorative perspective or protected-token redefinition;
- light/dark token consumption, narrow widths and reduced motion;
- repository-wide `npm test` and `npm run site:build`.
