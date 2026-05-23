# Changelog

All notable changes to `kaos-names` are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows Semantic Versioning while using pre-1.0 alpha releases.

## [Unreleased]

### Changed

- `pyproject.toml` classifier bumped from `Development Status :: 3 - Alpha`
  to `Development Status :: 5 - Production/Stable` to reflect the
  0.1.0 GA release (WU-L #543) that froze the public API for the
  0.1.x line. Closes audit-04/kaos-names.md Family D (classifier drift).


## [0.1.0a2] — 2026-05-18

### Security

- **bandit + vulture now run in both pre-commit and CI.** The
  ``.pre-commit-config.yaml`` gains two new hooks (bandit static
  security scan + vulture dead-code scan), mirrored by jobs in
  ``security.yml`` so the scan is publicly visible on every PR.
  Bandit skip list is justified inline per audit
  (``B101,B404,B603,B607``); vulture runs at ``--min-confidence
  100`` with a shared ``--ignore-names`` list for framework
  callbacks / signal handlers / OAuth field names that vulture
  can't infer from the import graph alone. Both hooks currently
  pass clean. Mirrors the rollout pattern from kaos-core.

### Changed

- **CI / supply-chain hardening pass.** Workflow actions pinned for
  public-PR hardening, CycloneDX SBOM published as a release asset,
  CODEOWNERS expansion + Dependabot + OpenSSF Scorecard wired up,
  macOS-arm64 + Windows-x64 test legs added, repo standards docs
  (`AGENTS.md`, `CONTRIBUTING.md`, `docs/standards/*`) landed, uv
  dependency-freshness policy aligned with the rest of kaos-*. No
  user-visible API change in this release.

## [0.1.0a1] - 2026-05-07

### Added

- Initial standalone `kaos-names` package, extracted from the Kelvin Agent
  API session-name helper and broadened for general KAOS use.
- Curated default vocabulary tuned for friendliness and recognizability:
  120 cheerful descriptors and 327 slug-safe legal terms (3,884,760 possible
  default names before random collision). Pejorative crime vocabulary,
  obscure feudal terminology, and downbeat descriptors are excluded by test.
- `generate_name()`, `generate_session_name()`, and Kelvin-compatible
  `generate_combination()` public helpers.
- `kaos-names` CLI with `generate` and `vocabulary` subcommands, plain text
  and JSON output, optional seed, custom separators, and configurable
  number range and width.
- Unit tests covering the public API plus vocabulary guards (size,
  uniqueness, slug-safety, exclusion lists).
- Apache-2.0 license, NOTICE, security policy, CI/release workflows, issue
  and pull-request templates, CODEOWNERS, dependabot config.
