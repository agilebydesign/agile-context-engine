"""
Reorganize Excel story map into hierarchical markdown for agent memory.

Parses spread structure: Epic (Category) -> Capability -> System -> Notes
Outputs one markdown file per Epic with ## Capability, ### System, - notes.

Usage:
  python organize_story_map_hierarchy.py --memory <memory_name> [--source <xlsx_path>]
  python organize_story_map_hierarchy.py --memory context

If --source omitted, looks for .xlsx in the original source folder.
Requires: pip install pandas openpyxl
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

import os

ROOT = Path(os.environ["CONTENT_MEMORY_ROOT"]) if "CONTENT_MEMORY_ROOT" in os.environ else Path.cwd()
MEMORY = ROOT / "memory"


def _sanitize_filename(s: str) -> str:
    """Sanitize string for use as filename."""
    s = re.sub(r'[<>:"/\\|?*]', "_", str(s))
    return s.strip() or "untitled"


def _is_valid(val) -> bool:
    """Check if value is non-null and non-empty after strip."""
    if val is None or (isinstance(val, float) and (val != val or val == 0)):
        return False
    s = str(val).strip()
    return len(s) > 0 and s.lower() not in ("nan", "none")


def parse_story_map_xlsx(xlsx_path: Path) -> dict:
    """
    Parse Excel story map into hierarchy: epic -> capability -> system -> [notes].
    Returns: {epic: {capability: {system: [notes]}}}
    """
    import pandas as pd
    df = pd.read_excel(xlsx_path, header=None)

    # Row indices
    ROW_CATEGORY = 0   # Epic
    ROW_CAPABILITY = 2
    ROW_SYSTEM = 3
    ROW_NOTES_START = 4

    # Forward-fill category (epic) across columns
    categories = []
    for c in range(df.shape[1]):
        val = df.iloc[ROW_CATEGORY, c]
        if _is_valid(val) and str(val).strip().lower() != "category":
            categories.append(str(val).strip())
        else:
            categories.append(categories[-1] if categories else "Unknown")

    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for col in range(1, df.shape[1]):  # Skip first column (labels)
        epic = categories[col]
        capability = df.iloc[ROW_CAPABILITY, col]
        system = df.iloc[ROW_SYSTEM, col]

        if not _is_valid(capability):
            capability = "Other"
        else:
            capability = str(capability).strip()

        if not _is_valid(system):
            system = "Other"
        else:
            system = str(system).strip()

        notes = []
        for row in range(ROW_NOTES_START, df.shape[0]):
            val = df.iloc[row, col]
            if _is_valid(val):
                text = str(val).strip()
                for line in text.split("\n"):
                    line = line.strip()
                    if line:
                        notes.append(line)

        if notes or capability != "Other" or system != "Other":
            hierarchy[epic][capability][system].extend(notes)

    return dict(hierarchy)


def write_hierarchical_markdown(hierarchy: dict, out_dir: Path, source_ref: str) -> int:
    """Write one markdown file per epic. Returns count of files written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for epic, capabilities in sorted(hierarchy.items()):
        if not capabilities:
            continue

        lines = [
            f"<!-- Source: {source_ref} -->",
            "",
            f"# {epic}",
            "",
        ]

        for capability, systems in sorted(capabilities.items()):
            lines.append(f"## {capability}")
            lines.append("")

            for system, notes in sorted(systems.items()):
                lines.append(f"### {system}")
                lines.append("")

                for note in notes:
                    lines.append(f"- {note}")
                lines.append("")

        filename = _sanitize_filename(epic) + ".md"
        out_path = out_dir / filename
        out_path.write_text("\n".join(lines), encoding="utf-8")
        count += 1

    return count


def _run_memory_mode(memory_name: str, source_path: str | None = None) -> None:
    memory_root = MEMORY / memory_name
    if not memory_root.exists():
        print(f"Memory not found: {memory_root}")
        return

    # Find xlsx source
    if source_path:
        xlsx = Path(source_path)
        if not xlsx.is_absolute():
            xlsx = ROOT / source_path
    else:
        # Prefer memory-name-based paths (e.g. context -> global-sco/context)
        candidates = [
            ROOT / "global-sco" / memory_name / "stroy Map.xlsx",
            ROOT / "global-sco" / memory_name / "story Map.xlsx",
        ]
        xlsx = next((p for p in candidates if p.exists()), None)
        if not xlsx:
            xlsx_files = [f for f in ROOT.rglob("*.xlsx") if "~$" not in f.name]
            xlsx = next((f for f in xlsx_files if memory_name in str(f)), None)
        if not xlsx:
            print("No .xlsx found. Use --source <path>")
            return

    if not xlsx.exists():
        print(f"Source not found: {xlsx}")
        return

    chunked_dir = memory_root / "chunked"
    chunked_dir.mkdir(parents=True, exist_ok=True)

    print(f"Parsing {xlsx.name} ...")
    hierarchy = parse_story_map_xlsx(xlsx)

    source_ref = str(xlsx.relative_to(ROOT)) if ROOT in xlsx.parents else str(xlsx)
    n = write_hierarchical_markdown(hierarchy, chunked_dir, source_ref)
    print(f"Wrote {n} hierarchical markdown files to {chunked_dir}/")


def main():
    args = sys.argv[1:]
    mem_idx = next((i for i, a in enumerate(args) if a == "--memory"), None)
    src_idx = next((i for i, a in enumerate(args) if a == "--source"), None)

    if mem_idx is None or mem_idx + 1 >= len(args):
        print("Usage: python organize_story_map_hierarchy.py --memory <memory_name> [--source <xlsx_path>]")
        return

    memory_name = args[mem_idx + 1]
    source_path = args[src_idx + 1] if src_idx is not None and src_idx + 1 < len(args) else None

    try:
        import pandas as pd  # noqa: F401
    except ImportError:
        print("Missing dependency. Run: pip install pandas openpyxl")
        sys.exit(1)

    _run_memory_mode(memory_name, source_path)


if __name__ == "__main__":
    main()
