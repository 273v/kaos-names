"""Tests for name generation."""

from __future__ import annotations

import random
import re

import pytest

from kaos_names import (
    DEFAULT_DESCRIPTORS,
    DEFAULT_NOUNS,
    generate_combination,
    generate_name,
    generate_session_name,
)


def test_generate_name_matches_default_shape() -> None:
    name = generate_name(rng=random.Random(273))

    assert re.fullmatch(r"[a-z]+-[a-z]+-\d{2}", name)


def test_generate_name_uses_packaged_vocabulary() -> None:
    name = generate_name(rng=random.Random(1))
    descriptor, noun, suffix = name.rsplit("-", maxsplit=2)

    assert descriptor in DEFAULT_DESCRIPTORS
    assert noun in DEFAULT_NOUNS
    assert 1 <= int(suffix) <= 99


def test_default_vocabulary_is_large_unique_and_slug_safe() -> None:
    assert len(DEFAULT_DESCRIPTORS) >= 100
    assert len(DEFAULT_NOUNS) >= 300
    assert len(DEFAULT_DESCRIPTORS) == len(set(DEFAULT_DESCRIPTORS))
    assert len(DEFAULT_NOUNS) == len(set(DEFAULT_NOUNS))
    assert all(re.fullmatch(r"[a-z]+", descriptor) for descriptor in DEFAULT_DESCRIPTORS)
    assert all(re.fullmatch(r"[a-z]+", noun) for noun in DEFAULT_NOUNS)


def test_default_nouns_avoid_negative_or_obscure_terms() -> None:
    """Names get attached to people in the KAOS web app — keep the vocabulary
    friendly and recognizable. Excludes both pejorative crime terms and
    obscure feudal vocabulary that no one will recognize."""
    excluded_terms = {
        # Pejorative or crime-implying labels
        "absconding",
        "abettor",
        "amercement",
        "barratry",
        "calumny",
        "deforcement",
        "embezzlement",
        "felony",
        "garnishee",
        "garnishment",
        "kidnap",
        "kleptomania",
        "knave",
        "larceny",
        "libel",
        "manslaughter",
        "misdemeanor",
        "mortmain",
        "negligence",
        "nuisance",
        "ouster",
        "perjury",
        "purpresture",
        "slander",
        "trespass",
        "unlaw",
        "wergild",
        "wreck",
        # Obscure / feudal / non-legal noise
        "advowson",
        "byline",
        "chirograph",
        "cognovit",
        "dacion",
        "deafforest",
        "detinue",
        "ealdorman",
        "emblements",
        "enfeoffment",
        "feoffee",
        "feoffment",
        "feoffor",
        "gabelle",
        "gavelkind",
        "glebe",
        "gleaning",
        "guild",
        "hereditament",
        "heritage",
        "hotchpot",
        "hue",
        "hypothec",
        "indentation",
        "infangthef",
        "inquisition",
        "interlocutor",
        "jailer",
        "juramentum",
        "kalendar",
        "kalends",
        "keyage",
        "knight",
        "libellant",
        "mainprise",
        "mesne",
        "mittimus",
        "narratio",
        "notarius",
        "nuncupate",
        "obligor",
        "oyer",
        "paction",
        "pandects",
        "pannage",
        "praecipe",
        "querela",
        "quitrent",
        "quittance",
        "quodlibet",
        "revivor",
        "sacramentum",
        "scutage",
        "serjeant",
        "socage",
        "tailzie",
        "tallage",
        "tanistry",
        "umpirage",
        "usucaption",
        "vassal",
        "vavasour",
        "villenage",
        "viscount",
        "wapentake",
        "xenodochium",
        "yard",
        "year",
        "yarn",
        "yeoman",
        "yule",
        "zanja",
        "zanjero",
        "zeal",
        "zemindar",
    }

    assert set(DEFAULT_NOUNS).isdisjoint(excluded_terms)


def test_default_descriptors_avoid_negative_tone() -> None:
    """Descriptors get prefixed onto attorney/judge handles — keep them upbeat."""
    excluded_descriptors = {
        "blurry",
        "boring",
        "clumsy",
        "cold",
        "cranky",
        "creepy",
        "dim",
        "dingy",
        "dizzy",
        "drab",
        "dreary",
        "dull",
        "flimsy",
        "fleeting",
        "gloomy",
        "grim",
        "grumpy",
        "hurried",
        "lazy",
        "mopey",
        "muted",
        "prickly",
        "sad",
        "shoddy",
        "silent",
        "slow",
        "sloppy",
        "sluggish",
        "stale",
        "stinky",
        "stuffy",
        "tired",
        "wobbly",
        "wonky",
    }

    assert set(DEFAULT_DESCRIPTORS).isdisjoint(excluded_descriptors)


def test_generate_name_is_deterministic_with_seeded_random() -> None:
    first = generate_name(rng=random.Random(273))
    second = generate_name(rng=random.Random(273))

    assert first == second


def test_generate_name_supports_custom_vocabulary_and_padding() -> None:
    name = generate_name(
        descriptors=("kind",),
        nouns=("brief",),
        rng=random.Random(1),
        number_min=7,
        number_max=7,
        number_width=3,
    )

    assert name == "kind-brief-007"


def test_generate_name_supports_custom_separator() -> None:
    name = generate_name(
        descriptors=("sunny",),
        nouns=("docket",),
        rng=random.Random(1),
        separator="_",
        number_min=2,
        number_max=2,
    )

    assert name == "sunny_docket_02"


def test_generate_session_name_aliases_generator() -> None:
    name = generate_session_name(rng=random.Random(273))

    assert name == generate_name(rng=random.Random(273))


def test_generate_combination_preserves_kelvin_helper_shape() -> None:
    name = generate_combination()

    assert re.fullmatch(r"[a-z]+-[a-z]+-\d{2}", name)


def test_generate_combination_respects_global_random_seed() -> None:
    random.seed(273)
    first = generate_combination()
    random.seed(273)
    second = generate_combination()

    assert first == second


def test_generate_name_rejects_empty_descriptors() -> None:
    with pytest.raises(ValueError, match="descriptors must contain at least one word"):
        generate_name(descriptors=())


def test_generate_name_rejects_empty_nouns() -> None:
    with pytest.raises(ValueError, match="nouns must contain at least one word"):
        generate_name(nouns=())


def test_generate_name_rejects_empty_separator() -> None:
    with pytest.raises(ValueError, match="separator must not be empty"):
        generate_name(separator="")


def test_generate_name_rejects_invalid_number_range() -> None:
    with pytest.raises(ValueError, match="number_min must be less than or equal"):
        generate_name(number_min=10, number_max=1)


def test_generate_name_rejects_invalid_number_width() -> None:
    with pytest.raises(ValueError, match="number_width must be at least 1"):
        generate_name(number_width=0)
