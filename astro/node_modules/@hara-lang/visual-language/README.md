# @hara-lang/visual-language

Hara's shared precision-material design system. It contains brand tokens,
cross-domain light/dark theme handling, responsive motifs, maximum-resolution
vector backgrounds, restrained field effects, document/product shells, and an
opt-in tool/workbench chrome for Astro and framework-free surfaces.

This package owns the **visual and semantic contract**. Product state, docking
engines, graph manipulation, drag-and-drop, command dispatch, and other
behaviour-rich editor systems remain application concerns or belong in
`@hara-lang/ui`.

**[View the published visual language laboratory](https://hara-lang.github.io/visual-language/)**

Consumers should pin a release tag exactly:

```json
"@hara-lang/visual-language": "github:hara-lang/visual-language#v1.0.0"
```

Import `theme.css`, `motifs.css`, and `theme.js` before using the existing Astro
components. Edge, Aperture, and Rack use the original restored 4096px masters
and responsive AVIF/WebP delivery assets. Rack is the material reference used by
the Hara benchmarks hero. Run `npm run assets:build` after a master changes.

The Hara material field system adds five adaptive SVG backgrounds on a
`4096 × 2304` canvas and five reusable effects. It uses frost, graphite,
brushed-metal structure, gothic vault geometry, and one functional blue signal;
there are no decorative multi-colour fields. Import it with:

```astro
---
import Backdrop from "@hara-lang/visual-language/astro/Backdrop.astro";
import "@hara-lang/visual-language/theme.css";
import "@hara-lang/visual-language/effects.css";
---

<section class="hero">
  <Backdrop effect="kernel" intensity="quiet" />
  <h1>Precision under load.</h1>
</section>
```

Motion is off by default. See [`HARA-IMAGERY.md`](./HARA-IMAGERY.md) for the
complete material, motion, accessibility, and composition rules.

## Experimental interface language v2

V2 has two related entry points. Both preserve the current block-H mark, signal
dot, theme storage, and heading family. Both now follow a calm-surface rule:
**precision without armour**. Common controls use quieter seams, restrained
rounding, sentence-case labels, and smooth state transitions; chamfers and
strong material effects are reserved for rare identity moments.

**[Open the v2 catalogue guide and live review matrix](https://hara-lang.github.io/visual-language/v2/guide/)**

The guide documents the route manifest, global versus product-local navigation,
shared versus product-owned boundaries, route lifecycle, screenshot and
accessibility review procedure, and downstream adoption map. See
[`V2-GUIDE.md`](./V2-GUIDE.md) for the written contract.

| Entry point | Use it for | Contract |
| --- | --- | --- |
| `v2.css` | WWW, Docs, Specs, Benchmarks, World, data products, and content-heavy application shells | [`V2-THEME.md`](./V2-THEME.md) |
| `v2-tool.css` | Toolbars, docks, inspectors, palettes, viewports, timelines, consoles, editor workbenches, and compact browser-runtime chrome | [`V2-TOOL.md`](./V2-TOOL.md), [`V2-RUNTIME.md`](./V2-RUNTIME.md) |

`v2-tool.css` imports `v2.css`, so a workbench consumer imports only the tool
entry point and places both `hara-v2` and `hara-v2-tool` on its interface root.
The two layers deliberately share identity, state colours, typography, and
responsive priorities. The tool layer adds denser controls and structural
regions without making every surface visually heavier.

### Document and product shells

**[Open the five-layout v2 laboratory](https://hara-lang.github.io/visual-language/v2/)**

```astro
---
import Shell from "@hara-lang/visual-language/astro/v2/Shell.astro";
import Header from "@hara-lang/visual-language/astro/v2/Header.astro";
import ContextNav from "@hara-lang/visual-language/astro/v2/ContextNav.astro";
import "@hara-lang/visual-language/v2.css";
---

<Shell sidebar={false}>
  <Header slot="header" section="Specs" nav={ecosystemNav} />
  <ContextNav slot="context" items={workflowNav} />
  <section class="hara-v2-panel">...</section>
</Shell>
```

The document contract is intentionally additive: v1 tokens and motifs are
unchanged, so sites can migrate layout family by layout family. See
[`V2-THEME.md`](./V2-THEME.md) for identity invariants, surface rhythm, site
anatomy, responsive behaviour, and adoption order.

### Tool, editor, live-environment, and browser-runtime workbenches

**[Open the environment, 3D, node, and animation workbench laboratory](https://hara-lang.github.io/visual-language/v2/tool/)**

```astro
---
import WorkbenchShell from "@hara-lang/visual-language/astro/v2/tool/WorkbenchShell.astro";
import Toolbar from "@hara-lang/visual-language/astro/v2/tool/Toolbar.astro";
import ToolGroup from "@hara-lang/visual-language/astro/v2/tool/ToolGroup.astro";
import ToolButton from "@hara-lang/visual-language/astro/v2/tool/ToolButton.astro";
import DockPanel from "@hara-lang/visual-language/astro/v2/tool/DockPanel.astro";
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
    <DockPanel slot="right" label="Inspector">...</DockPanel>
    <StatusBar slot="status">Ready</StatusBar>
  </WorkbenchShell>
</div>
```

The package exports twenty-six stateless Astro primitives and composites:

- controls: `Toolbar`, `ToolGroup`, `ToolButton`, `ToolToggle`, `ToolSelect`,
  `ToolNumberField`, `TabStrip`, `IconRail`, and `StatusBar`;
- structure: `WorkbenchShell`, `DockPanel`, `FloatingPalette`,
  `ViewportOverlay`, `InspectorSection`, and `PanelHeader`;
- environment: `SectionNavigator`, `EnvironmentSection`, `FrontmatterGrid`,
  `ResourceList`, `CapabilityPane`, and `EnvironmentWorkbench`;
- browser runtime: `StatusLamp`, `RuntimeSwitch`, `ConnectionRow`,
  `CompactRuntimeShell`, and `RuntimeAppShell`.

The environment layer supplies the standard **Nav / Frontmatter / Graphics /
Code** content series and capability-aware **Sessions / Files / Canvas / 3D**
control pane. Only slots supplied by the host are rendered. See
[`V2-ENVIRONMENT.md`](./V2-ENVIRONMENT.md) for the complete composition, slot,
state, responsive, and adoption contract.

The browser-runtime layer separates requested switch state from actual runtime
state and adds compact popup and application-shell geometry for extension
toolbars, REPL hosts, diagnostics, and site-specific browser tools. It contains
no browser APIs or product behaviour. See [`V2-RUNTIME.md`](./V2-RUNTIME.md).

All v2 tool components provide geometry, theme, semantic roles, and initial
state markers. Applications still own event handling, focus movement,
persistence, drag/dock behaviour, command execution, provider discovery, and
domain data. See [`V2-TOOL.md`](./V2-TOOL.md) for the complete token reference,
component inventory, composition patterns, accessibility requirements, and
responsive collapse order.

The shared Open Graph system adds six `3840 × 2016` material masters and twelve
site-specific cards with deterministic typography. See
[`OG-IMAGERY.md`](./OG-IMAGERY.md) and rebuild them with `npm run assets:og`.

The theme script stores `system`, `light`, or `dark` in the `hara-theme` cookie
on `hara-lang.org` and uses local storage on local hosts.
