# Hara interface language v2

Version 2 is the opt-in document and product interface layer for Hara's public
sites and content-heavy applications. It keeps the existing identity and theme
machinery while moving the spatial language away from both generic cards and
hard editor chrome toward calm, continuous command surfaces.

For toolbars, docks, inspectors, palettes, viewports, timelines, consoles, and
editor workbenches, use the additive [`V2-TOOL.md`](./V2-TOOL.md) contract.
`v2-tool.css` imports this document layer rather than creating a separate theme.

The reference mood is a precision instrument drawn through an illustrator's
technical notebook: continuous matte fields, quiet seams, sparse telemetry, and
slightly imperfect construction lines. It must remain recognisably Hara rather
than reproduce any franchise symbol, ship, type treatment, or control panel.

## Identity invariants

- Keep the current `HaraMark`: the block H and its single signal-colour dot.
- Keep the current heading family. `--hara-v2-font-heading` aliases
  `--hara-font-sans`; v2 changes hierarchy and spacing, not the wordmark.
- Use one primary blue signal. Orange, green, and red are state colours, not
  decoration.
- Light and dark modes are equal products. Light mode is pale steel and paper,
  not a washed-out dark mode.
- Structure comes from alignment, tonal layers, and one-pixel seams. Repeated
  controls and panels use restrained radii; clipped or chamfered geometry is
  reserved for rare identity and hero moments.
- Shadows are ambient only. Document controls do not imitate thick hardware,
  and no surface should combine a strong seam, bevel, chamfer, and state wash
  when one cue would communicate the hierarchy.
- Hand-drawn character is a quiet second line, grid drift, and original
  technical illustration. It must never reduce text contrast or data density.
- The tool extension may add raised and recessed operational surfaces, but it
  may not replace this identity, typography, state, or theme contract.

## Public contract

Import the document layer and place `hara-v2` at the interface root. The
exported Astro `Shell` already adds the class.

```astro
---
import Shell from "@hara-lang/visual-language/astro/v2/Shell.astro";
import Header from "@hara-lang/visual-language/astro/v2/Header.astro";
import "@hara-lang/visual-language/v2.css";
---

<Shell sidebar={false}>
  <Header slot="header" section="Specs" nav={ecosystemNav} />
  <section class="hara-v2-panel">...</section>
</Shell>
```

The document component contract is deliberately small:

- `Shell` owns header, context, rail, main, inspector, and footer slots.
- `Header` owns the persistent Hara identity and ecosystem navigation.
- `ContextNav` owns product-local navigation and command actions.
- `Sidebar` owns grouped, count-aware navigation.
- `PageHeader` owns page title, actions, metadata, and optional illustration.
- `FleetField` is an original monochrome command-deck illustration that follows
  the current theme through `currentColor` and the Hara signal token.

Everything else is a class-level primitive in `v2.css`. This lets Starlight,
Astro pages, and framework-free surfaces use the same geometry without forcing
one component model on every repository.

The calm-surface refinement is part of the public entry point. It softens the
original command-surface pass across headers, context rows, side rails, buttons,
fields, panels, tabs, tables, matrices, feeds, profiles, callouts, and code
frames. It intentionally does not import `--hara-tool-*` tokens: prose and
editorial reading surfaces remain calm.

## Surface rhythm

The governing principle is **precision without armour**.

- Use one primary separation cue per boundary: spacing, tone, or a seam.
- Prefer sentence case and natural letter spacing for repeated operational
  labels; reserve uppercase monospace labels for metadata and compact status.
- Repeated controls should be comfortable enough for long sessions. V2 uses
  34px regular tool controls and 30px dense controls rather than forcing every
  action into the smallest possible frame.
- Common panels and controls use restrained 6–12px radii. Large chamfers remain
  available as identity accents but are not the default component shape.
- Hover and selection changes should settle over roughly 180–190ms with reduced
  motion support. Do not animate geometry merely for atmosphere.
- Light/dark parity includes rhythm and contrast, not only token completeness.
  Dark mode must not compensate for weak hierarchy by increasing every edge.

## Choosing the document or tool layer

Use `v2.css` when the primary task is reading, browsing, publishing, comparing,
or completing a conventional product workflow. Use `v2-tool.css` when the
primary task is repeatedly manipulating a viewport, graph, timeline, console,
or dense property model. A Docs page with one embedded REPL can keep the page on
`v2.css` and scope `hara-v2-tool` to the embedded workbench.

Do not turn document cards into editor panels merely to make them feel more
technical. Command hierarchy should follow task frequency and state, not act as
decoration.

## Layout families

### WWW

The public site uses a broad single-column shell: ecosystem header, large page
header, proof strip, three-column capability decks, executable code surface,
and a restrained closing command. There is no permanent rail. Illustration may
occupy half of the hero, but product copy remains the first reading order.

### Docs

Documentation uses the full information shell: ecosystem header, product
context row, grouped left rail, prose main column, and a quiet right outline.
Search, version selection, REPL controls, and canvas state are command controls,
not rounded marketing pills. Code remains dark in both themes so syntax and
selection behaviour stay stable.

### Specs

Specifications use an application shell: ecosystem header, local workflow tabs,
registry or form main area, and a validation inspector. Tables, status badges,
publication checks, and digest values use compact rows and monospace labels.
The inspector disappears first as the viewport narrows.

### Benchmarks

Benchmark evidence uses a dense command board: evidence header, dataset tabs,
metric strip, comparison matrix, and selected-cell inspector. The visual signal
must indicate selection or a measured win, never simply add colour. Method and
raw-data links remain adjacent to the result they qualify.

### World

World uses an editorial command shell: ecosystem header, community section row,
optional feed filters, story stream, and right-side lesson/community modules.
Profiles and agents share one card grammar. Posting is the clear command action,
while reading surfaces keep the paper-like lightness of the theme.

## Responsive order

1. Remove the inspector below `1120px`.
2. Collapse the rail below `820px`; products provide a drawer trigger in the
   header or context row.
3. Preserve horizontal context navigation as a scrollable row.
4. Stack illustrated page headers and data cards below `820px`.
5. At phone widths, keep controls at least 34px high and make primary page
   actions full-width.

The tool extension has its own viewport-first collapse order in
[`V2-TOOL.md`](./V2-TOOL.md#responsive-contract).

## Accessibility contract

- Preserve visible keyboard focus and never encode selection by colour alone.
- Maintain source order when rails or inspectors collapse.
- Give icon-only controls accessible names.
- Keep state colours functional and contrast-safe in both themes.
- Respect reduced motion and do not require animation to understand state.
- Treat scrollable context rows, tables, matrices, and code surfaces as keyboard
  reachable content rather than hidden overflow.

## Adoption sequence

1. Import the opt-in package contract without changing v1 tokens or motifs.
2. Move `hara-www` onto the header, page-header, proof, card, and code primitives.
3. Map Starlight variables and documentation rails to v2 without changing REPL
   behaviour.
4. Move Specs and Benchmarks, which exercise tables, tabs, badges, and inspectors.
5. Move World after feed, profile, form, and account states are covered.
6. Adopt `v2-tool.css` only for embedded or full workbenches that meet the
   separate tool contract.
7. Promote v2 from experimental only after screenshots, keyboard navigation,
   reduced-motion behaviour, and both themes are verified across all families.

See the [five-layout document laboratory](https://hara-lang.github.io/visual-language/v2/)
and the [tool workbench laboratory](https://hara-lang.github.io/visual-language/v2/tool/)
for the executable reference compositions.

Use the [v2 catalogue guide and live route review matrix](https://hara-lang.github.io/visual-language/v2/guide/)
with [`V2-GUIDE.md`](./V2-GUIDE.md) for the exact route inventory, two-theme and
five-viewport review procedure, navigation ownership, lifecycle, screenshot
evidence contract, and downstream adoption boundaries.
