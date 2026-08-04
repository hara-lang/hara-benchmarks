# Hoplite submission for The Benchmarker

This directory mirrors the files intended for `lua/hoplite/` in `the-benchmarker/web-frameworks`.

Before opening the upstream pull request:

1. replace `ghcr.io/greenways-ai/hoplite:latest` with an immutable release tag;
2. run the three compatibility checks below against port 3000;
3. run the upstream framework target locally; and
4. add Hoplite to the upstream Makefile, `neph.yaml` and framework registry as required by that project.

```sh
curl -i http://127.0.0.1:3000/
curl -i http://127.0.0.1:3000/user/42
curl -i -X POST http://127.0.0.1:3000/user
```

Expected bodies are empty, `42`, and empty respectively. Hoplite currently exposes the matched path rather than a `:path-params` map, so the handler extracts the identifier from `:path`.
