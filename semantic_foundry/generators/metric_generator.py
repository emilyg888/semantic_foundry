from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.generators.reference_data import REFERENCE_METRICS


def build_metrics(use_case: UseCase) -> dict[str, object]:
    metrics = []
    for metric in REFERENCE_METRICS:
        row = dict(metric)
        row["owner"] = use_case.owners.get(metric["metric_id"], metric["owner"])
        row["source_references"] = ["fraud/detector.py::predict_fraud", "design/semantic_foundry_detailed_design.md"]
        metrics.append(row)
    return {"use_case_id": use_case.use_case_id, "metrics": metrics}
