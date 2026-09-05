# Hara visual language v2 — Packages application contract

## Status

The detailed Packages application laboratory lives at `/v2/packages/`. It is the visual acceptance surface for the future packages/registry product: package and namespace discovery, exact release evaluation, install handoff, publishing, maintenance, compatibility, signing, provenance, and reproduction.

The laboratory uses deterministic design-review fixtures. The shown versions, coordinates, maintainers, signatures, digests, dates, compatibility results, and receipts are not live package-registry records.

## Product principle

A package browser should make the exact installable object easier to understand than its popularity. Every important screen should keep the following facts adjacent:

- canonical package coordinate;
- exact release version and revision;
- included namespace references;
- current maintainers and delegated scopes;
- runtime and platform compatibility evidence;
- source and artifact digests;
- lifecycle status, migration relations, and revocation evidence;
- publisher identity, signature, and durable receipts;
- reproduction inputs.

Usage and reverse-dependency counts may help discovery, but they never replace compatibility, maintenance state, or provenance.

## Shared content contract

Packages consumes the complete `hara.packages@2.2.0` family:

- `packages.package@2.2.0` — canonical package identity and discovery metadata;
- `packages.release@2.2.0` — immutable version, namespace inventory, artifacts, compatibility, and publication evidence;
- `packages.namespace@2.2.0` — namespace identity, stewardship, public API, aliases, conflicts, and migrations;
- `packages.maintainer@2.2.0` — identity and delegated package or namespace scope;
- `packages.compatibility@2.2.0` — exact runtime, language, platform, and dependency compatibility evidence.

Authors may edit titles, summaries, tags, release notes, and migration notes. Package coordinates, namespace stewardship, release version, maintainers, compatibility evidence, artifact digests, status, exact revision, and publication receipts remain registry- or identity-controlled facts.

A browser form may propose exact bytes and declarations. It never assigns a durable release identity.

## Package identity and namespace identity

Package identity and namespace identity remain visually and semantically distinct.

A package coordinate identifies a distribution unit such as `hara/std.typed`. A namespace identity identifies a stewardship and API boundary such as `namespace:std.typed`. A package may distribute several namespaces, and a namespace may retain historical availability across several package releases, but neither identity is treated as an alias for the other.

Every package view should link to exact namespace records rather than copying namespace ownership, public forms, aliases, or migration state into package-local metadata. Every namespace view should reference its current package and release availability without making the namespace route a second package record.

## Application surfaces

### Discovery

Discovery supports exact package coordinates, namespace names, purpose, and capability queries. Filters remain independent for:

- domain;
- runtime;
- stability;
- license;
- compatibility.

Recently updated, widely used, and newly published are explicit orderings over the same exact package records. Widely used does not remove release, maintenance, compatibility, license, or registry-revision facts.

The discovery contract includes ready, empty-query, no-results, stale-index, and registry-degraded states. A stale index exposes its indexed-at fence. A degraded registry labels cached results and disables publishing, following, and new compatibility claims. It does not fabricate an empty registry.

Saved and followed packages are account or browser preferences, not registry facts.

### Package detail

A package detail surface includes:

- package coordinate and concise purpose;
- current release, status, exact revision, artifact digest, source revision, publisher, and publication time;
- an install projection that names the exact version and digest;
- exact namespace inventory;
- maintainers, reviewers, delegated scopes, and owned release bots;
- runtime compatibility matrix with evidence references;
- dependencies, resolved versions, digests, and reverse dependencies;
- release history, migration notes, deprecations, supersession, withdrawal, and revocation;
- Docs, Playground, Specs, World, source, license, receipt, and reproduction links.

The visual laboratory may show an illustrative CLI projection. The resolver and package runtime own executable install syntax, dependency resolution, artifact download, verification, installation, and install-attempt receipts.

Install failure is not release revocation. A resolver or mirror failure may produce an install-attempt receipt while the release remains current. A revoked release is a registry lifecycle decision backed by verification or authority evidence and blocks installation under registry policy.

### Namespace detail

The namespace surface includes:

- namespace identity, package reference, status, introduction, and deprecation versions;
- owner and delegated stewards;
- public forms grouped by category and kind;
- form introduction and deprecation versions;
- exact examples and canonical Docs or Playground handoff;
- runtime and package availability;
- aliases, conflicts, and qualified resolution guidance;
- migration relations and receipts;
- contributor and reviewer evidence.

Qualified symbols remain visible when they preserve ownership and conflict resolution. Historical aliases stay inspectable through their migration window.

### Publish workflow

Publishing separates author intent from controlled release facts.

Author-controlled fields include title, summary, tags, release notes, and migration notes. Registry- and identity-controlled fields include content identity, package coordinate, namespace references, version, maintainers, compatibility evidence, artifact digests, lifecycle status, exact revision, and publication receipt.

The workflow includes:

- metadata and raw front matter;
- version, language range, and runtime declaration;
- namespace inventory;
- source, JVM, Wasm, reproduction, and other artifact inventory;
- dependency lock and ownership checks;
- cross-runtime compatibility checks;
- registry listing and install preview;
- publisher key, source fence, artifact manifest, and expected receipt;
- draft, checks-failing, review-pending, published, superseded, and revoked states.

A failed check preserves the exact build attempt. Review pending makes the submitted revision read-only. Published creates durable registry evidence. Superseded and revoked states retain history and name their replacement or reason.

### Maintainer dashboard

Maintainer surfaces organize work by consequence rather than engagement:

- releases awaiting action;
- namespace ownership requests;
- deprecation and migration plans;
- dependency alerts and compatibility breakage;
- contributor and reviewer activity;
- evidence that can appear on contributor profiles and badges;
- user-owned release bots.

User-owned release bots always display bot identity, verified owner, purpose, capability scope, owner-presence rule, and receipt or policy reference. An owner-away policy may pause a sensitive action without deleting the bot’s historical receipts.

Maintainers may propose notes, compatibility targets, migrations, and delegated scope. They cannot rewrite historical digests, publisher identity, verification receipts, or revocation evidence.

## Trust and provenance

The product must answer six questions from named authorities and evidence:

1. Who published this package?
2. Which source revision and artifacts were published?
3. Which namespaces are included?
4. Which runtime targets are supported?
5. What changed from the previous version?
6. How can the release be verified or reproduced?

The reproduction chain should retain source revision, dependency lock, build environment, artifact manifest and digests, compatibility checks, publisher signature, and publication receipt. Downloads are projections of these same exact facts, not another authority.

## Ownership boundary

### Shared visual-language package

Owns shell geometry, typography, identity labels, filters, tables, forms, status, focus, responsive transformation, receipt presentation, and degraded-state grammar.

### Packages application

Owns discovery, comparison, package and namespace navigation, install projection, publish composition, maintainer queues, saved/followed preferences, and cross-product handoffs.

### Package, release, namespace, compatibility, and identity registries

Own package coordinates, namespace stewardship, versions, maintainers, artifacts, compatibility evidence, lifecycle decisions, publisher signatures, and durable receipts.

### Resolver and runtimes

Own dependency resolution, download, verification, installation, environment checks, execution, reproduction, and install-attempt receipts.

### Docs, Playground, Specs, and World

Own version-aware explanation, exact execution, formal definitions, and public discussion respectively. Packages links to these products without absorbing their information architecture or authority.

## Responsive and input contract

The primary package task yields last:

1. package purpose, exact release, namespace identity, or active publish form remains primary;
2. inspectors move below the main record;
3. release histories, workflow steps, and filters become contained horizontal lists;
4. compatibility, artifact, API, and activity tables scroll inside labelled regions;
5. maintainer navigation yields before action evidence;
6. no exact digest, coordinate, namespace, receipt, or error message is truncated without a full inspectable representation;
7. narrow-screen controls retain at least a 44-pixel touch target.

Keyboard users can search, filter, change ordering, save or follow, select release states, search namespace forms, inspect publish states, filter maintainer work, copy exact values, and traverse product handoffs. Focus remains visible. Reduced motion removes decorative movement without removing state feedback.

## Fixture contract

`site/src/lib/v2-packages.mjs` contains deterministic design-review data covering:

- six package coordinates and their namespace inventories;
- domain, runtime, stability, license, compatibility, update, use, save, and follow facts;
- ready, empty, no-result, stale, and degraded discovery states;
- one detailed package and release record;
- available, install-failure, deprecated, superseded, withdrawn, and revoked release states;
- namespace API, availability, aliases, conflicts, migrations, and contribution evidence;
- draft, checks-failing, review-pending, published, superseded, and revoked publish states;
- maintainer queues, contributor/reviewer activity, and accountable bots;
- the six provenance questions and reproduction chain.

Fixture records must not be presented as current package-registry data.

## Adoption checklist

Before adopting the laboratory into the packages/registry product:

1. pin a merged Visual Language revision;
2. bind package, release, namespace, maintainer, and compatibility views to exact canonical references;
3. keep package and namespace identity distinct in routes, labels, search, and receipts;
4. retain compatibility and maintenance facts in every popularity-based view;
5. distinguish install-attempt failure from release withdrawal or revocation;
6. keep historical releases, digests, migration relations, and revocation evidence inspectable;
7. keep author-controlled release notes separate from registry-controlled identity and artifacts;
8. require exact namespace ownership and dependency checks before publication;
9. show owned bots with verified owner, purpose, scope, presence rule, and receipts;
10. delegate installation and reproduction behavior to the resolver and runtimes;
11. validate keyboard, touch, light, dark, zoom/reflow, narrow widths, reduced motion, stale index, and registry degradation.

## Verification contract

The implementation keeps focused tests for:

- `hara.packages@2.2.0` content-type consumption;
- unique package coordinates and namespace references;
- deterministic query, filter, and ordering behavior;
- discovery service states;
- release, namespace, maintainer, compatibility, artifact, migration, and provenance inventories;
- available, install-failure, deprecated, superseded, withdrawn, and revoked release states;
- draft, checks-failing, review-pending, published, superseded, and revoked publishing states;
- accountable bot ownership and owner-away behavior;
- discovery, package, namespace, publish, maintain, trust, and adoption structure;
- shared `Shell` reuse and package/namespace identity distinction;
- Docs, Playground, Specs, and World handoffs;
- keyboard markers, focus-visible treatment, contained overflow, 44-pixel touch controls, responsive breakpoints, and reduced motion;
- absence of protected `--hara-*` token redefinitions;
- active catalogue route and package inclusion of this document;
- repository-wide `npm test` and `npm run site:build` on the exact pull-request head.
