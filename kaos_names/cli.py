"""CLI entry point for kaos-names."""

from __future__ import annotations

import argparse
import json
import random
import sys

from kaos_names.names import DEFAULT_DESCRIPTORS, DEFAULT_NOUNS, generate_name


def main(argv: list[str] | None = None) -> None:
    """Entry point for the kaos-names CLI."""
    parser = argparse.ArgumentParser(
        prog="kaos-names",
        description="Generate friendly legal-flavored names for KAOS sessions and agents",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    generate_parser = subparsers.add_parser("generate", help="Generate names")
    generate_parser.add_argument("--count", type=int, default=1, help="Number of names to emit")
    generate_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for deterministic output",
    )
    generate_parser.add_argument("--separator", default="-", help="Separator between name parts")
    generate_parser.add_argument(
        "--number-min", type=int, default=1, help="Minimum numeric suffix value"
    )
    generate_parser.add_argument(
        "--number-max", type=int, default=99, help="Maximum numeric suffix value"
    )
    generate_parser.add_argument(
        "--number-width", type=int, default=2, help="Minimum width for the numeric suffix"
    )
    generate_parser.add_argument(
        "--json", action="store_true", dest="json_output", help="JSON output"
    )

    vocabulary_parser = subparsers.add_parser("vocabulary", help="Show packaged vocabulary")
    vocabulary_parser.add_argument("--list", action="store_true", dest="list_words")
    vocabulary_parser.add_argument(
        "--json", action="store_true", dest="json_output", help="JSON output"
    )

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        raise SystemExit(1)
    if args.command == "generate":
        _cmd_generate(args)
        return
    if args.command == "vocabulary":
        _cmd_vocabulary(args)
        return

    _error(f"unknown command: {args.command}")


def _cmd_generate(args: argparse.Namespace) -> None:
    if args.count < 1:
        _error("count must be at least 1")

    rng = random.Random(args.seed) if args.seed is not None else None
    names: list[str] = []
    try:
        for _ in range(args.count):
            names.append(
                generate_name(
                    rng=rng,
                    separator=args.separator,
                    number_min=args.number_min,
                    number_max=args.number_max,
                    number_width=args.number_width,
                )
            )
    except ValueError as exc:
        _error(str(exc))

    if args.json_output:
        print(
            json.dumps(
                {
                    "command": "generate",
                    "count": len(names),
                    "names": names,
                    "separator": args.separator,
                    "number_min": args.number_min,
                    "number_max": args.number_max,
                    "number_width": args.number_width,
                },
                indent=2,
            )
        )
        return

    for name in names:
        print(name)


def _cmd_vocabulary(args: argparse.Namespace) -> None:
    descriptors = list(DEFAULT_DESCRIPTORS)
    nouns = list(DEFAULT_NOUNS)
    if args.json_output:
        print(
            json.dumps(
                {
                    "command": "vocabulary",
                    "descriptor_count": len(descriptors),
                    "noun_count": len(nouns),
                    "descriptors": descriptors,
                    "nouns": nouns,
                },
                indent=2,
            )
        )
        return

    print(f"Descriptors: {len(descriptors)}")
    print(f"Nouns: {len(nouns)}")
    if args.list_words:
        print()
        print("Descriptors:")
        print(", ".join(descriptors))
        print()
        print("Nouns:")
        print(", ".join(nouns))


def _error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)
