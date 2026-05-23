"""Regression tests for audit-04 F-003: contract drift pins.

audit-04/kaos-names.md F-003 flagged that the package's documented
public contracts — the exact default vocabulary counts (120 / 327),
the cartesian-space size (3 884 760), the six-symbol `__all__`, and
the CLI `--json` envelope key sets — were not pinned by tests. Only
broad lower bounds (`>= 100`, `>= 300`) were asserted. That meant
vocabulary or JSON-shape changes could make the README's exact
numbers and key lists silently false without failing the local
gate.

These tests pin every README-visible exact number and key set so a
future vocabulary tweak or CLI-output refactor surfaces in CI rather
than in a downstream consumer's bug report.
"""

from __future__ import annotations

import json
import subprocess
import sys

import kaos_names
from kaos_names import DEFAULT_DESCRIPTORS, DEFAULT_NOUNS


def test_default_descriptor_count_matches_readme() -> None:
    """README.md:23-24 says 120 descriptors. Pin the exact number."""
    assert len(DEFAULT_DESCRIPTORS) == 120, (
        "audit-04 F-003 regression: DEFAULT_DESCRIPTORS count drifted "
        f"from the documented 120 (now {len(DEFAULT_DESCRIPTORS)}). "
        "Update README.md:23-24 and CHANGELOG before changing this."
    )


def test_default_noun_count_matches_readme() -> None:
    """README.md:23-24 says 327 nouns. Pin the exact number."""
    assert len(DEFAULT_NOUNS) == 327, (
        "audit-04 F-003 regression: DEFAULT_NOUNS count drifted "
        f"from the documented 327 (now {len(DEFAULT_NOUNS)}). "
        "Update README.md:23-24 and CHANGELOG before changing this."
    )


def test_default_cartesian_space_matches_readme() -> None:
    """README.md:23-24 says 3 884 760 possible default names.

    Formula: len(DEFAULT_DESCRIPTORS) * len(DEFAULT_NOUNS) * 99
    (99 = number_max - number_min + 1 for the default 1..99 range).
    """
    cartesian = len(DEFAULT_DESCRIPTORS) * len(DEFAULT_NOUNS) * 99
    assert cartesian == 3_884_760, (
        "audit-04 F-003 regression: cartesian space drifted from the "
        f"documented 3 884 760 (now {cartesian}). Either the vocabulary "
        "counts changed (see prior tests) or the default number range "
        "did. Update README.md:23-24 and CHANGELOG before changing this."
    )


def test_dunder_all_matches_readme_six_symbol_claim() -> None:
    """README.md:109 says the public API is six symbols. Pin them."""
    expected = {
        "DEFAULT_DESCRIPTORS",
        "DEFAULT_NOUNS",
        "__version__",
        "generate_combination",
        "generate_name",
        "generate_session_name",
    }
    actual = set(kaos_names.__all__)
    assert actual == expected, (
        "audit-04 F-003 regression: kaos_names.__all__ drifted from "
        "the documented six-symbol public API.\n"
        f"  expected: {sorted(expected)}\n"
        f"  actual:   {sorted(actual)}\n"
        f"  added:    {sorted(actual - expected)}\n"
        f"  removed:  {sorted(expected - actual)}\n"
        "Update README.md:109 + CHANGELOG before changing __all__."
    )


def test_generate_json_envelope_full_key_set() -> None:
    """`kaos-names generate --json` emits the full documented envelope.

    kaos_names/cli.py:84-98 writes seven keys. Pin them so a future
    CLI refactor (rename, add, or drop a key) surfaces in CI before
    a downstream consumer's parser breaks.
    """
    result = subprocess.run(
        [sys.executable, "-m", "kaos_names", "generate", "--json", "--count", "2"],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    expected_keys = {
        "command",
        "count",
        "names",
        "separator",
        "number_min",
        "number_max",
        "number_width",
    }
    assert set(payload.keys()) == expected_keys, (
        "audit-04 F-003 regression: `generate --json` envelope keys "
        "drifted from the documented set.\n"
        f"  expected: {sorted(expected_keys)}\n"
        f"  actual:   {sorted(payload.keys())}"
    )
    # And the typed values match: `command` is the literal subcommand
    # name; `count` and `names` are int + list with consistent length.
    assert payload["command"] == "generate"
    assert isinstance(payload["count"], int)
    assert payload["count"] == 2
    assert isinstance(payload["names"], list)
    assert len(payload["names"]) == payload["count"]


def test_vocabulary_json_envelope_full_key_set() -> None:
    """`kaos-names vocabulary --json` emits the documented envelope.

    kaos_names/cli.py:108-118 writes five keys. Pin them.
    """
    result = subprocess.run(
        [sys.executable, "-m", "kaos_names", "vocabulary", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    expected_keys = {
        "command",
        "descriptor_count",
        "noun_count",
        "descriptors",
        "nouns",
    }
    assert set(payload.keys()) == expected_keys, (
        "audit-04 F-003 regression: `vocabulary --json` envelope keys "
        "drifted from the documented set.\n"
        f"  expected: {sorted(expected_keys)}\n"
        f"  actual:   {sorted(payload.keys())}"
    )
    assert payload["command"] == "vocabulary"
    # And the counts in the envelope match the underlying vocabulary
    # constants — a single source of truth tied to the README claims.
    assert payload["descriptor_count"] == len(DEFAULT_DESCRIPTORS) == 120
    assert payload["noun_count"] == len(DEFAULT_NOUNS) == 327
