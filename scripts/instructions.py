#!/usr/bin/env python3
"""
CLI entry point for ace-shaping instructions.
Usage: python scripts/instructions.py <operation> [--workspace PATH]
Operations: create_strategy, generate_slice, improve_strategy
Prints assembled markdown for injection into AI prompt.
"""
import argparse
import sys
from pathlib import Path

# Add repo root to path
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from src.engine import AgileContextEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="Get ace-shaping instructions for an operation")
    parser.add_argument(
        "operation",
        choices=["create_strategy", "generate_slice", "improve_strategy"],
        help="Operation to get instructions for",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace path (sets strategy_path when ace-output exists)",
    )
    args = parser.parse_args()

    engine = AgileContextEngine()
    engine.load()

    if args.workspace:
        engine.set_workspace(args.workspace)

    skill = engine.get_skill("ace-shaping")
    if not skill:
        print("Error: ace-shaping skill not found", file=sys.stderr)
        return 1

    content = skill.instructions.display_content(args.operation)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
