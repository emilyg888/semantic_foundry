from __future__ import annotations

from semantic_foundry.config import FunctionLogic, UseCase
from semantic_foundry.generators.reference_data import REFERENCE_PREDICTIONS
from semantic_foundry.generators.signal_generator import find_source_references


def build_predictions(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, object]:
    discovered = set(use_case.in_scope_signals)
    for function in logic:
        discovered.update(function.assigned_names)
        discovered.update(function.return_names)

    ordered_names = [name for name in REFERENCE_PREDICTIONS if name in discovered]
    if not ordered_names:
        ordered_names = list(REFERENCE_PREDICTIONS)

    predictions = []
    for name in ordered_names:
        template = REFERENCE_PREDICTIONS[name]
        predictions.append(
            {
                "prediction_id": name,
                "name": to_display_name(name),
                "prediction_type": template["prediction_type"],
                "evaluation_subject": "transaction",
                "definition": template["definition"],
                "logic": template["logic"],
                "required_inputs": template["required_inputs"],
                "owner": use_case.owners.get(name, "Fraud Analytics Lead"),
                "status": template["status"],
                "source_references": find_source_references(name, logic),
            }
        )
    return {"use_case_id": use_case.use_case_id, "predictions": predictions}


def to_display_name(name: str) -> str:
    if name == "predicted_fraud":
        return "Predicted Fraud"
    if name == "fraud_score":
        return "Fraud Score"
    return name.replace("_", " ").title()
