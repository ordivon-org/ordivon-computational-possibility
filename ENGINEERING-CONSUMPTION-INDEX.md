> **Modification notice (Apache-2.0 §4(b)):** This file contains changes from an Apache-2.0-licensed upstream version in `ordivon-computing`.

# Computational Possibility Engineering Consumption Index

Earned engineering consumption is intentionally thin and is subordinate to the project-level [Applicability / Theorem Transport Subsystem](APPLICABILITY-SUBSYSTEM.md).

## Committed baseline artifact

[`experiments/computational-applicability-transport-v0/`](experiments/computational-applicability-transport-v0/)

Canonical components:

- [`SPEC.md`](experiments/computational-applicability-transport-v0/SPEC.md) — normative derived engineering specification;
- [`computational-applicability-transport-v1.schema.json`](experiments/computational-applicability-transport-v0/computational-applicability-transport-v1.schema.json) — JSON Schema Draft 2020-12 structural schema;
- `fixtures/valid/` — 5 intended-valid examples;
- `fixtures/invalid/` — 7 intended-invalid deletion/direction/quantitative examples.

The artifact entered canonical Computing history at commit:

`1a9cc7b3a9144751b6f3d38650f42f0ea7340148`.

## Repository-owned conformance entry

Current consumer pressure has earned one small reproducibility improvement without changing the artifact's semantic role:

```bash
scripts/check-applicability-artifact
```

The script is an environment/conformance wrapper around the ordinary third-party Python `jsonschema` Draft 2020-12 implementation. If `jsonschema` is not already importable, it creates a temporary virtual environment outside the repository and installs the bounded dependency declared in `requirements-validation.txt`. It then runs `scripts/validate_applicability_fixtures.py` over the committed schema and fixtures.

The expected conformance set is:

- 5/5 files under `fixtures/valid/` validate structurally;
- 7/7 files under `fixtures/invalid/` are rejected structurally.

This is **not** a bespoke semantic validator. The repository-owned Python file is only a fixture expectation harness around a standard validator implementation.

## Truth boundary

The artifact is derived instrumentation, not a Foundation, theorem engine, owner-state cache, production gate, registry, service, or automatic currentness system.

Permanent boundaries:

- `SchemaValid != TheoremTrue`;
- `SchemaValid != PremisesTrue`;
- `SchemaValid != SemanticPreservationTrue`;
- `APPLIES != ProductionReady`;
- `APPLIES != Authorized`.

Owner-authoritative facts remain referenced with scope/currentness. They are never copied into timeless Computational Possibility truth.

## Validation boundary

The current artifact supports declarative structural conformance only. No bespoke validator is part of the earned baseline.

The new repository-owned command only makes the already-earned Draft 2020-12 conformance contract reproducible from a cold checkout. It does not validate theorem truth, semantic preservation, current owner premises, authorization, measurement semantics or actual realization.

## Not earned

Without a concrete consumer falsifier, do not expand this artifact into:

- semantic validator/service/database;
- MCP surface;
- global applicability registry;
- theorem engine;
- automatic premise/currentness refresher;
- production admission/authority gate;
- transport-composition graph.
