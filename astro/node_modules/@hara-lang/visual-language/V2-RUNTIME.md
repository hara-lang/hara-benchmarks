# Hara v2 browser-runtime chrome contract

The browser-runtime family extends the Hara v2 tool layer with the compact,
state-heavy surfaces used by browser extensions, runtime connection menus,
DevTools hosts, REPL shells, and site-specific browser applications.

It is part of `v2-tool.css`; consumers do not import a third theme entry point.

## Purpose and boundary

Browser runtime surfaces have a distinctive constraint: a switch records what a
person requested, while a lamp and status label report what actually happened.
The visual contract must never present a requested connection as a successful
connection.

The package owns:

- compact geometry and material hierarchy;
- initial switch, status, output, navigation, region, and alert semantics;
- visible requested and actual state;
- light, dark, focus, disabled, transition, warning, danger, and reduced-motion
  presentation;
- responsive collapse for compact popups and runtime workbenches.

The consuming extension or application owns:

- Chrome APIs and Manifest V3 lifecycle;
- exact-tab authority;
- runtime, RESP, DOM, diagnostics, download, ChatGPT, and Tripo state;
- storage, reconnect, shutdown, command dispatch, and error recovery;
- all event handlers and synchronization of ARIA and data markers.

No script, evaluator, message transport, content script, or browser authority is
shipped by these components.

## Components

| Component | Purpose |
| --- | --- |
| `StatusLamp` | Pairs a semantic state lamp with a required textual label and optional detail. |
| `RuntimeSwitch` | Renders a native checkbox switch representing requested state only. |
| `ConnectionRow` | Separates desired switch state from actual lamp/output state in one compact row. |
| `CompactRuntimeShell` | Composes identity, target, connections, status, error, and command regions for a toolbar popup. |
| `RuntimeAppShell` | Composes header, application navigation, toolbar, primary surface, inspector, bottom surface, and status for a browser runtime app. |

## Import

```astro
---
import CompactRuntimeShell from "@hara-lang/visual-language/astro/v2/tool/CompactRuntimeShell.astro";
import ConnectionRow from "@hara-lang/visual-language/astro/v2/tool/ConnectionRow.astro";
import ToolButton from "@hara-lang/visual-language/astro/v2/tool/ToolButton.astro";
import "@hara-lang/visual-language/v2-tool.css";
---

<div class="hara-v2 hara-v2-tool">
  <CompactRuntimeShell
    idPrefix="hara-popup"
    label="Hara Chrome connection control"
    state="ready"
    stateLabel="Ready"
    target="chatgpt.com · tab 73"
    targetDetail="Exact bound browser target"
  >
    <ConnectionRow
      slot="connections"
      id="runtime-toggle"
      label="Hara runtime"
      detail="Shared offscreen host"
      state="ready"
      stateLabel="Ready"
      desired
    />

    <div slot="actions">
      <ToolButton label="Open REPL" density="dense" />
    </div>
  </CompactRuntimeShell>
</div>
```

Framework-free consumers use the same `.hara-runtime-*` classes and keep the
rendered switch, output, state text, `data-state`, and `data-desired` attributes
synchronized.

## State vocabulary

Actual state is explicit:

- `off`;
- `starting`;
- `ready`;
- `stopping`;
- `connecting`;
- `connected`;
- `attention` or `warning`;
- `danger` or `error`;
- `disabled`.

Requested state is separately encoded by the native switch and
`data-desired="on|off"`. Products may add domain-specific visible text such as
`Login required`, but they map colour and lamp treatment onto the shared
functional states.

A status lamp is never the only carrier of state. Every lamp has a text label,
either visible in its component or exposed by the adjacent output.

## Compact popup pattern

A toolbar popup uses `CompactRuntimeShell` at 320–380px and normally contains:

1. Hara identity and global actual state;
2. exact browser target;
3. connection rows for current tab, runtime, RESP, and contextual adapter;
4. status rows for DOM, diagnostics, and downloads;
5. one concise error region;
6. two or three frequent commands.

It is an equipment-status surface, not a website. Do not add a hero, marketing
cards, long navigation, or decorative telemetry.

## Runtime application pattern

A full browser-runtime application uses `RuntimeAppShell` with:

- compact application navigation for Runtime, ChatGPT, Tripo, and Diagnostics;
- a shared toolbar for target/session and frequent commands;
- the primary REPL, inventory, asset, or diagnostics surface;
- an optional inspector;
- an optional event/history bottom surface;
- persistent runtime and connection status.

The inspector yields below 1120px and the bottom surface yields below 640px.
Applications provide explicit commands for hidden capabilities.

## Accessibility

- Keep the checkbox as the switch control rather than emulating it with a div.
- Give every switch a useful accessible label.
- Announce only concise state changes through a polite live status.
- Keep actual state visible without relying on colour.
- Preserve `focus-visible` treatment.
- Keep controls at least the shared dense-control height.
- Disable transition animation under reduced motion.
- Do not move focus or change a bound target merely because the popup reopens.

## Adoption sequence

1. Compose and review the compact popup and browser applications in the
   visual-language v2 laboratory.
2. Verify real product states without implying unsupported providers.
3. Import or vendor the accepted framework-free contract downstream.
4. Attach existing runtime behaviour without changing its authority boundary.
5. Remove local tokens and chrome only after light, dark, focus, disabled,
   transition, warning, danger, and compact-width states match.
