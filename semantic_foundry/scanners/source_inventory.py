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
                role=infer_role(path.relative_to(root).as_posix()),
            )
        )
    return InventorySummary(root=str(root), files=files)


def infer_role(relative_path: str) -> str | None:
    role_by_suffix_path = {
        "fraud/features.py": "feature_engineering",
        "fraud/detector.py": "fraud_detector",
        "fraud/run_fraud.py": "evaluation_runner",
        "fraud/load.py": "data_enrichment",
        "datasets/generator.py": "synthetic_data_generator",
        "datasets/generator_v2.py": "synthetic_data_generator",
        "datasets/generator_v3.py": "synthetic_data_generator",
        "datasets/schema.py": "schema_validation",
        "datasets/validator.py": "dq_validation",
    }
    return role_by_suffix_path.get(relative_path)
