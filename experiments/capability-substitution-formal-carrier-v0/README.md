# Capability Substitution Formal-Carrier Dogfood v0

## Status and truth role

This is a **bounded Computational Possibility consumer dogfood**, not a new theorem family, Foundation, capability datatype, solver dependency, service, or external-tool ownership claim.

Purpose: test whether the current CP Comparative/Transport and Applicability surfaces can consume an external formal carrier plus Runtime execution evidence without collapsing pointwise validity into history-sensitive substitutability.

## Question

Suppose a two-call provider exposes the same pointwise response relation on each call:

`output_i in {0,1}`.

The consumer slot additionally requires the history contract:

`output_1 = 0` and `output_2 = output_1 + 1`.

Does pointwise response validity alone guarantee provider substitutability for the history-sensitive slot?

CP predicts **no** unless history/selection/state semantics are preserved. The relevant existing control is:

`PointwiseValidity != HistoryValidity`.

## External formal carrier

Carrier acquisition was external to CP and did not modify CP dependencies.

- acquisition Runtime Job: `job-01a043f2-06e0-76f3-b9df-98aa3ac44258`;
- carrier: `z3-solver`;
- observed carrier version: `4.16.0`;
- formal-query Runtime Job: `job-01a043f2-4d06-7992-a68c-25d4972a6aeb`.

The formal query asks for a two-call trace such that:

- first output is `0`;
- each output is pointwise-valid in `{0,1}`;
- the second output does **not** equal the first output plus one.

Z3 returned `sat` with the exact witness:

`[0,0]`.

Therefore the pointwise relation does not entail the required history relation.

[`formal_counterexample.py`](formal_counterexample.py) preserves the small formal query used by the dogfood. It imports Z3 as an **external carrier**; CP does not add Z3 to its repository-owned requirements.

## Runtime actual witness

Runtime Job `job-01a043f2-6f17-7cc0-8526-8e1927cdf7c5` executed two concrete providers:

- `PointwiseOnlyProvider` -> `[0,0]`;
- `StatefulCounterProvider` -> `[0,1]`.

Both traces satisfy the pointwise output relation for the two observed calls. Only `[0,1]` satisfies the required increment-history contract.

[`actual_providers.py`](actual_providers.py) preserves the exact bounded provider behavior used by the Runtime witness.

## Applicability result

[`applicability-pointwise-history-witness-v1.json`](applicability-pointwise-history-witness-v1.json) records only the narrow constructive consequence:

> For the exact Runtime-observed `PointwiseOnlyProvider` target, the formal history-violating witness `[0,0]` is actually realized. Therefore pointwise response validity alone does not guarantee the required increment-history contract for this target.

The record uses constructive `formal -> actual` transport because it transports one exact formal counterexample witness into one exact actual provider trace.

It does **not** establish:

- global impossibility of satisfying the history-sensitive slot;
- failure of every provider;
- equivalence or non-equivalence of arbitrary APIs;
- a lower bound over all implementations;
- a universal stateful-capability schema;
- that Z3 owns CP theorem truth or Runtime actual truth.

The `StatefulCounterProvider -> [0,1]` observation is an explicit control showing that a provider can satisfy both the same bounded pointwise relation and the stronger history contract.

## Capability-realization consequence

This dogfood demonstrates an end-to-end role split:

`CP constitutes the transport question`
`-> external Z3 finds a formal counterexample witness`
`-> Runtime supplies actual execution evidence`
`-> CP Applicability emits a bounded consequence`.

The external solver remains an assimilated carrier in its proper role. The experiment therefore supports **capability realization by composition**, not construction of a CP-native theorem prover.
