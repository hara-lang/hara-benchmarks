# Hara visual language v2 — Specs application contract

## Status

The detailed Specs application laboratory lives at `/v2/specs/`. It is an interactive registry, checker, proposal, and change-review specimen. The fixture data is deterministic and explicitly marked as non-production; the route does not claim to be connected to the `hara-lang/hara-specs` registry or a live conformance service.

The laboratory completes issue #40 inside `hara-lang/visual-language`. It consumes the shared catalogue, component, UI-pattern, theme, and front-matter contracts instead of creating a separate standards design system.

## Product principle

A standards application must answer six questions without making the reader reconstruct authority from prose:

1. What specification is this?
2. Which exact version and source revision does the claim target?
3. Is it draft, proposed, accepted, superseded, withdrawn, or experimental?
4. Which text is normative and which text is explanatory?
5. Which implementation and test revision produced a conformance result?
6. Where are the canonical source, review history, supersession relation, and publication receipt?

Dense registry rows are appropriate when those facts remain aligned and inspectable. Density must not turn the application into a generic administration dashboard or hide status behind colour alone.

## Shared content contract

Specs consumes `hara.specs@3.0.0` from the public front-matter contract:

- `specs.proposal@3.0.0` for an authored change with motivation, compatibility, registry-assigned number, and review decision;
- `specs.version@3.0.0` for an accepted exact specification version with a durable publication receipt;
- `specs.conformance@3.0.0` for checker or implementation evidence against an exact specification revision;
- `specs.publication-receipt@3.0.0` for registry evidence tying identity, version, source revision, and acceptance together.

The browser may author title, summary, abstract, motivation, compatibility notes, proposed normative text, examples, and test-vector references. Specification number, canonical identity, status, accepted version, review decision, conformance claims, source revision, supersession, and publication receipts remain controlled or derived facts.

## Application surfaces

### 1. Registry and discovery

The registry exposes identifier, specification number, title, version, lifecycle status, domain, exact revision, and update date in one horizontally inspectable row. Search and filters operate over stable facts. The selected record opens an inspector with machine identity, canonical source, and receipt.

Every lifecycle state has a complete specimen:

- draft;
- proposed;
- accepted;
- superseded;
- withdrawn;
- experimental.

Empty, stale, and partial registry states retain active filters and exact last-known revisions. A partial index never silently presents itself as complete.

### 2. Exact-version specification detail

The detail reader keeps the outline, authority ledger, normative requirements, grammar, explanatory guidance, related packages, namespaces, implementations, tests, conformance claims, and version history together.

Normative requirements use explicit requirement identifiers and authority words such as **must**, **should**, and **may**. Explanatory notes have a distinct semantic container and cannot be mistaken for compatibility requirements. Historical versions remain directly inspectable and point to their replacement.

### 3. Checker and conformance

The checker accepts pasted source, uploaded files, or registered examples. The result envelope retains:

```text
input label
+ input revision
+ specification identifier and version
+ specification source revision
+ checker implementation and version
+ result state
+ source-located findings
+ exact result receipt, when produced
```

The visible states are:

- **pass** — all selected normative checks passed;
- **warning** — input is valid but carries a compatibility or review warning;
- **failure** — one or more normative requirements failed;
- **unsupported** — the selected checker cannot evaluate a required rule;
- **unavailable** — the checker could not run, so no pass or failure claim exists.

Unavailable must never be normalized to failure. Unsupported must name the missing rule or target. Every source finding keeps a machine code, severity, source location when available, value path when available, and readable explanation.

Conformance rows name the exact specification, implementation, target, implementation revision, passed/total counts, state, and receipt. The application presents claims; the conformance system remains authoritative for their generation.

### 4. Proposal and review workflow

The proposal surface provides structured fields, raw front matter, a rendered preview, compatibility classification, examples, test-vector references, and explicit check results. Its workflow is:

```text
draft
→ checks pending
→ review requested
→ changes requested (optional loop)
→ accepted
→ merged and published
```

The visual application owns authoring assistance, validation presentation, preview, queue, and status projection. GitHub remains canonical for the proposal document, exact revision, discussion, review, merged commit, and acceptance decision. The application references those durable facts rather than copying them into a private review database.

### 5. Change digest

The digest communicates additive, breaking, and proposed changes through:

- exact specification and revision;
- concise consequence-oriented summary;
- affected packages and namespaces;
- concrete migration guidance;
- publication date;
- exact-diff handoff.

Public web, email, RSS, and JSON Feed are peer projections of the same fenced digest entry. Subscribing does not require a Specs account.

## Navigation contract

Visual Language owns the global catalogue launcher, route location, family relationships, page status, and page-level section index. Specs owns only its product workflow and document navigation:

- Registry;
- Detail;
- Checker;
- Proposal;
- Digest;
- Adoption.

The specification outline is local to the selected exact version. Checker controls are local to the checking task. Neither is promoted into global catalogue navigation.

## Responsive and input contract

The primary task yields last:

1. the selected specification document or checker result remains primary;
2. relationship and finding inspectors move below the primary region;
3. persistent outlines become horizontally scrollable local navigation;
4. wide tables scroll inside labelled containers rather than widening the document;
5. dense status inventories collapse from six to three, two, then one column;
6. proposal review evidence moves below authoring fields;
7. all touch controls retain at least a 44px target on narrow screens.

Keyboard users can traverse filters, select registry rows, move between visible rows with Arrow Up/Down, jump with Home/End, select checker scenarios, inspect findings, and move proposal state without pointer-only controls. Focus remains visibly distinct. Reduced-motion mode removes decorative displacement without removing feedback or state changes.

## Ownership boundary

### Shared visual-language package

Owns semantic tokens, typography, material, table/form/status presentation, focus-visible behavior, responsive yielding, receipt presentation, and shared catalogue chrome.

### Specs application

Owns registry search, product navigation, exact-version composition, checker transport selection, authoring assistance, proposal queue, digest filters, and subscription preferences.

### `hara-lang/hara-specs`

Owns canonical identifiers, versions, normative text, machine forms, source revisions, Git history, proposal discussion, review decisions, accepted commits, supersession, withdrawal reasons, and publication receipts.

### Checker and conformance systems

Own checker implementation identity, supported rules and targets, exact result generation, test-vector execution, implementation revisions, conformance claims, and result receipts.

## Fixture contract

`site/src/lib/v2-specs.mjs` is deterministic review data. It deliberately includes all lifecycle and checker states so interaction and responsive behavior can be reviewed without a production service. Downstream products must replace fixture records with authoritative registry responses while retaining the same visible authority envelope.

Fixture labels, identifiers, counts, dates, receipts, and implementation claims must not be marketed as current production registry facts.

## Adoption checklist

Before adopting the laboratory into `hara-lang/hara-specs`:

1. pin a merged Visual Language revision;
2. bind registry rows to exact canonical identifiers, versions, and revisions;
3. retain status words in addition to colour;
4. preserve the normative/explanatory semantic boundary;
5. keep unsupported and unavailable separate from failure;
6. retain machine codes, source locations, value paths, and receipts in checker results;
7. keep GitHub as canonical proposal and review history;
8. provide explicit supersession and withdrawal relations;
9. validate light, dark, keyboard, touch, narrow, zoom/reflow, and reduced-motion behavior;
10. disclose stale, partial, and unavailable registry/checker states without fabricated fallback claims.

## Verification contract

The implementation keeps focused tests for:

- route activation and internal catalogue linking;
- consumption of all four `hara.specs@3.0.0` content types;
- unique fixture identities and exact revisions;
- complete lifecycle, checker, proposal, conformance, digest, and degraded-state inventories;
- deterministic filtering and result lookup;
- registry, detail, checker, proposal, digest, and adoption page structure;
- keyboard selection, focus-visible treatment, responsive breakpoints, contained overflow, 44px touch controls, and reduced motion;
- absence of protected `--hara-*` token redefinitions;
- package inclusion of this adoption document;
- repository-wide `npm test` and `npm run site:build` on the exact pull-request head.
