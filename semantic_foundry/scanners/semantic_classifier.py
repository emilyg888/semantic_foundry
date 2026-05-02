from __future__ import annotations

from semantic_foundry.config import FunctionLogic, UseCase


ENTITY_NAME_MAP = {
    "customer": "business_customer",
    "customers": "business_customer",
    "account": "business_account",
    "accounts": "business_account",
    "merchant": "merchant",
    "merchants": "merchant",
    "transaction": "transaction",
    "transactions": "transaction",
}

BUSINESS_FIELDS_BY_ENTITY = {
    "business_customer": [
        "customer_id",
        "customer_name",
        "country",
        "risk_rating",
    ],
    "business_account": [
        "account_id",
        "customer_id",
        "account_type",
        "opened_date",
    ],
    "transaction": [
        "txn_id",
        "account_id",
        "amount",
        "txn_timestamp",
        "fraud_flag",
    ],
    "merchant": [
        "merchant_id",
        "merchant_category",
        "merchant_risk_rating",
    ],
}

FEATURE_NAMES = {
    "abs_amount",
    "txn_count",
    "same_ts_count",
    "z_score",
    "account_zscore",
}

SIGNAL_NAMES = {
    "is_burst",
    "account_had_burst",
    "is_spike",
    "is_velocity",
    "is_anomaly",
}

SCORE_NAMES = {"fraud_score"}
ALERT_OUTPUT_NAMES = {"predicted_fraud"}


def classify_semantic_candidates(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, object]:
    entity_candidates = build_entity_candidates(use_case)
    return {
        "entities": entity_candidates,
        "relationships": build_relationship_candidates(entity_candidates),
        "business_fields": build_business_fields(entity_candidates),
    }


def classify_signal_candidates(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, list[str]]:
    names = discovered_names(logic) | set(use_case.in_scope_signals)
    return {
        "features": sorted(name for name in FEATURE_NAMES if name in names),
        "signals": sorted(name for name in SIGNAL_NAMES if name in names),
        "scores": sorted(name for name in SCORE_NAMES if name in names),
    }


def classify_alert_candidates(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, object]:
    names = discovered_names(logic) | set(use_case.in_scope_signals)
    return {
        "outputs": sorted(name for name in ALERT_OUTPUT_NAMES if name in names),
        "requires_human_review": use_case.risk_level.lower() in {"high", "critical"},
    }


def build_governance_context(use_case: UseCase) -> dict[str, object]:
    return {
        "owner_defaults": use_case.owners,
        "target_platform": use_case.target,
    }


def build_entity_candidates(use_case: UseCase) -> list[str]:
    candidates: list[str] = []
    for name in use_case.in_scope_entities or use_case.source_dataset_names:
        mapped = ENTITY_NAME_MAP.get(name, name)
        if mapped not in candidates:
            candidates.append(mapped)
    return candidates


def build_relationship_candidates(entity_candidates: list[str]) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []
    if "business_customer" in entity_candidates and "business_account" in entity_candidates:
        relationships.append(
            {
                "from": "business_customer",
                "to": "business_account",
                "type": "owns",
            }
        )
    if "business_account" in entity_candidates and "transaction" in entity_candidates:
        relationships.append(
            {
                "from": "business_account",
                "to": "transaction",
                "type": "has",
            }
        )
    if "transaction" in entity_candidates and "merchant" in entity_candidates:
        relationships.append(
            {
                "from": "transaction",
                "to": "merchant",
                "type": "occurs_at",
            }
        )
    if "merchant" in entity_candidates and "transaction" in entity_candidates:
        relationships.append(
            {
                "from": "merchant",
                "to": "transaction",
                "type": "accepts",
            }
        )
    if "business_account" in entity_candidates and "merchant" in entity_candidates:
        relationships.append(
            {
                "from": "business_account",
                "to": "merchant",
                "type": "transacts_with",
            }
        )
    return relationships


def build_business_fields(entity_candidates: list[str]) -> list[str]:
    fields: list[str] = []
    for entity in entity_candidates:
        for field in BUSINESS_FIELDS_BY_ENTITY.get(entity, []):
            if field not in fields:
                fields.append(field)
    return fields


def discovered_names(logic: list[FunctionLogic]) -> set[str]:
    names: set[str] = set()
    for function in logic:
        names.update(function.assigned_names)
        names.update(function.return_names)
    return names
