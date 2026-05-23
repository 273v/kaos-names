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

### Fixed

- **Release SBOM now describes the runtime install, not the dev env.**
  `.github/workflows/release.yml` previously ran
  `cyclonedx-py environment .venv` after `uv sync --group dev`,
  publishing a CycloneDX SBOM whose `components` array listed pytest,
  ruff, ty, coverage, pluggy, packaging, iniconfig, Pygments, and
  pytest-cov as dependencies of `kaos-names` — a zero-dep leaf package
  per `pyproject.toml`. The SBOM is now generated from the existing
  `/tmp/smoke` clean runtime venv (built by the smoke-test step from
  the wheel with no dev group), so it reflects what `pip install
  kaos-names` actually pulls.

  Added a runtime-honesty assertion in the workflow: for this
  `dependencies = []` package the SBOM components array must contain
  only the package itself plus pip install plumbing
  (`pip`/`setuptools`/`wheel`). Anything else (test/type/lint tooling)
  fails the release build. Closes audit-04/kaos-names.md F-001.

  Note: the existing `v0.1.0a2` SBOM asset on GitHub Releases remains
  the contaminated artifact. Re-cut or replace it manually if the
  project treats Release SBOMs as authoritative compliance artifacts;
  per audit-04's "re-cut or replace" recommendation.

### Tests

- **audit-04 F-003 contract drift pins.** Added
  `tests/unit/test_contract_drift_pins.py` (6 tests) pinning every
  README-visible exact number and CLI JSON envelope key set:
  - `DEFAULT_DESCRIPTORS` count == 120 (README.md:23-24)
  - `DEFAULT_NOUNS` count == 327 (README.md:23-24)
  - cartesian space == 3 884 760 (README.md:23-24)
  - `kaos_names.__all__` matches the 6-symbol documented set
    (README.md:109)
  - `generate --json` envelope key set (7 keys: command, count,
    names, separator, number_min, number_max, number_width)
  - `vocabulary --json` envelope key set (5 keys: command,
    descriptor_count, noun_count, descriptors, nouns)
  Pre-existing tests only asserted broad lower bounds (`>= 100`,
  `>= 300`); the new tests pin the exact numbers the README promises
  so vocabulary tweaks or CLI refactors fail the gate instead of
  silently making docs false. No public API or behavior change.

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
