"""
Engine config — pydantic models for ace-config.json.
"""
from pydantic import BaseModel


class AceConfig(BaseModel):
    """Engine config schema. Strict — no extra fields."""

    skill_space_path: str | None = None
    skills: list[str]
    skills_config: dict | None = None
    constraints: list[dict] = []

    class Config:
        extra = "forbid"
