from __future__ import annotations

from pathlib import Path

from semantic_foundry.config import InventorySummary, SourceFile


CATEGORY_BY_SUFFIX = {
    ".py": "python",
    ".sql": "sql",
    ".ipynb": "notebook",
    ".yml": "config",
    ".yaml": "config",
    ".csv": "data",
    ".json": "data",
    ".md": "documentation",
}

SKIP_DIRS = {"__pycache__", ".venv", ".git", "outputs"}


def build_source_inventory(root: Path) -> InventorySummary:
    files: list[SourceFile] = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        category = CATEGORY_BY_SUFFIX.get(suffix, "other")
        files.append(
            SourceFile(
                path=str(path.relative_to(root)),
                category=category,
                suffix=suffix or "<none>",
            )
        )
    return InventorySummary(root=str(root), files=files)
