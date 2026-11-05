# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is semantic: the major version changes when the publication or provenance semantics change, the minor version when substantive registry content is added, and the patch version for corrections that do not change meaning.

## [Unreleased]

## [v0.2.1] - 2026-11-05

### Added (Wave H3: CR-021)

- NM-VER-7 enforcement: publication refuses an artefact claiming operational applicability without a build attestation; entries carry the attestation.


## [v0.2.0] - 2026-11-05

### Added (Wave H2: CR-017)

- Per-scope revocation as a separate recorded decision that never mutates the historical entry; resolve() surfaces the revocation state (NM-VER-6).


## [0.1.0] - 2026-11-04

### Reference registry

- Published the catalogue: immutable, versioned publication with content digests and lifecycle status.
- Published resolution by ref, including the harness identifier form.
- Published provenance chain verification: a published version's declared observed cases are checked against the case corpus, and the source reference must resolve as a cg:// case reference (NM-PRV-4).
- Published the CLI: publish, resolve, verify.

[Unreleased]: https://github.com/agentic-operating-procedure/aop-registry/compare/v0.2.1...HEAD
[v0.2.1]: https://github.com/agentic-operating-procedure/aop-registry/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/agentic-operating-procedure/aop-registry/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/agentic-operating-procedure/aop-registry/releases/tag/v0.1.0
