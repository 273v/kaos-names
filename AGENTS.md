# Agent Guidance

## Scope

This file is the canonical repository-local instruction file for coding
agents working in this repository. It applies to the whole repository.

Make changes that are small, public-repo appropriate, and consistent with:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Python design and architecture](docs/standards/python-design-and-architecture.md)
- [Code quality standards](docs/standards/code-quality-standards.md)
- [Engineering process](docs/standards/engineering-process.md)
- [Tests, fixtures, and CI](docs/standards/tests-fixtures-ci.md)

## Project Identity

`kaos-names` is the distribution name. `kaos_names` is the import package.
The package is a pure-Python, dependency-free friendly legal-flavored name
generator with a small public API and the `kaos-names` CLI.

Treat these as user-facing contracts:

- exported names in `kaos_names.__all__`
- documented generator behavior and vocabulary semantics
- CLI commands, flags, exit behavior, and `--json` output
- package metadata and wheel contents

## Setup

Use Python 3.13 or newer and `uv` for local development:

```bash
uv sync --group dev
```

Do not add runtime dependencies unless they are necessary, well licensed,
and justified by the package's tiny utility scope.

## Local Checks

Use the same practical quality gate as contributors and CI:

```bash
uv run ruff format --check kaos_names tests
uv run ruff check kaos_names tests
uv run ty check kaos_names tests
uv run pytest -m "not live and not network and not slow" --no-cov
```

This repository uses `ruff`, `ty`, and `pytest`. Type checking uses `ty`,
not mypy; use `# ty: ignore[...]` only for narrow, justified exceptions.

When packaging, metadata, README rendering, or release behavior changes,
also run:

```bash
uv build
uvx --from twine twine check --strict dist/*
```

## Architecture Rules

Keep the package simple and deterministic:

- Preserve the pure-Python package shape and `py.typed` typed-package marker.
- Keep import-time behavior cheap: no network, filesystem scans, logging setup,
  or expensive initialization.
- Keep the top-level API small, typed, and explicitly exported.
- Use keyword-only options for generator knobs when expanding public helpers.
- Keep CLI output stable and machine-readable JSON schemas predictable.
- Prefer explicit validation errors over surprising coercion or traceback-heavy
  user-facing failures.

## Name Processing

Name generation and any future normalization, parsing, or matching helpers must
be deterministic and easy to test.

- Preserve deterministic behavior when callers pass a seeded `random.Random`.
- Keep generated default names slug-safe, friendly, recognizable, and stable in
  shape unless a documented compatibility change is intentional.
- Be explicit about Unicode, case folding, and locale behavior. Do not rely on
  process locale or platform-dependent casing rules for public behavior.
- If parsing or matching names is added, normalize at boundaries and test
  equivalent inputs, rejected inputs, and round-trip behavior.
- Use realistic fixtures for edge cases, but keep fixtures small,
  redistributable, documented, and free of secrets or personal data.
- Do not commit large corpora or data with unknown, non-commercial,
  no-derivatives, GPL, or AGPL licensing.

## Testing

Add or update tests whenever behavior changes. Public API changes need tests
through the public entry point. CLI behavior changes need CLI tests, including
JSON output when applicable.

Keep tests deterministic. Unit tests must not require network access,
credentials, local services, wall-clock sleeps, or large downloads.

## Security

Follow [SECURITY.md](SECURITY.md) for vulnerability handling. Never commit
secrets, credentials, private keys, `.env` files, customer data, or privileged
content. Redact sensitive values from errors, logs, JSON output, and test
fixtures.

Validate untrusted input before using it in paths, subprocesses, serialization,
or output formats. Keep failure modes bounded and predictable.

## Commits, PRs, And Releases

Use focused conventional commits and sign them with `git commit -s`. Keep PRs
to one logical change and include the commands used for verification.

Before committing, fetch `origin` and rebase on `main` if needed. Do not move
public tags. Do not force-push unless a maintainer explicitly asks for it.

Public API, CLI behavior, JSON/schema output, package metadata, security
behavior, fixture, or release-process changes usually need documentation and a
`CHANGELOG.md` entry. Releases require the full release gate described in the
standards.
