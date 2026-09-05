# Hara v2 environment widget contract

The environment widgets are stateless Astro compositions for embedded live
coding, project studios, graphical previews, REPLs, and other surfaces that need
to move between several related views without becoming a wall of panels.

They extend the [`v2-tool.css`](./V2-TOOL.md) workbench layer. They do not change
any Hara site, product, runtime, or application state by themselves.

**Reference specimen:**
[Live environment workbench](https://hara-lang.github.io/visual-language/v2/tool/#environment)

## Purpose

A Hara environment commonly needs two orthogonal navigation systems:

1. **content sections** describing what the main surface shows;
2. **capability groups** describing the attached runtime and providers.

The standard content series is:

- **Nav** — project, document, lesson, or local environment navigation;
- **Frontmatter** — repository, revision, session, filesystem, runtime, and
  publication facts;
- **Graphics** — canvas, graph, scene, preview, or other visual output;
- **Code** — editor, source, structural selection, and evaluation results.

The standard capability series is:

- **Sessions** — current and related evaluator sessions;
- **Files** — logical files, resources, and active source;
- **Canvas** — 2D viewport and execution controls;
- **3D** — camera, scene, renderer, and spatial-provider controls.

Applications omit sections and capability groups they do not support. The
visual language must never imply a provider exists merely to make a specimen
look complete.

## Components

| Component | Purpose |
| --- | --- |
| `SectionNavigator` | Renders a labelled section tablist with stable values, panel relationships, badges, density, selected, and disabled state. |
| `EnvironmentSection` | Renders one labelled `tabpanel` with explicit section, kind, scrolling, active, and hidden markers. |
| `FrontmatterGrid` | Renders compact definition-list facts with optional detail, links, code typography, and semantic state. |
| `ResourceList` | Renders sessions, files, or other resources as static rows, links, or application-wired actions. |
| `CapabilityPane` | Composes only the Sessions, Files, Canvas, and 3D slots supplied by the host into a docked tabbed pane. |
| `EnvironmentWorkbench` | Composes the section navigator, main section panels, optional capability pane, commands, overlay, bottom region, and status inside `WorkbenchShell`. |

`TabStrip` also accepts optional `controls`, `value`, `badge`, `description`, and
`variant` fields. Existing tab consumers remain valid.

## Import

```astro
---
import EnvironmentWorkbench from "@hara-lang/visual-language/astro/v2/tool/EnvironmentWorkbench.astro";
import FrontmatterGrid from "@hara-lang/visual-language/astro/v2/tool/FrontmatterGrid.astro";
import ResourceList from "@hara-lang/visual-language/astro/v2/tool/ResourceList.astro";
import InspectorSection from "@hara-lang/visual-language/astro/v2/tool/InspectorSection.astro";
import ToolToggle from "@hara-lang/visual-language/astro/v2/tool/ToolToggle.astro";
import StatusBar from "@hara-lang/visual-language/astro/v2/tool/StatusBar.astro";
import "@hara-lang/visual-language/v2-tool.css";
---

<div class="hara-v2 hara-v2-tool">
  <EnvironmentWorkbench
    label="Tutorial environment"
    idPrefix="tutorial-environment"
    activeSection="code"
    activeControlGroup="sessions"
  >
    <nav slot="nav">...</nav>

    <FrontmatterGrid
      slot="frontmatter"
      entries={[
        { label: "Scope", value: "isolated", status: "current" },
        { label: "Session", value: "tutorial-01", code: true },
        { label: "Filesystem", value: "memory:tutorial-01", code: true }
      ]}
    />

    <canvas slot="graphics"></canvas>
    <div slot="code">...</div>

    <ResourceList
      slot="sessions"
      items={[{ id: "tutorial-01", label: "Tutorial", status: "ready", current: true }]}
    />

    <ResourceList
      slot="files"
      items={[{ id: "main", label: "main.hal", current: true, action: true }]}
    />

    <InspectorSection slot="canvas" title="Viewport">
      <ToolToggle label="Grid" pressed />
    </InspectorSection>

    <StatusBar slot="status">Kernel connected</StatusBar>
  </EnvironmentWorkbench>
</div>
```

## Slots

`EnvironmentWorkbench` exposes:

1. `nav`;
2. `frontmatter`;
3. `graphics`;
4. `code`, with the default slot accepted as a code fallback;
5. `commands` beside the section navigator;
6. `sessions`;
7. `files`;
8. `canvas`;
9. `threeD`;
10. `controlActions` in the capability-pane header;
11. `bottom`;
12. `overlay`;
13. `status`.

Only supplied section and capability slots are rendered. The initial active
section and capability group fall back to the first available item when the
requested item is absent.

## State and behaviour boundary

The package owns:

- visual geometry and material hierarchy;
- initial `role="tablist"`, `role="tab"`, and `role="tabpanel"` semantics;
- `aria-selected`, `aria-controls`, `aria-labelledby`, `hidden`, `tabindex`,
  `aria-current`, `disabled`, and semantic data markers;
- light, dark, focus, disabled, selected, current, warning, danger, and reduced
  motion presentation;
- responsive collapse of the secondary capability pane through the shared
  workbench contract.

The application or `@hara-lang/ui` owns:

- arrow-key movement and activation;
- synchronizing selected tabs and hidden panels;
- focus placement and restoration;
- opening a collapsed capability pane;
- persistence of the active section or group;
- session and file selection;
- canvas and 3D command dispatch;
- evaluation, cancellation, reset, resize, and runtime lifecycle;
- provider capability discovery and live data.

No script is shipped with these widgets. A downstream controller should bind by
`data-value`, `data-section`, `data-resource-id`, and the stable IDs supplied by
`idPrefix`, then keep the rendered ARIA contract synchronized.

## Responsive behaviour

- Section tabs remain horizontally scrollable instead of wrapping into an
  ambiguous second row.
- The capability pane follows the existing workbench rule and is removed from
  the primary grid below `1120px`.
- At narrow widths, frontmatter moves from an automatic grid to two columns and
  then one column.
- Resource metadata yields before resource identity.
- Graphics and code remain the primary working surface.
- Reduced-motion mode removes widget transitions.

Applications must expose an explicit command when hidden or collapsed
capabilities remain necessary on smaller screens.

## Adoption sequence

1. Build and review the environment in the visual-language laboratory.
2. Attach application behaviour without changing the shared CSS or component
   markup.
3. Verify only supported sections and capability groups are present.
4. Verify explicit light, explicit dark, system theme, keyboard focus,
   disabled, selected, current, warning, danger, and reduced-motion states.
5. Replace local product chrome only after the shared contract matches the
   product behaviour.
6. Roll out to sites and products in separate downstream pull requests.

This order keeps the interface language upstream and prevents each Hara surface
from inventing its own navigation, frontmatter, and runtime-control grammar.
