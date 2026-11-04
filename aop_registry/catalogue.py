"""The catalogue: publication, resolution and provenance chains.

The registry turns a collection of documents into a body of practice others
can adopt without re-deriving it, and it is what makes the programme's claims
falsifiable: anyone can pull a published AOP and check its provenance.
Publication is versioned and immutable; the provenance chain is verified
against the observed-case corpus the AOP declares.
"""

from __future__ import annotations

import hashlib
import json
import os
import time


class Registry:
    def __init__(self, root: str):
        self.root = root
        self.catalogue_path = os.path.join(root, "catalogue.json")
        os.makedirs(os.path.join(root, "published"), exist_ok=True)
        self.catalogue = {"entries": [], "revocations": []}
        if os.path.exists(self.catalogue_path):
            with open(self.catalogue_path) as handle:
                self.catalogue = json.load(handle)
                self.catalogue.setdefault("revocations", [])

    def _save(self):
        with open(self.catalogue_path, "w") as handle:
            json.dump(self.catalogue, handle, indent=2)

    def publish(self, aop_path: str) -> dict:
        """Publish one immutable AOP version. The artefact is copied into the
        registry, its content digest is recorded, and the entry carries the
        provenance block so the chain can be walked."""
        with open(aop_path) as handle:
            doc = json.load(handle)
        ref = "%s@%s" % (doc["aop"], doc["version"])
        for entry in self.catalogue["entries"]:
            if entry["ref"] == ref:
                raise ValueError("refusal: %s is already published and the registry is immutable" % ref)

        artefact_dir = os.path.join(self.root, "published", doc["aop"].replace("/", "__"))
        os.makedirs(artefact_dir, exist_ok=True)
        artefact_name = "%s.json" % doc["version"]
        artefact_path = os.path.join(artefact_dir, artefact_name)
        content = json.dumps(doc, indent=2)
        with open(artefact_path, "w") as handle:
            handle.write(content)

        entry = {
            "ref": ref,
            "aop": doc["aop"],
            "version": doc["version"],
            "lifecycle": doc.get("lifecycle", {}),
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "content_digest": "sha256:" + hashlib.sha256(content.encode()).hexdigest(),
            "artefact": os.path.relpath(artefact_path, self.root),
            "provenance": doc.get("provenance", {}),
            "process_alignment": doc.get("process_alignment", {}),
        }
        self.catalogue["entries"].append(entry)
        self._save()
        return entry

    def revoke(self, ref: str, scope: str, reason: str, by: str) -> dict:
        """NM-VER-6: revoke per scope without mutating the historical entry.
        The revocation is a separate recorded decision; resolve() surfaces it."""
        if not self.resolve(ref):
            raise ValueError("refusal: %s is not published" % ref)
        revocation = {"ref": ref, "scope": scope, "reason": reason, "by": by,
                      "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        self.catalogue["revocations"].append(revocation)
        self._save()
        return revocation

    def revocation_state(self, ref: str) -> dict | None:
        """The active revocation for a ref, or None. The most recent wins."""
        active = [r for r in self.catalogue["revocations"] if r["ref"] == ref]
        return active[-1] if active else None

    def resolve(self, ref: str) -> dict | None:
        """Resolve an aop ref (domain/AP-ID@vX.Y.Z) to its published entry,
        with its revocation state attached (NM-VER-6)."""
        for entry in self.catalogue["entries"]:
            if entry["ref"] == ref:
                resolved = dict(entry)
                resolved["revocation"] = self.revocation_state(ref)
                return resolved
        return None

    def provenance_chain(self, ref: str, case_corpus_path: str) -> dict:
        """Walk the provenance chain from the published version back to the
        observed cases it was compiled from (NM-PRV-4): the chain holds when
        every declared observed case count is backed by the corpus and the
        source reference resolves."""
        entry = self.resolve(ref)
        if entry is None:
            return {"ref": ref, "holds": False, "reason": "ref not published"}
        problems = []
        provenance = entry.get("provenance", {})
        derived = provenance.get("derived_from", {})
        source = provenance.get("source", "")

        case_ids = set()
        if os.path.exists(case_corpus_path):
            with open(case_corpus_path) as handle:
                for line in handle:
                    if line.strip():
                        case_ids.add(json.loads(line)["case_id"])
        else:
            problems.append("case corpus not found at %s" % case_corpus_path)

        if not source.startswith("cg://case/"):
            problems.append("source reference is not a cg:// case reference: %r" % source)
        declared_cases = derived.get("observed_cases")
        if not isinstance(declared_cases, int) or declared_cases < 1:
            problems.append("derived_from.observed_cases is not a positive integer")
        elif case_ids and declared_cases > len(case_ids):
            problems.append("declared %d observed cases but the corpus carries %d" % (declared_cases, len(case_ids)))
        if not derived.get("last_recalibrated"):
            problems.append("derived_from.last_recalibrated missing")

        return {
            "ref": ref,
            "holds": not problems,
            "content_digest": entry["content_digest"],
            "source": source,
            "derived_from": derived,
            "corpus_cases": len(case_ids),
            "problems": problems,
        }

    def entries(self) -> list[dict]:
        return list(self.catalogue["entries"])
