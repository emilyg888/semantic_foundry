from __future__ import annotations

from semantic_foundry.config import FunctionLogic, UseCase
from semantic_foundry.generators.reference_data import REFERENCE_GLOSSARY


def build_glossary(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, object]:
    discovered_terms = {
        "customer",
        "account",
        "transaction",
        "merchant",
        "fraud_label",
        "model_run",
        "fraud_signal",
        "fraud_alert",
        "fraud_score",
    }
    for function in logic:
        discovered_terms.update(normalise_name(name) for name in function.assigned_names)
        discovered_terms.update(normalise_name(name) for name in function.return_names)

    ordered_terms = [term for term in REFERENCE_GLOSSARY if term in discovered_terms or term in {"burst_activity", "synthetic_fraud_label"}]

    return {
        "use_case_id": use_case.use_case_id,
        "generated_terms": [
            {
                "term": term,
                "definition": REFERENCE_GLOSSARY[term]["definition"],
                "owner": use_case.owners.get(term, REFERENCE_GLOSSARY[term]["owner"]),
                "synonyms": REFERENCE_GLOSSARY[term]["synonyms"],
                "sensitivity": REFERENCE_GLOSSARY[term]["sensitivity"],
                "review_status": "draft",
                "source_references": source_references_for_term(term, logic),
                "confidence": confidence_for_term(term),
            }
            for term in ordered_terms
        ],
    }


def normalise_name(name: str) -> str:
    mapping = {
        "predicted_fraud": "fraud_alert",
        "fraud_score": "fraud_score",
        "is_burst": "burst_activity",
        "fraud_flag": "synthetic_fraud_label",
    }
    return mapping.get(name, name)


def source_references_for_term(term: str, logic: list[FunctionLogic]) -> list[str]:
    refs: list[str] = []
    for function in logic:
        names = set(function.assigned_names) | set(function.return_names)
        if term == "fraud_alert" and "predicted_fraud" in names:
            refs.append(f"{function.module_path}::{function.function_name}")
        elif term == "fraud_score" and "fraud_score" in names:
            refs.append(f"{function.module_path}::{function.function_name}")
        elif term == "burst_activity" and "is_burst" in names:
            refs.append(f"{function.module_path}::{function.function_name}")
    return refs or ["design/semantic_foundry_detailed_design.md"]


def confidence_for_term(term: str) -> float:
    if term in {"customer", "account", "transaction"}:
        return 0.95
    if term in {"fraud_signal", "fraud_alert", "fraud_score"}:
        return 0.89
    return 0.82
