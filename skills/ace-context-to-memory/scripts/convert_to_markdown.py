"""
Convert source files to markdown for agent memory.

Usage:
  python convert_to_markdown.py --memory <source_path>   # folder: all supported files
  python convert_to_markdown.py --file <file_path>      # single file only

Run from workspace root. Creates memory/<name>/*/converted/ (markdown + images).
Requires: pip install "markitdown[all]"

CRITICAL: Use --file when user asks for ONE file. Use --memory only when user
explicitly wants a folder processed. Do not process entire folders when user
specifies a single file.
"""

import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print('Missing dependency. Run: pip install "markitdown[all]"')
    sys.exit(1)

# Workspace root: cwd (run from project root) or CONTENT_MEMORY_ROOT env
import os
ROOT = Path(os.environ["CONTENT_MEMORY_ROOT"]) if "CONTENT_MEMORY_ROOT" in os.environ else Path.cwd()

MEMORY = ROOT / "memory"
ASSETS = ROOT / "Assets"

SUPPORTED = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".html", ".htm", ".txt", ".csv", ".json", ".xml",
}

_md = MarkItDown()


def convert_one(src: Path, out_dir: Path, source_ref: bool = True) -> Path:
    """Convert one file to markdown. Returns output path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    img_sub = f"images/{src.stem}"
    img_dir = out_dir / "images" / src.stem

    text = _md.convert(str(src)).text_content

    if source_ref:
        try:
            rel = src.relative_to(ROOT)
            url = (ROOT / rel).as_uri()
            text = f"<!-- Source: {rel.as_posix()} | {url} -->\n\n" + text
        except (ValueError, OSError):
            pass

    out = out_dir / (src.stem + ".md")
    out.write_text(text, encoding="utf-8")
    return out


def _run_file_mode(file_path: str) -> None:
    """Convert a single file to markdown. Only processes that file."""
    p = Path(file_path)
    if not p.is_absolute():
        for base in (ASSETS, ROOT):
            candidate = base / file_path
            if candidate.is_file():
                p = candidate
                break
    if not p.is_file():
        print(f"File not found: {file_path}")
        return
    if p.suffix.lower() not in SUPPORTED:
        print(f"Unsupported format: {p.suffix}. Supported: {sorted(SUPPORTED)}")
        return

    memory_name = p.stem or "memory"  # subfolder named after the file
    rel_parent = Path(".")
    out_root = MEMORY / memory_name
    converted_dir = out_root / rel_parent / "converted"
    chunked_dir = out_root / rel_parent / "chunked"
    converted_dir.mkdir(parents=True, exist_ok=True)
    chunked_dir.mkdir(parents=True, exist_ok=True)

    print(f"File: {p.name} -> memory/{memory_name}/converted/\n")
    try:
        out = convert_one(p, converted_dir)
        kb = out.stat().st_size // 1024
        print(f"Done: 1 file converted ({kb} KB)")
    except (Exception, BaseException) as e:
        print(f"FAIL  {type(e).__name__}: {e}")


def _run_memory_mode(memory_path: str) -> None:
    """Convert folder to memory/<name>/ preserving structure."""
    p = Path(memory_path)
    if p.is_absolute():
        src_full = p
    else:
        # Try under Assets first (abd_content style), then ROOT
        under_assets = ASSETS / memory_path
        under_root = ROOT / memory_path
        if under_assets.exists():
            src_full = under_assets
        elif under_root.exists():
            src_full = under_root
        else:
            print(f"Path not found: {memory_path}")
            return

    memory_name = src_full.name
    out_root = MEMORY / memory_name

    files = sorted(
        f for f in src_full.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED
    )
    if not files:
        print(f"No supported files in {src_full}")
        return

    print(f"Memory: {memory_name}  ({len(files)} files) -> {out_root}/\n")

    ok, fail = [], []
    for i, f in enumerate(files, 1):
        rel_parent = f.parent.relative_to(src_full)
        converted_dir = out_root / rel_parent / "converted"
        chunked_dir = out_root / rel_parent / "chunked"
        converted_dir.mkdir(parents=True, exist_ok=True)
        chunked_dir.mkdir(parents=True, exist_ok=True)

        label = str(rel_parent / f.name) if rel_parent != Path(".") else f.name
        print(f"  [{i}/{len(files)}] {label} ... ", end="", flush=True)
        try:
            out = convert_one(f, converted_dir)
            kb = out.stat().st_size // 1024
            print(f"OK  ({kb} KB)")
            ok.append(label)
        except (Exception, BaseException) as e:
            print(f"FAIL  {type(e).__name__}: {e}")
            fail.append((label, str(e)))

    print(f"\nDone: {len(ok)} converted, {len(fail)} failed.")
    if fail:
        for n, e in fail:
            print(f"  {n}: {e}")


def main():
    file_idx = next((i for i, a in enumerate(sys.argv) if a == "--file"), None)
    if file_idx is not None and file_idx + 1 < len(sys.argv):
        _run_file_mode(sys.argv[file_idx + 1])
        return

    memory_idx = next((i for i, a in enumerate(sys.argv) if a == "--memory"), None)
    if memory_idx is not None and memory_idx + 1 < len(sys.argv):
        _run_memory_mode(sys.argv[memory_idx + 1])
        return

    print("Usage:")
    print("  python convert_to_markdown.py --file <file_path>     # single file only")
    print("  python convert_to_markdown.py --memory <source_path> # folder (all files)")
    print("  Use --file when user asks for ONE file. Use --memory only for folders.")


if __name__ == "__main__":
    main()
