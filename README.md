# kaos-names

> **Part of [Kelvin Agentic OS](https://kelvin.legal) (KAOS)** — open agentic
> infrastructure for legal work, built by
> [273 Ventures](https://273ventures.com).
> See the [full KAOS package map](https://github.com/273v) for the rest of the stack.

[![PyPI - Version](https://img.shields.io/pypi/v/kaos-names)](https://pypi.org/project/kaos-names/)
[![Python](https://img.shields.io/pypi/pyversions/kaos-names)](https://pypi.org/project/kaos-names/)
[![License](https://img.shields.io/pypi/l/kaos-names)](https://github.com/273v/kaos-names/blob/main/LICENSE)
[![quality](https://github.com/273v/kaos-names/actions/workflows/quality.yml/badge.svg)](https://github.com/273v/kaos-names/actions/workflows/quality.yml)

`kaos-names` is a tiny, dependency-free Python package that mints friendly,
legal-flavored handles such as `sunny-docket-07` for sessions, traces, demo
data, jobs, attorney/judge avatars, and short-lived agent workspaces. The
default vocabulary is curated to be memorable, easy to say out loud, and free
of pejorative or obscure terms — names show up next to real users in the KAOS
web app, so they need to feel friendly, not backhanded.

The package has **zero runtime dependencies** and only uses the Python
standard library. It exposes a stable vocabulary, a deterministic testing
hook through `random.Random`, and a CLI that emits plain text or JSON.
The default vocabulary has 120 friendly descriptors and 327 slug-safe legal
terms — **3,884,760 possible default names** before random collision.

## Install

```bash
uv add kaos-names
# or
pip install kaos-names
```

`kaos-names` requires Python **3.13** or newer and runs on Linux, macOS, and
Windows from a single pure-Python wheel.

## Quick start

```python
from kaos_names import generate_name

print(generate_name())
# e.g. "sunny-docket-07"
```

For deterministic output in tests, pass a seeded random source:

```python
import random

from kaos_names import generate_name

rng = random.Random(273)
assert generate_name(rng=rng) == generate_name(rng=random.Random(273))
```

The original Kelvin Agent API helper was named `generate_combination()`.
`kaos-names` keeps that alias so existing callers can migrate without
changing behavior:

```python
from kaos_names import generate_combination

session_name = generate_combination()
```

New code should prefer `generate_name()` or `generate_session_name()`.

## Concepts

The package is intentionally tiny — three helpers and two vocabularies.

| Concept | What it is |
|---|---|
| **`generate_name()`** | The primary entry point. Returns one `<descriptor>-<noun>-<NN>` slug. All knobs are keyword-only: `descriptors`, `nouns`, `rng`, `separator`, `number_min`, `number_max`, `number_width`. |
| **`generate_session_name()`** | Session-oriented alias for `generate_name()`. Same signature; reads naturally in code that creates sessions, traces, or short-lived workspaces. |
| **`generate_combination()`** | Backwards-compatible alias for the original Kelvin Agent API helper. No parameters; uses the packaged vocabulary and the global `random` module so existing code calling `random.seed(...)` keeps working. |
| **`DEFAULT_DESCRIPTORS`** | Tuple of 120 cheerful, slug-safe descriptors (`agile`, `bubbly`, `dapper`, `winsome`, …). Pejorative or downbeat words are excluded by test. |
| **`DEFAULT_NOUNS`** | Tuple of 327 recognizable, slug-safe legal terms (`gavel`, `docket`, `subpoena`, `chambers`, `verdict`, …). Obscure feudal vocabulary and crime-implying labels are excluded by test. |

The default output format is `<descriptor>-<noun>-<NN>`, with a two-digit
number from 01 through 99. Pass `separator`, `number_min`, `number_max`, and
`number_width` to change the shape.

## CLI

`kaos-names` ships a `kaos-names` command. Every subcommand supports `--json`
for machine-readable output:

```bash
kaos-names generate                              # one name
kaos-names generate --count 5                    # five names, one per line
kaos-names generate --count 5 --seed 273         # deterministic output
kaos-names generate --count 3 --json             # JSON envelope
kaos-names generate --separator _ --number-width 3   # sunny_docket_007 shape
kaos-names vocabulary                            # vocabulary counts
kaos-names vocabulary --list                     # full word lists
kaos-names vocabulary --json                     # vocabulary as JSON
```

You can also run the package as a module: `python -m kaos_names generate`.

## Compatibility & status

| Aspect | |
|---|---|
| **Python** | 3.13, 3.14 (informational matrix entries for 3.14t free-threaded and 3.15-dev) |
| **OS** | Linux, macOS, Windows (pure-Python wheel; no native code) |
| **Maturity** | Alpha. The public API is documented in `kaos_names.__all__` (6 symbols). |
| **Stability policy** | Pre-1.0: minor bumps may change behaviour. Vocabulary additions are non-breaking; removals or renames go through a deprecation cycle and are documented in [`CHANGELOG.md`](CHANGELOG.md). |
| **Test coverage** | Unit tests cover the public API plus vocabulary guards (size, slug-safety, exclusion lists). |
| **Type checker** | Validated with [`ty`](https://docs.astral.sh/ty/), Astral's Python type checker. |

## Companion packages

`kaos-names` is one of the packages in the
[Kelvin Agentic OS](https://kelvin.legal). The broader stack:

| Package | Layer | What it does |
|---|---|---|
| [`kaos-core`](https://github.com/273v/kaos-core) | Core | Foundational runtime, MCP-native types, registries, execution engine, VFS |
| [`kaos-content`](https://github.com/273v/kaos-content) | Core | Typed document AST: Block/Inline, provenance, views |
| [`kaos-mcp`](https://github.com/273v/kaos-mcp) | Bridge | FastMCP server, `kaos` management CLI, MCP resource templates |
| [`kaos-pdf`](https://github.com/273v/kaos-pdf) | Extraction | PDF → AST with provenance |
| [`kaos-web`](https://github.com/273v/kaos-web) | Extraction | Web extraction, browser automation, search, domain intelligence |
| [`kaos-office`](https://github.com/273v/kaos-office) | Extraction | DOCX / PPTX / XLSX readers + writers to AST |
| [`kaos-tabular`](https://github.com/273v/kaos-tabular) | Extraction | DuckDB-powered SQL analytics |
| [`kaos-source`](https://github.com/273v/kaos-source) | Data | Government + financial data connectors (Federal Register, eCFR, EDGAR, GovInfo, PACER, GLEIF) |
| [`kaos-llm-client`](https://github.com/273v/kaos-llm-client) | LLM | Multi-provider LLM transport |
| [`kaos-llm-core`](https://github.com/273v/kaos-llm-core) | LLM | Typed LLM programming (Signatures, Programs, Optimizers) |
| [`kaos-nlp-core`](https://github.com/273v/kaos-nlp-core) | Primitives (Rust) | High-performance NLP primitives |
| [`kaos-nlp-transformers`](https://github.com/273v/kaos-nlp-transformers) | ML | Dense embeddings + retrieval |
| [`kaos-graph`](https://github.com/273v/kaos-graph) | Primitives (Rust) | Graph algorithms + RDF/SPARQL |
| [`kaos-ml-core`](https://github.com/273v/kaos-ml-core) | Primitives (Rust) | Classical ML on the document AST |
| [`kaos-citations`](https://github.com/273v/kaos-citations) | Legal | Legal citation extraction, resolution, verification |
| [`kaos-agents`](https://github.com/273v/kaos-agents) | Agentic | Agent runtime, memory, recipes |
| [`kaos-reference`](https://github.com/273v/kaos-reference) | Sample | Reference module for module authors |

`kaos-names` is a leaf utility — it has no `kaos-*` dependencies and is safe
to use from any of the packages above (or anywhere outside KAOS).

## Development

```bash
git clone https://github.com/273v/kaos-names
cd kaos-names
uv sync --group dev
```

Install pre-commit hooks (recommended — they run the same checks as CI on
every commit, scoped to staged files):

```bash
uvx pre-commit install
uvx pre-commit run --all-files     # one-time full sweep
```

Manual QA commands (the same set CI runs):

```bash
uv run ruff format --check kaos_names tests
uv run ruff check kaos_names tests
uv run ty check kaos_names tests
uv run pytest -m "not live and not network and not slow"
```

## Build from source

```bash
uv build
uv pip install dist/*.whl
```

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md)
for setup, quality gates, pull request expectations, and engineering
standards. By contributing you agree to follow the
[project conduct expectations](CODE_OF_CONDUCT.md) and certify the
[Developer Certificate of Origin v1.1](https://developercertificate.org/) —
sign every commit with `git commit -s`. Please open an issue before starting
on a non-trivial change so we can align on scope.

## Security

For security issues, **please do not file a public issue**. Report privately
via [GitHub Private Vulnerability Reporting](https://github.com/273v/kaos-names/security/advisories/new)
or email **security@273ventures.com**. See [SECURITY.md](SECURITY.md) for the
full disclosure policy.

## License

Apache License 2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Copyright 2026 [273 Ventures LLC](https://273ventures.com).
Built for [kelvin.legal](https://kelvin.legal).
