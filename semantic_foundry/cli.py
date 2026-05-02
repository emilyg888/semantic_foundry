from __future__ import annotations

import argparse
import json
from pathlib import Path

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build, certify, discover


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "discover":
        payload = discover(source_path=args.source, use_case_path=args.use_case)
        print(json.dumps(payload, indent=2))
        return 0

    if args.command == "build":
        output_dir = build(
            BuildRequest(
                source_path=args.source,
                use_case_path=args.use_case,
                output_root=args.output_root,
                target=args.target,
            )
        )
        print(output_dir)
        return 0

    if args.command == "certify":
        payload = certify(args.package)
        print(json.dumps(payload, indent=2))
        return 0

    parser.error("A subcommand is required")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="semantic-foundry")
    subparsers = parser.add_subparsers(dest="command")

    discover_parser = subparsers.add_parser("discover", help="Inspect a source folder and use case.")
    discover_parser.add_argument("--source", type=Path, required=True)
    discover_parser.add_argument("--use-case", type=Path, required=True)

    build_parser = subparsers.add_parser("build", help="Generate an MVP semantic package.")
    build_parser.add_argument("--source", type=Path, required=True)
    build_parser.add_argument("--use-case", type=Path, required=True)
    build_parser.add_argument("--target", type=str, default="generic_sql")
    build_parser.add_argument("--output-root", type=Path, default=Path("outputs"))

    certify_parser = subparsers.add_parser("certify", help="Check for required certification artefacts.")
    certify_parser.add_argument("--package", type=Path, required=True)

    return parser
