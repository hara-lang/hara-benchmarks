# Hara visual language v2 — Playground application contract

## Status

The first Playground application laboratory lives at `/v2/playground/`. It is an interactive protocol and responsive-layout specimen, not a connected Hara evaluator. Its controls model lifecycle transitions so downstream implementations can adopt one visible contract without treating the design site as a runtime host.

The route starts issue #39. It deliberately builds on the shared v2 catalogue, UI-pattern, front-matter, component, and tool-workbench layers rather than creating a separate editor system.

## Product principle

The Playground should provide a useful visible result before asking a newcomer to operate a full editor. Its first choices are **Run**, **Edit**, and **Explore**. Samples are grouped by outcomes such as making something move, inspecting a live system, composing graphics, or building a durable work receipt.

Expert users and agents may load an exact repository, branch, path, and revision directly. Missing revisions and unavailable capabilities remain visible states; the application must not silently open the latest source or fall back to a different backend.

## Shared contracts consumed

The application composes these shared surfaces:

- `EnvironmentWorkbench` for the Project, Front matter, Canvas, and Code modes plus optional Sessions, Files, Canvas, and 3D controls.
- shared `Toolbar`, `ToolButton`, `TabStrip`, `ResourceList`, `FrontmatterGrid`, and `StatusBar` primitives;
- the `docs.live-example@2.1.0` content contract for source identity, runtime references, and document embedding;
- `learn.exercise@2.0.0` and `learn.project@2.0.0` when an executable sample carries learning context;
- shared UI-pattern behavior for keyboard tabs, focus-visible treatment, recoverable states, explicit permissions, and responsive disclosure.

The Playground may author titles, summaries, requested source coordinates, and optional learning context. Stable identity, canonical route, exact source revision, actual backend, advertised capabilities, execution receipts, publication state, and replacement history are controlled or derived facts.

## Unified runtime envelope

Every executable surface must display or retain the same lifecycle envelope:

```text
session identity
+ generation
+ exact source revision
+ requested backend
+ actual backend
+ explicit capability set
+ monotonic event sequence
+ lifecycle state
+ receipt references
```

The application contract requires the following behavior:

1. **Run** evaluates only the fenced source revision in the current generation.
2. **Cancel** produces a terminal cancellation state for that execution.
3. **Restart** advances generation while retaining session identity and source revision.
4. **Replacement** creates a newly fenced session rather than mutating source identity in place.
5. **Disposal** is terminal and idempotent.
6. Backend selection never silently falls back. An unavailable HBC request is shown as unavailable with no fabricated interpreter result.
7. Interpreter- and HBC-specific observations may differ, but both use the same lifecycle and event envelope.
8. Sequence numbers are monotonic within the session envelope and remain visible in output, console, status, and receipts.

The laboratory script simulates these transitions for interaction review. A production Playground must bind the same presentation to the browser live-session API.

## Main studio composition

The full workspace has five application modes:

- **Navigation / project** — repository tree, exact source coordinates, and replacement semantics.
- **Front matter / configuration** — author intent beside controlled runtime and registry facts.
- **Graphics / canvas** — capability-gated visual output and controls.
- **Code** — source editor, result, observations, diagnostics, and stack trace.
- **Console / observations** — monotonic events and fenced evaluation commands.

The optional live-control pane contains only capability groups advertised by the current session. A missing capability should either omit its controls or show a bounded unavailable state; it must not imply support through inactive decorative controls.

Clean, comfortable, and dense modes may change spacing. They must not remove session identity, source revision, backend, capabilities, diagnostics, event sequence, or receipt evidence.

## Documentation embeds

Two embed scales are supported:

- **Inline** keeps documentation prose primary and exposes source, Run, Cancel, Restart, result, source fence, and an exact Playground handoff.
- **Expanded** may reveal Code, Sessions, and Files through the shared workbench. Canvas and 3D remain absent unless the exact example advertises them.

The host requests read-only or editable behavior and optional controls. The runtime response remains authoritative for backend, capability, lifecycle, source fence, and receipts.

Exact share links fence repository, branch, path, revision, backend request, and editability. Private or unpublished content has no public route, and a copied URL does not grant permission. Stale links preserve the exact historical revision and require an explicit action to follow a replacement.

## Mobile and touch

Mobile execution follows an explicit focus contract:

- initial source is read-only;
- **Run** updates status and result without focusing the editor or summoning the software keyboard;
- **Edit** is the only initial action that unlocks and focuses source;
- transport controls retain at least a 44px touch target;
- optional Canvas and 3D controls yield first;
- Sessions and Files move to a disclosure or bottom sheet;
- result follows the editor in document order;
- diagnostics and code scroll inside their own regions rather than causing horizontal page overflow.

## Ownership boundary

### Shared visual-language package

Owns workbench geometry, component styling, keyboard/focus presentation, responsive yielding, status treatment, and capability-aware slot composition.

### Playground application

Owns repository loading, sample discovery, project navigation, editor state, saved and recent sessions, anonymous versus signed-in behavior, sharing policy, and application commands.

### Docs and Learn products

Own surrounding narrative, curriculum context, read-only/editable request, placement, and the handoff into the full Playground.

### Runtime and registries

Own session lifecycle, exact source identity, actual backend, capabilities, observations, diagnostics, receipts, canonical content identity, permissions, publication state, and replacement history.

## Verification contract

The implementation must keep focused tests for:

- route activation and catalogue linking;
- required arrival, studio, control-pane, embed, sharing, and mobile states;
- composition of shared primitives instead of duplicate workbench markup;
- runtime fencing, explicit backend failure, monotonic sequence, cancellation, restart, replacement, and idempotent disposal markers;
- no editor `autofocus` and no focus call in the mobile Run path;
- keyboard tabs, focus-visible CSS, responsive breakpoints, 44px touch controls, reduced motion, and absence of protected `--hara-*` token redefinitions;
- complete repository checks through `npm test` and `npm run site:build` on the pull-request head.
