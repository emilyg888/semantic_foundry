from __future__ import annotations

from semantic_foundry.config import UseCase


REQUIRED_FIELDS = {
    "use_case_id",
    "business_objective",
    "primary_users",
    "business_questions",
    "decision_type",
    "automation_level",
    "risk_level",
}


def validate_use_case(payload: dict) -> UseCase:
    missing = sorted(REQUIRED_FIELDS.difference(payload))
    if missing:
        raise ValueError(f"Use case is missing required fields: {', '.join(missing)}")

    primary_users = ensure_list(payload["primary_users"], "primary_users")
    business_questions = ensure_list(payload["business_questions"], "business_questions")
    in_scope_entities = ensure_list(payload.get("in_scope_entities", []), "in_scope_entities")
    in_scope_signals = ensure_list(payload.get("in_scope_signals", []), "in_scope_signals")
    source_dataset_names = ensure_list(payload.get("source_dataset_names", []), "source_dataset_names")
    owners = payload.get("owners", {})

    if not isinstance(owners, dict):
        raise ValueError("owners must be a mapping")

    return UseCase(
        use_case_id=str(payload["use_case_id"]),
        business_objective=str(payload["business_objective"]),
        primary_users=[str(item) for item in primary_users],
        business_questions=[str(item) for item in business_questions],
        decision_type=str(payload["decision_type"]),
        automation_level=str(payload["automation_level"]),
        risk_level=str(payload["risk_level"]),
        in_scope_entities=[str(item) for item in in_scope_entities],
        in_scope_signals=[str(item) for item in in_scope_signals],
        owners={str(key): str(value) for key, value in owners.items()},
        source_dataset_names=[str(item) for item in source_dataset_names],
        target=str(payload.get("target", "generic_sql")),
    )


def ensure_list(value: object, field_name: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value
