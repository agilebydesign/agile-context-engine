#!/usr/bin/env python3
"""
Build AGENTS.md for ace-build (this skill). Thin entry point — delegates to engine.
Usage: python scripts/build.py
"""
import sys
from pathlib import Path

# Add engine to path
_script_dir = Path(__file__).resolve().parent
_skill_dir = _script_dir.parent  # skills/ace-build
_engine_root = _skill_dir.parent.parent  # skills -> repo root
if str(_engine_root) not in sys.path:
    sys.path.insert(0, str(_engine_root))

from src.engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_engine_root)
    print(f"Wrote {out}")
