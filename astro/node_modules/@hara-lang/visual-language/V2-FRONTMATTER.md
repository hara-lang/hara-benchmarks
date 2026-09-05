# Hara v2 front matter content contract

The front matter contract is the executable metadata registry behind the `/v2/frontmatter/` review laboratory. It is published from the package so WWW, Docs, Benchmarks, Specs, Packages, World, and Learn can consume the same accepted definitions without copying laboratory data.

```js
import {
  contentContracts,
  contentTypeById,
  browserEditableFields,
  controlledFields,
  derivedFields,
  validateSpecimen,
  frontmatterRepresentations,
  previewFromSpecimen
} from "@hara-lang/visual-language/v2/frontmatter.js";
```

The source of truth is `src/v2/frontmatter.mjs`. The historical site entrypoint, `site/src/lib/v2-frontmatter.mjs`, only re-exports that module so the catalogue and downstream package users resolve one API.

## What the contract contains

The registry defines:

- seven application-family contracts: WWW, Docs, Benchmarks, Specs, Packages, World, and Learn;
- thirty concrete content types;
- eighteen shared fields;
- product-specific field inventories;
- required, optional, and deprecated requirements;
- author, derived, identity, registry, source, reviewer, and runtime control boundaries;
- draft, proposed, reviewed, published, superseded, and withdrawn lifecycle states;
- valid, invalid, imported, and migrated specimens;
- validation messages;
- YAML, JSON, Hara-form, Markdown, and Hara-publication representations;
- route, card, feed, search, social, and machine previews;
- application adoption mappings, relationship boundaries, and registry statistics.

## Public data

### `controlLabels`

Human-readable labels for the seven control authorities:

```text
author · derived · identity · registry · source · reviewer · runtime
```

Control is semantic, not visual decoration. A browser form may edit author-controlled fields. It may display, select, or request changes to other facts, but it must not manufacture identity, registry, source, reviewer, runtime, or derived truth.

### `lifecycleStates`

The durable publication vocabulary:

```text
draft → proposed → reviewed → published → superseded → withdrawn
```

Each state names its actor, durability boundary, and meaning. A transient success message is not a lifecycle record.

### `sharedFields`

Fields common to content products where their semantics are genuinely shared. The shared inventory includes schema identity, schema version, stable content identity, content type, title, summary, slug, canonical URL, authors, lifecycle status, locale, tags, timestamps, exact revision, publication receipt, provenance, and the deprecated legacy permalink.

Every field records:

```text
id · label · type · requirement · control · source · description
```

Fields may additionally name a default, derivation inputs, registry ownership, or a replacement for a deprecated field.

### `contentContracts`

The seven family contracts. Each contract records:

```text
id · label · application issue · route · summary
schema namespace · schema version · publication paths
registry owner · product fields · concrete types
```

The common envelope does not erase product semantics. Benchmark evidence, a package namespace, a World canonical source, and a Learn prerequisite remain distinct fields with distinct owners.

### `contentTypeInventory`

A flattened inventory of all concrete content types. Current examples include:

```text
www.narrative-page
www.capability

docs.guide
docs.reference
docs.version
docs.live-example

benchmarks.report
benchmarks.workload
benchmarks.baseline
benchmarks.methodology
benchmarks.evidence

specs.proposal
specs.version
specs.conformance
specs.publication-receipt

packages.package
packages.release
packages.namespace
packages.maintainer
packages.compatibility

world.article
world.clipping
world.feed
world.profile
world.bot

learn.lesson
learn.concept
learn.exercise
learn.project
learn.progress
```

### `relationships`

The external ownership boundaries used by content records. Identities, packages, namespaces, sources, evidence, specifications, and runtime facts are referenced from their owning registries rather than copied into front matter as unverified display data.

### `specimens`

Review records that cover successful, invalid, imported, and migrated states. Each specimen keeps authored, controlled, and derived facts in separate maps. Imported records may attach provenance; migrated records may attach a deterministic migration receipt.

### `applicationContractMap`

The adoption map for application issues #38–#43. Applications can discover which content families, publication paths, schema versions, and registry boundaries they consume while keeping product workflow logic local.

### `registryStats`

Counts used by catalogue and verification surfaces. They make missing families, types, fields, lifecycle states, or controlled facts detectable rather than implicit.

## Public queries

### `contentContractById(id)`

Return one family contract such as `docs`, `benchmarks`, `packages`, or `world`.

```js
const docs = contentContractById("docs");
console.log(docs.schemaNamespace); // hara.docs
console.log(docs.schemaVersion);   // 2.1.0
```

### `contentTypeById(id)`

Return one flattened concrete content type.

```js
const guide = contentTypeById("docs.guide");
console.log(guide.family);  // docs
console.log(guide.version); // 2.1.0
```

### `fieldInventoryForContract(family)`

Combine shared fields with the product-specific fields for one family.

### `fieldInventoryForType(contentType)`

Resolve the complete field inventory for one concrete type.

### `requiredFieldsForType(contentType)`

Resolve the required shared and product fields, including durable schema, identity, route, timestamp, revision, and lifecycle facts.

### `browserEditableFields(contentType)`

Return only non-deprecated author-controlled fields that may appear as browser-editable inputs.

### `controlledFields(contentType)`

Return identity-, registry-, source-, reviewer-, and runtime-controlled fields. Applications should render their owner and source rather than presenting them as ordinary text inputs.

### `derivedFields(contentType)`

Return generated fields. Every derived field must name its derivation inputs.

## Validation

### `combinedSpecimenValues(specimen)`

Combine authored, controlled, and derived maps for inspection and projection. Separation is retained on the specimen itself so mutation boundaries remain reviewable.

### `validateSpecimen(specimen)`

Return structured validation messages with:

```text
level · code · field · message
```

Validation covers:

- unknown content types;
- missing required fields;
- browser attempts to author controlled or registry-owned fields;
- deprecated fields and their replacements;
- schema-version migrations;
- missing derivation sources;
- attached provenance;
- attached migration receipts;
- successful contract conformance.

Validation preserves authored work. It does not invent missing identities, revisions, review decisions, source evidence, runtime observations, or publication receipts.

### `specimenValidation`

Precomputed validation results for every shipped specimen. This is useful for review surfaces and deterministic tests.

## Representations

### `frontmatterRepresentations(specimen)`

Produce equivalent projections of the same semantic record:

```text
YAML · JSON · Hara form · Markdown · Hara publication form
```

Representation changes syntax, not field meaning, control, required status, lifecycle, or registry ownership.

```js
const views = frontmatterRepresentations(specimen);
console.log(views.yaml);
console.log(views.haraPublication);
```

## Previews

### `previewFromSpecimen(specimen)`

Derive the visible and machine interfaces driven by one record:

```text
route · card · feed · search · social · machine
```

Previews expose canonical identity, route, summary, source, status, revision, and machine context. Changing theme, width, or preview kind must not mutate the content record.

## Product boundaries

The package contract owns:

- field and content-type meaning;
- control and source metadata;
- schema versions;
- lifecycle vocabulary;
- validation shape;
- representations and preview projections;
- relationship boundaries;
- deterministic specimen and migration evidence.

Applications own:

- product navigation and composition;
- authoring workflow;
- ranking and search policy;
- review and moderation policy;
- benchmark comparability policy;
- package publication workflow;
- curriculum and progress presentation;
- responsive product decisions beyond the shared interaction contract.

External services and registries own:

- identity profiles and accountable bot ownership;
- package and namespace stewardship;
- specification status;
- canonical source and syndication truth;
- benchmark, conformance, and compatibility evidence;
- exact runtime capabilities and observations;
- publication acknowledgement;
- user progress.

## Adoption rule

Downstream products should pin a merged `@hara-lang/visual-language` revision and import this module. They should not copy `contentContracts`, fork lifecycle names, or redefine control labels locally.

The catalogue route remains a review and acceptance surface. Its product-owned CSS and specimen composition are not package runtime dependencies.

## Compatibility entrypoint

The site compatibility file intentionally contains only:

```js
export * from "../../../src/v2/frontmatter.mjs";
```

This keeps existing catalogue imports stable while ensuring the package and site cannot drift into two content registries.

## Validation requirements

Changes to the public contract must pass:

```sh
npm test
npm run site:build
```

Focused package tests verify:

- the package export resolves to `src/v2/frontmatter.mjs`;
- the written contract is included in the package files;
- package and site entrypoints expose exactly the same names and object identities;
- representative query, validation, representation, and preview behavior remains available;
- the accepted `/v2/frontmatter/` route and its existing contract tests remain unchanged.
