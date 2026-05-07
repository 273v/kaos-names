"""Tests for the kaos-names CLI."""

from __future__ import annotations

import json

import pytest

from kaos_names.cli import main


def test_generate_prints_one_name(capsys: pytest.CaptureFixture[str]) -> None:
    main(["generate", "--seed", "273"])
    captured = capsys.readouterr()

    lines = captured.out.strip().splitlines()
    assert len(lines) == 1
    assert lines[0].count("-") == 2


def test_generate_count_json(capsys: pytest.CaptureFixture[str]) -> None:
    main(["generate", "--count", "3", "--seed", "273", "--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["command"] == "generate"
    assert data["count"] == 3
    assert len(data["names"]) == 3


def test_generate_rejects_invalid_count(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["generate", "--count", "0"])
    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "count must be at least 1" in captured.err


def test_generate_rejects_invalid_number_range(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["generate", "--number-min", "99", "--number-max", "1"])
    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "number_min must be less than or equal" in captured.err


def test_vocabulary_json(capsys: pytest.CaptureFixture[str]) -> None:
    main(["vocabulary", "--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["command"] == "vocabulary"
    assert data["descriptor_count"] == len(data["descriptors"])
    assert data["noun_count"] == len(data["nouns"])


def test_no_command_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([])
    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Available commands" in captured.out
