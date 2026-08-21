# Hara Benchmarks — Visual Language v2 adoption

## Accepted source

The dashboard publication workflow pins `hara-lang/visual-language` at merged revision:

```text
a2ab66d0fde79edb1cee46b79528098b3fda68cf
```

Before presentation tests or builds, the workflow materialises only that package revision's declared publication boundary. The accepted revision includes the shared v2 document shell, review grammar and accessible evidence/data-visualisation contract.

## This first adoption slice

- adopts the exported v2 `Header` while retaining benchmark-owned destinations and sign-in;
- opts the dashboard into the shared v2 document and data/evidence stylesheets;
- adds a direct skip path, stable evidence focus target, 44-pixel controls, visible focus, contained matrix overflow and reduced-motion handling;
- places the evidence contract—measure direction, comparison boundary, uncertainty and authority—immediately after the overview;
- maps existing matrices, detail inspectors and result panels onto shared v2 tokens without replacing their data or interaction logic.

## Preserved benchmark authority

This visual adoption does not change:

- benchmark runners, suites, profiles or runtime selection;
- canonical evidence ingestion or presentation-data derivation;
- workload equivalence, baselines, ratio calculation or geometric means;
- sample values, uncertainty, HTTP measurements or runtime telemetry;
- tab, deep-link, matrix-selection or live detail behavior;
- homepage evidence endpoint, history branch or publication artifact;
- canonical and social metadata.

## Ownership boundary

Visual Language owns shared document geometry, navigation, state vocabulary, evidence presentation, focus and responsive grammar. `hara-benchmarks` remains authoritative for measurements, methods, transformations, comparisons, source revisions and interactions.

`astro/src/styles/v2-adoption.css` is a product mapping layer. It consumes protected `--hara-v2-*` tokens but does not redefine them.

## Remaining issue #23 work

This PR begins but does not close the complete Benchmarks adoption. Follow-on slices should:

1. align class, language, HTTP and runtime panels with the accepted `/v2/data/` benchmark compositions;
2. expose sample counts, intervals and explicit unavailable states wherever the underlying evidence provides them;
3. attach light/dark desktop and mobile screenshots for every tab and selected-detail state;
4. remove superseded local shell declarations after all routes and print behavior are verified;
5. keep every downstream change pinned to a merged Visual Language revision.
