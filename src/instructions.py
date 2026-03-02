"""
Instructions — assembles sectioned content per operation.
Uses operation_sections map + engine context. No context parameter.
"""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import AgileContextEngine


class Instructions:
    """
    Assembles sections for an operation; injects context from engine.
    Caller uses display_content(operation) to get markdown for injection.
    """

    def __init__(
        self,
        operation_sections: dict[str, list[str]],
        skill_path: Path,
        engine: "AgileContextEngine",
    ):
        self.operation_sections = operation_sections
        self.skill_path = Path(skill_path).resolve()
        self.engine = engine
        self._content_cache: dict[str, str] = {}

    def display_content(self, operation: str) -> str:
        """
        Assembles sections for operation; injects context from engine.
        Returns markdown for caller to inject into prompt.
        """
        section_ids = self.operation_sections.get(operation, [])
        if not section_ids:
            return ""

        parts: list[str] = []
        content_dir = self.skill_path / "content"

        # Map section IDs to content (extract by <!-- section: id -->)
        for sid in section_ids:
            text = self._get_section_content(sid, content_dir)
            if text:
                parts.append(text)
                parts.append("\n\n---\n\n")

        # Inject context metadata
        context = self._build_context_block()
        if context:
            parts.insert(0, context + "\n\n---\n\n")

        # For generate_slice and improve_strategy: append strategy doc when it exists
        if operation in ("generate_slice", "improve_strategy") and self.engine.strategy_path:
            if self.engine.strategy_path.exists():
                strategy_content = self.engine.strategy_path.read_text(encoding="utf-8").strip()
                parts.append("## Strategy Document\n\n")
                parts.append(strategy_content)
                parts.append("\n\n---\n\n")

        return "".join(parts).rstrip() + "\n"

    def sections_included(self, operation: str) -> list[str]:
        """Section IDs that would be assembled (for debugging)."""
        return list(self.operation_sections.get(operation, []))

    def _get_section_content(self, section_id: str, content_dir: Path) -> str:
        """Extract content for section_id from content/*.md or rules/."""
        # shaping.validation.rules -> load from rules/*.md
        if section_id == "shaping.validation.rules":
            rules_dir = self.skill_path / "rules"
            if not rules_dir.exists():
                return ""
            parts: list[str] = []
            for md in sorted(rules_dir.glob("*.md")):
                parts.append(md.read_text(encoding="utf-8").strip())
                parts.append("\n\n---\n\n")
            return "".join(parts).rstrip() if parts else ""

        # section_id like shaping.strategy.phase -> in shaping-strategy.md
        domain = section_id.split(".")[1] if "." in section_id else ""
        file_map = {
            "process": "shaping-process.md",
            "strategy": "shaping-strategy.md",
            "output": "shaping-output.md",
            "validation": "shaping-validation.md",
            "core": "shaping-core.md",
        }
        fname = file_map.get(domain, "shaping-process.md")
        path = content_dir / fname
        if not path.exists():
            return ""

        text = path.read_text(encoding="utf-8")
        marker = f"<!-- section: {section_id} -->"
        if marker not in text:
            return ""

        start = text.index(marker) + len(marker)
        rest = text[start:]
        next_marker = "<!-- section:"
        idx = rest.find(next_marker)
        if idx >= 0:
            return rest[:idx].strip()
        return rest.strip()

    def _build_context_block(self) -> str:
        """Build context metadata from engine."""
        lines: list[str] = []
        if self.engine.workspace_path:
            lines.append(f"**Workspace:** `{self.engine.workspace_path}`")
        if self.engine.strategy_path:
            lines.append(f"**Strategy path:** `{self.engine.strategy_path}`")
        if self.engine.context_paths:
            lines.append("**Context paths:**")
            for p in self.engine.context_paths:
                lines.append(f"- `{p}`")
        if not lines:
            return ""
        return "## Context\n\n" + "\n".join(lines)
