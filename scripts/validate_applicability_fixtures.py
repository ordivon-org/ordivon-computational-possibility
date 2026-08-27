#!/usr/bin/env python3
"""Conformance expectation harness for the CP Applicability JSON Schema.

This file does not implement CP semantics. It delegates structural validation to the
third-party jsonschema Draft 2020-12 implementation and only checks the committed
valid/invalid fixture expectations.
"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments" / "computational-applicability-transport-v0"
SCHEMA_PATH = ARTIFACT / "computational-applicability-transport-v1.schema.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    mismatches: list[str] = []
    total = 0

    for directory, expected_valid in (("valid", True), ("invalid", False)):
        paths = sorted((ARTIFACT / "fixtures" / directory).glob("*.json"))
        for path in paths:
            total += 1
            errors = list(validator.iter_errors(load_json(path)))
            actual_valid = not errors
            status = "VALID" if actual_valid else "INVALID"
            expected = "VALID" if expected_valid else "INVALID"
            print(f"{directory:7} {path.name:56} {status:7} expected={expected}")
            if actual_valid != expected_valid:
                detail = errors[0].message if errors else "unexpectedly accepted"
                mismatches.append(f"{path}: {detail}")

    valid_count = len(list((ARTIFACT / "fixtures" / "valid").glob("*.json")))
    invalid_count = len(list((ARTIFACT / "fixtures" / "invalid").glob("*.json")))
    print(f"summary total={total} valid_fixtures={valid_count} invalid_fixtures={invalid_count} mismatches={len(mismatches)}")

    if valid_count != 5 or invalid_count != 7:
        mismatches.append(
            f"fixture cardinality drift: expected valid=5 invalid=7, got valid={valid_count} invalid={invalid_count}"
        )

    if mismatches:
        for mismatch in mismatches:
            print(f"MISMATCH: {mismatch}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
