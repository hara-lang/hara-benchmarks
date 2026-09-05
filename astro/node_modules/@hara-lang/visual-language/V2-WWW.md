# Hara v2 WWW family

Issue #38 turns the earlier compact Home, Docs, and Benchmarks specimens into a directly reviewable application family:

- `/v2/www/`
- `/v2/www/docs/`
- `/v2/www/benchmarks/`

The buildout is a visual-language reference implementation. It specifies information hierarchy, shared component ownership, runtime and evidence states, responsive behaviour, and the contract expected of downstream adopters. Fixture content is deliberately realistic enough to review, but it is not production data.

## Family model

One `WwwFamilyHeader` owns the relationship among Home, Docs, and Benchmarks. It provides:

- a stable Hara identity;
- direct Home / Docs / Benchmarks routes;
- family-wide search entry;
- account entry;
- the shared theme control;
- current-route context; and
- a quiet path back to the visual-language catalogue.

Each route adds a `WwwSubnav` for route-local sections and actions. Product pages do not render `CatalogueHeader`, because doing so would create two competing global navigation systems.

## Shared visual-language ownership

The common visual language owns:

- colour, type, spacing, material, focus, motion, and responsive tokens;
- buttons, fields, selects, badges, tables, and document prose primitives;
- the theme implementation;
- reusable runtime and workbench primitives under `src/astro/v2/*`; and
- the catalogue that discovers implemented application routes.

The issue #38 family consumes these foundations through `src/v2.css` and small Astro components. It does not redefine the theme or create an unrelated component system.

## Shared content-contract ownership

`site/src/lib/v2-frontmatter.mjs` remains the only contract source. `site/src/lib/v2-www.mjs` resolves and fails closed on:

- `hara.www` / `www.narrative-page` / `www.capability`;
- `hara.docs` / `docs.guide` / `docs.reference` / `docs.version` / `docs.live-example`; and
- `hara.benchmarks` / report, workload, baseline, methodology, and evidence records.

The family does not duplicate front-matter fields locally. Editable narrative intent remains distinct from registry-owned authors, revisions, runtime examples, proof references, workloads, baselines, methods, evidence, comparability, and publication receipts.

## WWW-family ownership

`site/src/components/v2-www/*` owns the family-level application patterns:

- `WwwFamilyHeader.astro` — identity, family routes, search, account, theme, and route relationship;
- `WwwSubnav.astro` — route-local location and commands;
- `LiveHaraExample.astro` — static source plus a bounded runtime contract, actions, optional control pane, and degraded states;
- `StateSpecimen.astro` — visible unavailable, error, stale, missing, incomparable, and low-confidence outcomes; and
- `ViewportSpecimen.astro` — explicit desktop, tablet, and mobile review frames.

`site/src/styles/v2-www.css` owns composition for this family. It does not move product-specific layout into global v2 primitives until another product demonstrates the same need.

## Home contract

The Home route uses the order:

1. proposition;
2. proof ledger;
3. explanation / proof / action first example;
4. portability, tooling, runtimes, and interop;
5. ecosystem orientation;
6. package and project proof;
7. release and change summary;
8. Learn and World handoffs;
9. browser, CLI, and agent-first starting paths;
10. degraded and first-arrival states; and
11. responsive and adoption specimens.

The ecosystem map is intentionally small. It explains how language, runtime, libraries, evidence, and community relate without turning the public homepage into a full product directory.

The first example is static documentation before it is executable. The page remains useful when the Wasm backend is unavailable or deferred for low bandwidth.

## Docs contract

The Docs route distinguishes four content roles:

- task-oriented landing paths;
- explanatory guides and articles;
- canonical API and namespace reference; and
- optional executable examples.

The guide shell retains persistent navigation and outline on wide screens. On smaller screens, the outline folds first and the guide rail becomes a labelled drawer boundary. Prose remains primary.

`LiveHaraExample` exposes:

- runtime backend;
- session identity and scope;
- fenced generation;
- declared capabilities;
- exact source revision;
- Run, Copy, Open in Playground, and Exact revision actions; and
- optional Sessions, Files, Canvas, and 3D controls.

The component also documents runtime unavailable, compile error, and stale-version states. In all three states, source and exact revision remain inspectable.

## Benchmarks contract

The Benchmarks route orders evidence as:

1. bounded question and fixture disclosure;
2. top insights with confidence and evidence references;
3. filterable, shareable workload matrix;
4. selected-result detail;
5. exact environment, baseline, and methodology beside the result;
6. source-revision history;
7. missing, incomparable, and low-confidence review states;
8. responsive specimens; and
9. compact audit/source table.

The source table comes later because a dense ledger is not a substitute for interpretation. The matrix remains a semantic HTML table. Mobile workload cards aid scanning, while the canonical table remains available for assistive and horizontal inspection.

All numeric values in the visual-language route are fixture data. They are explicitly labelled as an interface fixture and must not be published as Hara performance claims.

## Fixture data versus production data

The visual-language repository owns fixture data only when it is needed to demonstrate:

- hierarchy;
- interaction;
- data density;
- missing and degraded states;
- responsive reflow; and
- evidence adjacency.

Production data must come from the owning registry or product:

- release and package facts from package and release registries;
- documentation symbols from the symbol and documentation registries;
- search results from the production search index;
- live state from the runtime provider;
- benchmark samples and methods from the evidence registry; and
- identity/account state from the production identity provider.

## Adoption: hara-www

Consume:

- `WwwFamilyHeader` and `WwwSubnav`;
- the Home narrative hierarchy;
- `hara.www` content contracts;
- proof-reference placement; and
- the live-demo unavailable and low-bandwidth contracts.

Replace:

- fixture release feed;
- fixture project/package proof;
- placeholder search;
- placeholder account state; and
- demo runtime adapter.

Preserve the explanation → proof → action hierarchy. An unavailable demo must not collapse into a fake success animation or remove its static source.

## Adoption: hara-docs

Consume:

- the guide reading shell;
- task map, API rows, and filtered-result patterns;
- `LiveHaraExample` and all runtime state contracts;
- `hara.docs` content contracts; and
- the rule that static documentation is useful without execution.

Replace:

- fixture task records;
- fixture search index;
- fixture symbol records;
- version/runtime selector options; and
- runtime provider implementation.

Preserve prose primacy, exact revisions, visible compatibility, and the distinction between static and executable content.

## Adoption: hara-benchmarks

Consume:

- the insight-first order;
- the accessible comparison matrix;
- selected-result evidence composition;
- comparability and confidence states;
- the history and compact source ledger; and
- `hara.benchmarks` content contracts.

Replace every numeric fixture, source revision, baseline, sample, environment, method, confidence assessment, and evidence digest with production registry data.

Preserve the rule that every promoted claim exposes method, environment, samples, baseline, revision, confidence, and comparability. Missing or incomparable results remain visible and are never coerced into zero or a winner.

## Validation

Run from the repository root:

```sh
npm test
npm run site:build
```

The issue-specific tests verify route discovery, shared contract identity, component ownership, required Home/Docs/Benchmarks states, responsive rules, fixture disclosure, accessible tables, and downstream adoption notes.
