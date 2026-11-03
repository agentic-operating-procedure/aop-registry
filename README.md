# AOP Registry

`aop-registry` is the single authority for the versioned catalogue of published AOPs: publication, resolution, and the provenance chain from a published AOP back to the observed cases it was compiled from.

| Field | Value |
|---|---|
| Authority | The catalogue: publication, versioning, provenance chains, discovery |
| Tier | Registry |
| Landing wave | 4 |
| Version | 0.1.0 |
| Status | Stable |
| Licence | MIT |

## What this repository owns

- Publication: an AOP version is published immutably, with a content digest, lifecycle status, and its provenance block.
- Resolution: a ref (`domain/AP-ID@vX.Y.Z`, harness refs with `HR-`) resolves to its entry.
- Provenance chains: the chain from a published version back to the observed cases is verified against the case corpus, per NM-PRV-4. This is what makes the programme's claims falsifiable: anyone can pull a published AOP and check where it came from.

## What this repository does not own

- The content of the AOPs it catalogues. That is `aop-spec` and the domain.
- The identifier and versioning scheme. That is `aop-spec`.
- The conformance verdict on what it publishes. That is `aop-conformance`.

## Running

```
python3 -m aop_registry publish <aop.json> --root <registry-root>
python3 -m aop_registry resolve <ref> --root <registry-root>
python3 -m aop_registry verify <ref> --root <registry-root> --cases <cases.jsonl>
```

The Phase 4 end-to-end gate in `aop-reference-harness` exercises publish, resolve and verify against the fixture corpus.
