# Hara visual language v2 — Learn application contract

## Status

The detailed Learn application laboratory lives at `/v2/learn/`. It is the visual acceptance surface for a future `learn.hara-lang.org` product: experience-aware arrival, curriculum and concept graphs, lesson reading, executable practice, projects, revision-aware progress, teaching workflows, and the explicit boundary with World.

The laboratory uses deterministic design-review fixtures. It is not a production learner database, live curriculum registry, evaluator, or completion authority.

## Product principle

Learn should let someone produce a visible result before asking them to understand the whole language or create an account. It then grows that result through concepts, exercises, projects, and meaningful evidence.

The product rejects opaque engagement mechanics. It records:

- exact lessons and curriculum revisions;
- attempts and checker receipts;
- concepts learned;
- first run, first source change, first solved problem, and first useful project;
- selected projects and private notes;
- explicit migration when curriculum or exercise versions change.

It does not require XP, vanity leaderboards, streaks, or penalties for pausing.

## Shared content contract

Learn consumes the complete `hara.learn@2.0.0` family:

- `learn.lesson@2.0.0` — guided explanation with objectives, prerequisites, optional runtime example, and exact revision;
- `learn.concept@2.0.0` — canonical concept in the prerequisite graph;
- `learn.exercise@2.0.0` — bounded practice with starter source, checks, hints, and expected evidence;
- `learn.project@2.0.0` — multi-step useful build with milestones, reflection, and runtime handoff;
- `learn.progress@2.0.0` — account-scoped attempts and completion evidence against an exact curriculum revision.

Authors may edit titles, summaries, learning objectives, prerequisite references, estimates, exercise specifications, project guidance, and explanatory prose. Content identity, authorship references, concept graph, runtime environment, status, exact revision, attempts, completion evidence, and progress remain registry- or runtime-controlled facts.

Progress is never authored as front matter.

## Application surfaces

### Arrival

The landing provides three explicit experience entrances:

1. new to programming;
2. programmed before;
3. familiar with Lisp.

Each entrance changes explanation depth and the recommended first lesson. All entrances resolve into one visible curriculum graph.

Outcome tracks include Web, Agents, Graphics, Games, Music, and Language tools. Preview tracks remain labelled as previews rather than implying capability or course availability.

Anonymous visitors can run the first lesson and local exercises without signing in. Recent progress remains browser-local until explicitly saved. Account creation is offered only after meaningful activity.

### Course and concept graph

A course view contains lessons, concepts, exercises, and projects with complete, current, locked, and optional states. Locked units remain visible and name their prerequisites. Optional branches do not become hidden requirements.

Every course exposes:

- content type and schema version;
- author identity reference;
- exact course revision;
- runtime compatibility;
- estimated scope;
- downloadable machine manifest;
- prerequisite graph;
- state semantics.

### Lesson reader

Reading remains primary. The lesson surface includes:

- objectives and prerequisites;
- calm explanatory prose;
- runnable source and result;
- Run, Edit, Reset, and exact Playground handoff;
- session, generation, backend, capabilities, source revision, event sequence, and curriculum revision;
- glossary and related Specs, Packages, and World links;
- check-for-understanding interaction;
- stale lesson and runtime-unavailable states.

Run must never focus the editor. Edit is the explicit action that unlocks and focuses source. This applies on desktop, mobile, and embedded lesson contexts.

### Practice and koans

The practice contract distinguishes:

- initial;
- checking;
- local failure;
- local pass;
- server-verified completion;
- exercise version changed;
- runtime unavailable.

A local pass is useful immediate feedback, not an external verification claim. Durable or competitive claims require a named verifier and receipts for the exact exercise, curriculum, source, checker, and identity references.

Runtime unavailable is not failure. The exact source and retry context remain visible.

Hints use progressive disclosure. Peer approaches remain unavailable until a solved state. Saving progress becomes available after a meaningful attempt, not before execution.

### Project learning

Projects may produce a page, agent workflow, visual, game, or audio patch. The detailed specimen reuses the shared `EnvironmentWorkbench` and Playground runtime envelope for navigation, front matter, Canvas, Code, Sessions, Files, observations, and status.

Learn owns project milestones, explanation, reflection, and curriculum evidence. Playground owns execution, source loading, runtime commands, exact sharing, and publication handoff. World owns a linked public discussion.

### Progress and profile

Progress is private by default and revision-aware. It presents meaningful milestones, path completion by exact revision, saved examples, notes, privacy controls, and export.

The learner may share selected projects. Notes, attempts, and the full progress record never become public merely because the same identity participates in World.

### Teaching and reference

The teaching surface supports:

- structured lesson authoring;
- raw front matter and rendered preview;
- author-controlled versus registry/runtime-controlled field inspection;
- concept registry and prerequisite maintenance;
- explicit schema migration review;
- JSON, Hara form, RSS curriculum feed, and downloadable course manifest projections;
- reading and accessibility controls.

Git or another canonical content repository may own durable proposal and review history. The Learn product should reference that history rather than copying it into a private review silo.

## World boundary

Learn and World may share identity and links, but not product ownership:

### Learn owns

- instructional sequence;
- curriculum and prerequisite graph;
- lesson placement;
- exercises and projects;
- attempts and completion evidence;
- private notes and progress;
- exact curriculum revision and migration.

### World owns

- articles and canonical outbound sources;
- clippings;
- comments and mentions;
- contributor profiles;
- presence;
- accountable bots;
- Snippet of the day as a social object;
- discussion around lessons, projects, releases, and packages.

A World article may link into a lesson. A Learn project may link to a World thread. World popularity never unlocks Learn content, and Learn progress never becomes a World reputation score.

## Ownership boundary

### Shared visual-language package

Owns semantic tokens, typography, material, status, form, table, focus, responsive, workbench, and receipt presentation.

### Learn application

Owns experience entrances, track browsing, curriculum navigation, lesson composition, practice commands, project milestones, notes, privacy, teaching tools, and product-local navigation.

### Curriculum and progress registries

Own content identities, concept graph, exact revisions, status, migration relations, attempts, completion evidence, learner visibility, and account-scoped progress.

### Playground and runtime systems

Own sessions, generations, source fences, backends, capabilities, observations, execution, checks, runtime receipts, and exact share links.

### Specs, Packages, and World

Own formal definitions, package and namespace records, and public discussion respectively. Learn references these products without absorbing their information architecture.

## Responsive and input contract

The primary task yields last:

1. lesson prose or the active practice/project surface remains primary;
2. inspectors move below the main content;
3. outlines and scenario selectors become contained horizontal lists;
4. wide tables, code, status, and event rows scroll inside labelled regions;
5. project control panes yield before the editor or Canvas;
6. progress and teaching inspectors move below the main record;
7. all narrow-screen controls retain at least a 44-pixel touch target.

Keyboard users can select entrances, search tracks, navigate course units, run and edit lessons, answer checks, select practice states, inspect project choices, and operate teaching controls. Focus remains visible. Reduced motion removes decorative displacement without removing state feedback.

## Fixture contract

`site/src/lib/v2-learn.mjs` contains deterministic design-review data. It deliberately covers:

- all three experience entrances;
- six outcome tracks;
- anonymous, new-account, and returning learner states;
- complete, current, locked, and optional course units;
- lesson runtime, stale, and unavailable states;
- seven practice states;
- project files, capabilities, milestones, and handoffs;
- meaningful progress and privacy controls;
- authoring, concept-registry, migration, and machine-format states.

Fixture identities, dates, revisions, attempts, completion claims, and progress must not be marketed as current production data.

## Adoption checklist

Before adopting this laboratory into `learn.hara-lang.org`:

1. pin a merged Visual Language revision;
2. bind every lesson, concept, exercise, project, and progress view to exact canonical identities and revisions;
3. allow anonymous first execution;
4. keep Run free of editor-focus side effects;
5. keep local pass distinct from server-verified completion;
6. keep runtime unavailable distinct from exercise failure;
7. preserve historical attempts when curriculum versions change;
8. keep progress private by default and separate from World reputation;
9. use shared Playground and EnvironmentWorkbench contracts instead of copying editor geometry;
10. validate keyboard, touch, light, dark, zoom/reflow, narrow widths, and reduced motion.

## Verification contract

The implementation keeps focused tests for:

- `hara.learn@2.0.0` content-type consumption;
- unique fixture identities and exact revisions;
- all entrance, track, learner, unit, practice, project, progress, teaching, and degraded states;
- deterministic track filtering and next-unit selection;
- landing, course, lesson, practice, project, progress, teaching, World-boundary, and adoption structure;
- shared `Shell`, `EnvironmentWorkbench`, and Playground contract reuse;
- no sign-in gate before first execution;
- no editor autofocus or Run-path focus call;
- keyboard markers, focus-visible treatment, contained overflow, 44-pixel touch controls, responsive breakpoints, and reduced motion;
- absence of protected `--hara-*` token redefinitions;
- package inclusion of this document;
- repository-wide `npm test` and `npm run site:build` on the exact pull-request head.
