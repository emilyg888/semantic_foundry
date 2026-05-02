from __future__ import annotations

from semantic_foundry.config import UseCase


def resolve_scope(use_case: UseCase) -> dict[str, object]:
    return {
        "entities": use_case.in_scope_entities,
        "signals": use_case.in_scope_signals,
        "owners": use_case.owners,
        "target": use_case.target,
        "requires_human_review": use_case.risk_level.lower() in {"high", "critical"},
    }
