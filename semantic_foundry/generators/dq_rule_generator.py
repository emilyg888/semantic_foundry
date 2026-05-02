from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.generators.reference_data import REFERENCE_DQ_RULES


def build_dq_rules(use_case: UseCase) -> dict[str, object]:
    return {"use_case_id": use_case.use_case_id, "dq_rules": REFERENCE_DQ_RULES}
