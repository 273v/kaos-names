# Changelog

All notable changes to `kaos-names` are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows Semantic Versioning while using pre-1.0 alpha releases.

## [Unreleased]

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
