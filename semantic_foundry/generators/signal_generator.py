from __future__ import annotations

from semantic_foundry.config import FunctionLogic, UseCase
from semantic_foundry.generators.reference_data import REFERENCE_SIGNALS


def build_signals(use_case: UseCase, logic: list[FunctionLogic]) -> dict[str, object]:
    signals = []
    for name, template in REFERENCE_SIGNALS.items():
        template = REFERENCE_SIGNALS[name]
        signals.append(
            {
                "signal_id": name,
                "signal_type": "derived_signal",
                "definition": template["definition"],
                "logic": template["logic"],
                "required_inputs": template["required_inputs"],
                "status": template["status"],
                "owner": use_case.owners.get(name, "Fraud Analytics Lead"),
                "source_references": source_references_for_signal(name),
            }
        )
    return {"use_case_id": use_case.use_case_id, "signals": signals}


def find_source_references(signal_name: str, logic: list[FunctionLogic]) -> list[str]:
    refs: list[str] = []
    for function in logic:
        names = set(function.assigned_names) | set(function.return_names)
        if signal_name in names:
            refs.append(f"{function.module_path}::{function.function_name}")
    return refs or ["design/semantic_foundry_detailed_design.md"]


def source_references_for_signal(signal_name: str) -> list[str]:
    references = {
        "amount_spike_signal": ["fraud/features.py::build_features", "fraud/detector.py::predict_fraud"],
        "velocity_burst_signal": ["fraud/features.py::build_features", "fraud/detector.py::predict_fraud"],
        "statistical_anomaly_signal": ["fraud/features.py::build_features", "fraud/detector.py::predict_fraud"],
        "account_burst_history_signal": ["fraud/features.py::build_features"],
    }
    return references.get(signal_name, ["design/semantic_foundry_detailed_design.md"])
