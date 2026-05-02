from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.generators.reference_data import REFERENCE_ENTITIES


def build_entities(use_case: UseCase) -> dict[str, object]:
    entities = []
    for entity in REFERENCE_ENTITIES:
        row = dict(entity)
        row["owner"] = use_case.owners.get(entity["name"], entity["owner"])
        row["source_references"] = [f"dataset::{entity['source_table']}"]
        row["review_status"] = "draft" if row["certification_status"] == "draft" else "candidate"
        entities.append(row)
    return {"use_case_id": use_case.use_case_id, "entities": entities}
