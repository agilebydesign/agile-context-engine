"""
Agile Context Engine — defines skill structure, scaffold, and build.
Engine for building and running skills in their entirety.
All structural logic lives here. Skill scripts are thin entry points.
"""
import json
from pathlib import Path
from typing import Any

from .config import AceConfig
from .ace_skill import AceSkill


def _default_engine_root() -> Path:
    """Resolve engine root (parent of src/)."""
    return Path(__file__).resolve().parent.parent


class AgileContextEngine:
    """Engine for building and running skills in their entirety."""

    def __init__(self, engine_root: str | Path | None = None):
        self.engine_root = Path(engine_root).resolve() if engine_root else _default_engine_root()
        self.config_path = self.engine_root / "conf" / "ace-config.json"
        self.workspace_path: Path | None = None
        self.strategy_path: Path | None = None
        self.context_paths: list[Path] = []
        self.skills: list[AceSkill] = []

    def load(self) -> "AgileContextEngine":
        """Load config; load skills; inject self into each skill."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        config = AceConfig.model_validate(data)
        if config.skill_space_path:
            self.workspace_path = Path(config.skill_space_path).resolve()
            self._update_strategy_path()
        order = (config.skills_config or {}).get("order", config.skills)
        self.skills = []
        for rel_path in order:
            skill_path = (self.engine_root / rel_path).resolve()
            if skill_path.exists():
                skill = AceSkill(skill_path, engine=self)
                skill.rule_set.load()
                self.skills.append(skill)
        return self

    def set_workspace(self, path: str | Path) -> Path:
        """Set workspace; persist to config; create output dirs for each skill."""
        self.workspace_path = Path(path).resolve()
        if not self.workspace_path.exists():
            self.workspace_path.mkdir(parents=True, exist_ok=True)
        self._persist_config()
        self._create_output_dirs()
        self._update_strategy_path()
        return self.workspace_path

    def get_skill(self, name: str) -> AceSkill | None:
        """Get skill by name (e.g. ace-shaping)."""
        for s in self.skills:
            if s.path.name == name or name in str(s.path):
                return s
        return None

    def get_skill_scaffold_spec(self) -> dict[str, Any]:
        """Returns canonical ace-skill structure."""
        return get_skill_scaffold_spec()

    def scaffold_skill(self, name: str, path: str | Path) -> Path:
        """Creates ace-skill directory with content/, rules/, scripts/."""
        return scaffold_skill(name, path, engine_root=self.engine_root)

    def build_skill(self, skill_path: str | Path) -> Path:
        """Assembles content into AGENTS.md."""
        return build_skill(skill_path, engine_root=self.engine_root)

    def _persist_config(self) -> None:
        """Write skill_space_path to config."""
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        data["skill_space_path"] = str(self.workspace_path)
        self.config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _create_output_dirs(self) -> None:
        """Create <workspace>/ace-output/<skill-name>/ for each registered skill."""
        if not self.workspace_path:
            return
        output_root = self.workspace_path / "ace-output"
        output_root.mkdir(parents=True, exist_ok=True)
        for skill in self.skills:
            skill_name = skill.path.name
            (output_root / skill_name).mkdir(parents=True, exist_ok=True)
            (output_root / skill_name / "story").mkdir(parents=True, exist_ok=True)
            (output_root / skill_name / "slice-1").mkdir(parents=True, exist_ok=True)

    def _update_strategy_path(self) -> None:
        """Set strategy_path from workspace when ace-shaping output exists."""
        if not self.workspace_path:
            self.strategy_path = None
            return
        # Default: <workspace>/ace-output/ace-shaping/story/shaping-strategy.md
        candidates = [
            self.workspace_path / "ace-output" / "ace-shaping" / "story" / "shaping-strategy.md",
            self.workspace_path / "docs" / "shaping-strategy.md",
        ]
        for p in candidates:
            if p.exists():
                self.strategy_path = p
                return
        # Even if not exists, caller may create it — point to default location
        self.strategy_path = candidates[0]


# Content files in order for assembly
CONTENT_ORDER = [
    "shaping-core.md",
    "shaping-process.md",
    "shaping-strategy.md",
    "shaping-output.md",
    "shaping-validation.md",
]

# Optional content for skills with scripts
SCRIPT_INVOCATION = "script-invocation.md"


def get_skill_scaffold_spec() -> dict[str, Any]:
    """
    Returns the canonical ace-skill structure. Engine is single source of truth.
    No file — in-memory spec.
    """
    return {
        "content_files": CONTENT_ORDER + [SCRIPT_INVOCATION],
        "dirs": ["content", "rules", "scripts"],
        "root_files": ["SKILL.md", "README.md", "skill-config.json"],
        "content_templates": {
            "shaping-core.md": "# Core Definitions\n\n",
            "shaping-process.md": "# Shaping Process\n\n",
            "shaping-strategy.md": "# Shaping Strategy\n\n",
            "shaping-output.md": "# Output Structure\n\n",
            "shaping-validation.md": "# Validation\n\n",
            "script-invocation.md": "# Script Invocation\n\nHow to call scripts (params, when, what to expect).\n",
        },
        "rules_default": {"scanners": []},
    }


def scaffold_skill(name: str, path: str | Path, engine_root: str | Path | None = None) -> Path:
    """
    Creates an ace-skill directory with content/, rules/, scripts/, and standard files.
    Engine does the actual file/dir creation.
    """
    path = Path(path)
    if not path.is_absolute() and engine_root:
        path = Path(engine_root) / path
    path = path.resolve()

    spec = get_skill_scaffold_spec()

    # Create dirs
    for d in spec["dirs"]:
        (path / d).mkdir(parents=True, exist_ok=True)

    # Create content files
    for fname in spec["content_files"]:
        content_path = path / "content" / fname
        content_path.parent.mkdir(parents=True, exist_ok=True)
        template = spec["content_templates"].get(fname, "")
        if not content_path.exists():
            content_path.write_text(template, encoding="utf-8")

    # Create rules/scanners.json
    rules_dir = path / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    scanners_path = rules_dir / "scanners.json"
    if not scanners_path.exists():
        import json
        scanners_path.write_text(
            json.dumps(spec["rules_default"], indent=2),
            encoding="utf-8",
        )

    # Create scripts/build.py
    scripts_dir = path / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    build_script = scripts_dir / "build.py"
    if not build_script.exists():
        build_script.write_text(_BUILD_SCRIPT_TEMPLATE.format(skill_name=name), encoding="utf-8")

    # Create SKILL.md
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        skill_md.write_text(
            f"# {name}\n\nAce-skill. Fill content pieces and run build.\n",
            encoding="utf-8",
        )

    # Create README.md
    readme = path / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {name}\n\nRun `python scripts/build.py` to assemble AGENTS.md.\n",
            encoding="utf-8",
        )

    # Create skill-config.json
    skill_config = path / "skill-config.json"
    if not skill_config.exists():
        import json
        skill_config.write_text(
            json.dumps({"name": name, "version": "0.1.0"}, indent=2),
            encoding="utf-8",
        )

    return path


def build_skill(skill_path: str | Path, engine_root: str | Path | None = None) -> Path:
    """
    Assembles content/*.md into AGENTS.md per engine conventions.
    Order: shaping-core, shaping-process, shaping-strategy, shaping-output, shaping-validation.
    """
    skill_path = Path(skill_path)
    if not skill_path.is_absolute() and engine_root:
        skill_path = Path(engine_root) / skill_path
    skill_path = skill_path.resolve()

    content_dir = skill_path / "content"
    output_path = skill_path / "AGENTS.md"

    parts: list[str] = []
    for fname in CONTENT_ORDER:
        p = content_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    # Optional: script-invocation at end
    script_inv = content_dir / SCRIPT_INVOCATION
    if script_inv.exists():
        parts.append(script_inv.read_text(encoding="utf-8").strip())
        parts.append("\n\n---\n\n")

    output_path.write_text("".join(parts).rstrip() + "\n", encoding="utf-8")
    return output_path


_BUILD_SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""Build AGENTS.md from content. Thin entry point — delegates to engine."""
import sys
from pathlib import Path

# Add engine to path when run from skill dir
_skill_dir = Path(__file__).resolve().parent.parent
_engine_root = _skill_dir.parent.parent  # skills/ace-<name> -> skills -> repo root
if str(_engine_root) not in sys.path:
    sys.path.insert(0, str(_engine_root))

from src.engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_engine_root)
    print(f"Wrote {{out}}")
'''