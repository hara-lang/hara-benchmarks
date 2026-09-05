# Hara v2 tool and workbench contract

The v2 tool layer extends the Hara document/product language with the denser
operational surfaces needed by 3D editors, node and material graphs, animation
timelines, consoles, REPLs, inspectors, and other long-lived workbenches.

It is not a second brand or a replacement for [`v2.css`](./V2-THEME.md).
`v2-tool.css` imports the document foundation, then adds tool material tokens,
control primitives, and a viewport-first workbench shell.

**Reference laboratory:**
[3D, node/material, and animation workbenches](https://hara-lang.github.io/visual-language/v2/tool/)

## Boundary

Use the tool layer when repeated manipulation, selection, inspection, and status
are the primary task. Use the document layer when reading, browsing, publishing,
comparison, or a conventional product workflow is primary.

| Surface | Entry point | Root class | Typical examples |
| --- | --- | --- | --- |
| Document/product | `v2.css` | `hara-v2` | WWW, Docs, Specs, Benchmarks, World |
| Tool/workbench | `v2-tool.css` | `hara-v2 hara-v2-tool` | 3D editor, node graph, timeline, console, REPL workbench |

A mixed page may remain a document shell and scope `hara-v2-tool` to an embedded
workbench. Do not apply tool chrome to prose merely to make it look technical.

This package owns visual geometry, theme, semantic roles, and state markers. It
does **not** implement a docking engine, drag-and-drop, graph manipulation,
roving-tab keyboard logic, focus traps, persistence, command dispatch, undo, or
product data. Applications or `@hara-lang/ui` own those behaviours.

## Import and composition

Import only `v2-tool.css`; it already imports `v2.css`.

```astro
---
import WorkbenchShell from "@hara-lang/visual-language/astro/v2/tool/WorkbenchShell.astro";
import Toolbar from "@hara-lang/visual-language/astro/v2/tool/Toolbar.astro";
import ToolGroup from "@hara-lang/visual-language/astro/v2/tool/ToolGroup.astro";
import ToolButton from "@hara-lang/visual-language/astro/v2/tool/ToolButton.astro";
import DockPanel from "@hara-lang/visual-language/astro/v2/tool/DockPanel.astro";
import PanelHeader from "@hara-lang/visual-language/astro/v2/tool/PanelHeader.astro";
import InspectorSection from "@hara-lang/visual-language/astro/v2/tool/InspectorSection.astro";
import ViewportOverlay from "@hara-lang/visual-language/astro/v2/tool/ViewportOverlay.astro";
import StatusBar from "@hara-lang/visual-language/astro/v2/tool/StatusBar.astro";
import "@hara-lang/visual-language/v2-tool.css";
---

<div class="hara-v2 hara-v2-tool">
  <WorkbenchShell label="Scene editor">
    <Toolbar slot="top" label="Scene commands" density="dense">
      <ToolGroup label="Transform">
        <ToolButton label="Move" active />
        <ToolButton label="Rotate" />
      </ToolGroup>
    </Toolbar>

    <main slot="viewport">...</main>

    <DockPanel slot="right" label="Object inspector">
      <PanelHeader title="Command aperture" eyebrow="Object" />
      <InspectorSection title="Transform">...</InspectorSection>
    </DockPanel>

    <div slot="overlay">
      <ViewportOverlay placement="top-left">Perspective · 1 m</ViewportOverlay>
    </div>

    <StatusBar slot="status">Ready</StatusBar>
  </WorkbenchShell>
</div>
```

## Identity invariants

The tool layer inherits every invariant in [`V2-THEME.md`](./V2-THEME.md):

- the current block H and single signal dot;
- the existing heading family;
- one primary blue signal, with orange, green, and red reserved for state;
- equal light and dark products;
- original technical linework rather than franchise imitation;
- contrast, information density, and legibility before decoration.

Tool surfaces may be raised or recessed when this communicates control
hierarchy, selection, docking, or data entry. They must not become thick
skeuomorphic hardware or ornamental science-fiction panels.

## Token contract

### Dimensions and motion

| Token | Purpose |
| --- | --- |
| `--hara-tool-control` | Regular control height |
| `--hara-tool-control-dense` | Dense repeated-control height |
| `--hara-tool-toolbar` | Toolbar minimum height |
| `--hara-tool-rail` | Icon rail width or horizontal height |
| `--hara-tool-status` | Status bar minimum height |
| `--hara-tool-cut`, `--hara-tool-cut-small` | Clipped surface geometry |
| `--hara-tool-gap`, `--hara-tool-gap-dense` | Regular and dense grouping gaps |
| `--hara-tool-motion` | Short state-transition duration |

### Material and state

| Token | Purpose |
| --- | --- |
| `--hara-tool-bg` | Neutral tool surface |
| `--hara-tool-bg-raised` | Command rails, headers, and raised controls |
| `--hara-tool-bg-recessed` | Viewports, fields, selected/pressed wells |
| `--hara-tool-edge`, `--hara-tool-edge-strong` | Seams and structural frames |
| `--hara-tool-glint` | Restrained top-edge light |
| `--hara-tool-shadow`, `--hara-tool-shadow-inset` | Floating and inset hierarchy |
| `--hara-tool-highlight` | Selected/pressed wash |
| `--hara-tool-noise` | Quiet material grain |
| `--hara-tool-signal` | Selection and primary operational state |
| `--hara-tool-warning`, `--hara-tool-danger`, `--hara-tool-success` | Functional state only |
| `--hara-tool-ink`, `--hara-tool-muted` | Tool text hierarchy |

Both explicit themes and system dark mode define the complete material contract.
Do not hard-code a theme-specific surface colour in downstream editor chrome.

## Class-level surfaces

Framework-free consumers may compose the material layer directly:

- `.hara-tool-surface` — neutral framed tool surface;
- `.hara-tool-surface--raised` — floating or command hierarchy;
- `.hara-tool-surface--recessed` — data entry or working well;
- `.hara-tool-surface--framed` — stronger structural containment;
- `.hara-tool-surface--cut` and `--cut-small` — shared clipped geometry;
- `.hara-tool-seam` — explicit section boundary.

Use `data-state="selected"`, `warning`, or `danger`, `aria-selected="true"`, or
`aria-invalid="true"` when those states are semantic. Never add a state colour
only for decoration.

## Component inventory

### Controls

| Component | Semantic purpose |
| --- | --- |
| `Toolbar` | Labelled horizontal or vertical command collection; supports regular/dense and sticky states |
| `ToolGroup` | Related command grouping with horizontal/vertical separation |
| `ToolButton` | Momentary command, active marker, command hint, icon-only labelling, disabled state |
| `ToolToggle` | Boolean command with `aria-pressed` |
| `ToolSelect` | Labelled compact selection field |
| `ToolNumberField` | Labelled numeric input with bounds, step, and optional unit |
| `TabStrip` | Labelled horizontal/vertical `tablist` with selected and disabled tabs |
| `IconRail` | Labelled vertical or horizontal navigation/tool rail |
| `StatusBar` | Primary and secondary status regions; optional polite live status |

### Workbench structure

| Component | Semantic purpose |
| --- | --- |
| `WorkbenchShell` | Top, left, viewport, right, bottom, overlay, and status slots |
| `DockPanel` | Left, right, bottom, or floating panel with size, selected, and collapsed markers |
| `FloatingPalette` | Non-modal labelled palette/dialog surface |
| `ViewportOverlay` | Readable telemetry or interactive control over scene content |
| `InspectorSection` | Native open/collapsed property group using `details`/`summary` |
| `PanelHeader` | Compact title, eyebrow, metadata, and action header |

All components are stateless Astro primitives. Props render initial semantic
state. A product that changes state after load must supply client-side behaviour
and keep the relevant ARIA attributes synchronized.

## Workbench slots

`WorkbenchShell` exposes these named regions:

1. `top` — command toolbar and optional tab strip;
2. `left` — icon rail, outliner, catalogue, or navigator;
3. `viewport` — the primary graph, scene, canvas, terminal, or editor surface;
4. `right` — inspector or property dock;
5. `bottom` — timeline, assets, console, logs, or secondary editor;
6. `overlay` — viewport telemetry and floating palettes;
7. `status` — persistent operational status.

The default slot may stand in for `viewport`. Preserve this source order so
responsive collapse does not change the reading or keyboard order.

## Composition patterns

### 3D or spatial editor

Use a top `Toolbar`, a left `IconRail` plus outliner `DockPanel`, a quiet
viewport, a right property inspector, a bottom asset shelf, sparse
`ViewportOverlay` telemetry, and `StatusBar`. Geometry and scene art belong to
the application; do not bake them into shared chrome.

### Node or material editor

Use a compact toolbar and `TabStrip`, a left node catalogue, graph viewport,
right property dock, bottom material assets, and an optional `FloatingPalette`
for add/search commands. Node colour should identify semantic domains or state,
not decorate every node.

### Scene or animation editor

Use transport controls in the top toolbar, a rig hierarchy, pose viewport,
right animation inspector, bottom timeline, and status/receipt telemetry. The
bottom dock uses the same panel grammar as every other workbench region.

### Console or REPL workbench

Use the viewport for terminal/editor output, a right inspector for session or
capability state, a bottom log/history dock where needed, and `StatusBar` for
backend, generation, source revision, cancellation, or receipt state. Preserve
monospace output contrast independently of surrounding theme.

## Responsive contract

The viewport remains the primary surface. Shared CSS collapses secondary regions
in this order:

1. below `1120px`, hide the right inspector dock;
2. below `820px`, hide the left dock and reduce the shell to top, viewport,
   bottom, and status;
3. below `640px`, hide the bottom dock and preserve top, viewport, and status;
4. at narrow widths, toolbars scroll horizontally rather than wrapping commands
   into ambiguous rows;
5. floating palettes become bottom sheets within the workbench bounds.

Applications must provide explicit commands to reveal collapsed content where
it remains necessary. Do not rely on hover-only disclosure.

## Accessibility contract

- Every toolbar, rail, panel, overlay, and workbench must have a useful label.
- `ToolButton` and `ToolToggle` require a text `label`; icon-only mode exposes it
  through `aria-label` and visually hides the duplicate text.
- Keep `aria-pressed`, `aria-selected`, `aria-invalid`, `disabled`, and active
  data markers synchronized with product state.
- `TabStrip` supplies tab semantics but not keyboard movement or panel
  activation. The consuming application implements the complete tab pattern.
- `FloatingPalette` is non-modal and does not trap focus. The application owns
  focus placement, dismissal, and restoration.
- Use `StatusBar live` only for concise changes that should be announced; do not
  stream high-frequency telemetry through a live region.
- Visible `focus-visible` outlines are part of the contract and must not be
  removed.
- State must remain understandable without colour alone.
- Motion transitions run only when reduced motion is not requested.
- Viewport overlays must remain legible over both light and dark scene content.

## Light and dark parity

Review every workbench in explicit light, explicit dark, and system modes.
Selection, pressed state, focus, disabled state, warning, danger, and data-entry
recession must retain the same hierarchy. Light mode is pale machined steel and
paper; dark mode is graphite and recessed black, not an inversion filter.

## Migration from document-only v2

Existing `v2.css` consumers require no changes. Adopt the tool layer only where
the primary task is editor-like manipulation:

1. keep `v2.css` on existing WWW, Docs, Specs, Benchmarks, World, and product
   shells;
2. import `v2-tool.css` instead of importing both entry points in a workbench,
   because the tool entry already includes the document foundation;
3. add `hara-v2-tool` beside `hara-v2` at the workbench root;
4. replace local toolbar, field, dock, inspector, overlay, and status chrome
   incrementally with shared primitives;
5. retain existing application behaviour and wire it to the rendered ARIA and
   data-state contract;
6. remove local visual tokens only after both themes, focus, disabled, and
   responsive collapse states match the shared contract.

No application should migrate a prose or editorial surface to the tool layer
solely for visual consistency. Mixed pages may scope the tool root to one
embedded REPL, graph, timeline, or editor.

## Release note

This is an additive v2 capability release. It introduces `v2-tool.css`, fifteen
stateless Astro primitives, framework-free material classes, and the `/v2/tool/`
reference laboratory. Existing v1 imports and existing `v2.css` document-shell
imports remain valid and unchanged. No docking engine, editor runtime, or
product behaviour is added to this package.

## Adoption checklist

- [ ] Import `v2-tool.css` once and apply `hara-v2 hara-v2-tool` at the intended root.
- [ ] Use shared components or class primitives instead of local toolbar/dock chrome.
- [ ] Keep identity and state colours inherited from the package.
- [ ] Supply accessible labels for every icon-only or structural surface.
- [ ] Implement dynamic keyboard and focus behaviour in the application layer.
- [ ] Verify the `1120px`, `820px`, and `640px` collapse states.
- [ ] Verify explicit light, explicit dark, system theme, focus, disabled, and reduced-motion states.
- [ ] Keep prose and editorial content on the document surface language.
- [ ] Record any product-specific extension rather than silently forking shared tokens.

See [`README.md`](./README.md) for package imports,
[`V2-THEME.md`](./V2-THEME.md) for the shared document and identity foundation,
and the [v2 catalogue guide and live route review matrix](https://hara-lang.github.io/visual-language/v2/guide/)
with [`V2-GUIDE.md`](./V2-GUIDE.md) for exact route, theme, viewport, state,
keyboard, overflow, reduced-motion and adoption review.
