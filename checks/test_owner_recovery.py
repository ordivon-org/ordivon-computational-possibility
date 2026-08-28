from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OWNER = "research-owner:computational-possibility"
AUTHORITY = "authority:ordivon:research-owner:computational-possibility"


def _relative_file(value: object) -> Path:
    if not isinstance(value, str) or not value or value != value.strip():
        raise AssertionError(f"invalid relative path: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts:
        raise AssertionError(f"path escapes owner root: {value}")
    path = ROOT.joinpath(*pure.parts)
    if not path.is_file():
        raise AssertionError(f"owner recovery path is missing: {value}")
    return path


class ComputationalPossibilityOwnerRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = json.loads((ROOT / "authority" / "CURRENT.json").read_text(encoding="utf-8"))
        cls.publication_path = _relative_file(cls.current["publication"])
        cls.publication_bytes = cls.publication_path.read_bytes()
        cls.publication = json.loads(cls.publication_bytes)

    def test_current_authority_pointer_matches_publication_bytes_and_identity(self) -> None:
        observed = "sha256:" + hashlib.sha256(self.publication_bytes).hexdigest()
        self.assertEqual(self.current["schemaVersion"], 1)
        self.assertEqual(self.current["kind"], "ordivon.research-owner-current")
        self.assertEqual(self.current["ownerResearchRef"], OWNER)
        self.assertEqual(self.current["authorityRef"], AUTHORITY)
        self.assertEqual(self.current["currentAuthorityVersionRef"], observed)
        self.assertEqual(self.publication_path.stem, observed.removeprefix("sha256:"))
        self.assertEqual(self.publication["ownerResearchRef"], OWNER)
        self.assertEqual(self.publication["authorityRef"], AUTHORITY)

    def test_current_source_lineage_and_recovery_are_available(self) -> None:
        source = self.publication["source"]
        self.assertEqual(source["kind"], "git")
        revision = source["sourceRevision"]
        self.assertRegex(revision, r"^[0-9a-f]{40}$")
        if (ROOT / ".git").exists():
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        recovery = self.publication["currentRecovery"]
        self.assertEqual(recovery["targetRole"], "OWNER_RESEARCH_CORPUS")
        _relative_file(recovery["locator"])

    def test_authority_named_current_recovery_and_conformance_entries_exist(self) -> None:
        corpus = json.dumps(self.publication, ensure_ascii=False)
        for token, locator in {
            "CURRENT-RECOVERY.md": "CURRENT-RECOVERY.md",
            "RESEARCH-PRODUCTS.md": "RESEARCH-PRODUCTS.md",
            "scripts/check-applicability-artifact": "scripts/check-applicability-artifact",
        }.items():
            self.assertIn(token, corpus)
            _relative_file(locator)
        self.assertIn("result:computational-possibility:applicability-conformance-entry-current", corpus)
        self.assertIn("APPLICABILITY_CONFORMANCE_ENTRY", corpus)

    def test_historical_dogfood_does_not_masquerade_as_current_external_state(self) -> None:
        products = (ROOT / "RESEARCH-PRODUCTS.md").read_text(encoding="utf-8")
        self.assertIn("b5eae9c4abeea960d4b3f9e41e54fd07a04477a4", products)
        self.assertIn("preserved dogfood evidence", products)
        self.assertIn("must reacquire current owner-native Runtime/Interlocus evidence", products)
        self.assertNotIn("Current Harness Campaign-5 evidence", products)
        self.assertNotIn("A live 2026-08-19 observation", products)

    def test_latest_formal_carrier_dogfood_is_not_silently_promoted_into_authority(self) -> None:
        corpus = json.dumps(self.publication, ensure_ascii=False).lower()
        self.assertNotIn("z3-solver", corpus)
        self.assertNotIn("capability-substitution-formal-carrier-v0", corpus)
        self.assertTrue((ROOT / "experiments" / "capability-substitution-formal-carrier-v0" / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
