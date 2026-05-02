from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.generators.reference_data import REFERENCE_RELATIONSHIPS


def build_relationships(use_case: UseCase) -> dict[str, object]:
    return {
        "use_case_id": use_case.use_case_id,
        "relationships": REFERENCE_RELATIONSHIPS,
    }
