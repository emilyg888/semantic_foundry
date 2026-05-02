from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.generators.reference_data import REFERENCE_POLICIES


def build_policies(use_case: UseCase) -> dict[str, object]:
    policies = []
    for policy in REFERENCE_POLICIES:
        row = dict(policy)
        row["review_required"] = use_case.risk_level.lower() in {"high", "critical"}
        policies.append(row)
    return {"use_case_id": use_case.use_case_id, "policies": policies}
