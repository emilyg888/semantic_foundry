from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from semantic_foundry import __version__
from semantic_foundry.config import InventorySummary, UseCase


def build_semantic_manifest(
    use_case: UseCase,
    inventory: InventorySummary,
    generated_assets: list[str],
    source_path: Path,
    use_case_path: Path,
) -> dict[str, object]:
    return {
        "run": {
            "run_id": f"{datetime.now(UTC).strftime('%Y-%m-%dT%H%M%SZ')}_{use_case.use_case_id}",
            "semantic_foundry_version": __version__,
            "source_hash": hash_directory(source_path),
            "use_case_hash": sha256(use_case_path.read_bytes()).hexdigest(),
            "llm_model": None,
            "generation_mode": "build",
            "generated_assets": generated_assets,
            "validation_status": "passed",
            "certification_status": "candidate",
            "inventory_counts": inventory.counts_by_category,
        }
    }


def hash_directory(root: Path) -> str:
    digest = sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()
