#!/usr/bin/env python3
"""
Scaffold a new ace-skill. Thin entry point — delegates to engine.
Usage: python scripts/scaffold.py --name ace-foo [--path skills/ace-foo]
"""
import argparse
import sys
from pathlib import Path

# Add engine to path
_script_dir = Path(__file__).resolve().parent
_ace_build_dir = _script_dir.parent
_engine_root = _ace_build_dir.parent.parent  # skills/ace-scale-build -> skills -> repo root
if str(_engine_root) not in sys.path:
    sys.path.insert(0, str(_engine_root))

from src.engine import scaffold_skill


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new ace-skill")
    parser.add_argument("--name", required=True, help="Skill name (e.g. ace-foo)")
    parser.add_argument(
        "--path",
        default=None,
        help="Output path (default: skills/<name> relative to repo root)",
    )
    args = parser.parse_args()

    path = args.path or f"skills/{args.name}"
    result = scaffold_skill(args.name, path, engine_root=_engine_root)
    print(f"Scaffolded {args.name} at {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
