from __future__ import annotations

from semantic_foundry.config import UseCase
from semantic_foundry.validators.certification_validator import CertificationGateReport


def build_package_manifest(use_case: UseCase, gate: CertificationGateReport) -> dict[str, object]:
    return {
        "package_id": use_case.use_case_id,
        "package_name": "Business Banking Fraud Detection Semantic Package",
        "version": "0.1.0",
        "status": gate.result,
        "created_by": "Semantic_Foundry",
        "target_platform": use_case.target,
        "business_domain": "Business Banking",
        "use_case_type": "fraud_detection",
        "risk_level": use_case.risk_level,
        "requires_human_review": True,
        "owners": {
            "business_owner": use_case.owners.get("customer", "Head of Business Banking"),
            "data_owner": use_case.owners.get("account", "Head of Business Banking"),
            "fraud_risk_owner": use_case.owners.get("fraud_signal", "Fraud Risk Owner"),
            "analytics_owner": use_case.owners.get("fraud_score", "Fraud Analytics Lead"),
            "operations_owner": use_case.owners.get("fraud_alert", "Fraud Operations Lead"),
        },
        "artefacts": {
            "use_case": "use_case.yaml",
            "discovery_report": "discovery_report.json",
            "semantic_catalogue": "semantic_catalogue.yaml",
            "signal_catalogue": "signal_catalogue.yaml",
            "metric_catalogue": "metric_catalogue.yaml",
            "dq_rules": "dq_rules.yaml",
            "policy_rules": "policy_rules.yaml",
            "lineage": "lineage.yaml",
            "semantic_views": "semantic_views.sql",
            "ai_context_cards": "ai_context_cards.yaml",
            "evaluation_questions": "evaluation_questions.yaml",
            "certification_report": "certification_report.md",
        },
    }


def build_semantic_catalogue(artefacts: dict[str, object]) -> dict[str, object]:
    glossary = artefacts["glossary"]  # type: ignore[index]
    entities = artefacts["entities"]  # type: ignore[index]
    relationships = artefacts["relationships"]  # type: ignore[index]
    return {
        "use_case_id": glossary["use_case_id"],  # type: ignore[index]
        "glossary_terms": glossary["generated_terms"],  # type: ignore[index]
        "entities": entities["entities"],  # type: ignore[index]
        "relationships": relationships["relationships"],  # type: ignore[index]
    }


def build_signal_catalogue(artefacts: dict[str, object]) -> dict[str, object]:
    predictions = artefacts["predictions"]  # type: ignore[index]
    scores: list[object] = []
    prediction_outputs: list[object] = []
    for prediction in predictions["predictions"]:  # type: ignore[index]
        if prediction["prediction_id"] == "fraud_score":  # type: ignore[index]
            scores.append(
                {
                    "score_id": prediction["prediction_id"],
                    "name": prediction["name"],
                    "source_field": prediction["prediction_id"],
                    "entity": prediction["evaluation_subject"],
                    "definition": prediction["definition"],
                    "owner": prediction["owner"],
                    "score_type": prediction["prediction_type"],
                    "requires_human_review": True,
                    "status": prediction["status"],
                    "source_references": prediction["source_references"],
                }
            )
        else:
            prediction_outputs.append(
                {
                    "prediction_id": prediction["prediction_id"],
                    "name": prediction["name"],
                    "source_field": prediction["prediction_id"],
                    "entity": prediction["evaluation_subject"],
                    "definition": prediction["definition"],
                    "logic": prediction["logic"],
                    "owner": prediction["owner"],
                    "requires_human_review": True,
                    "approved_use": [
                        "fraud analyst review queue",
                        "alert explanation",
                        "detector evaluation",
                    ],
                    "disallowed_use": [
                        "final fraud determination",
                        "account closure without human investigation",
                        "adverse customer action without review",
                    ],
                    "status": prediction["status"],
                    "source_references": prediction["source_references"],
                }
            )
    return {
        "use_case_id": predictions["use_case_id"],  # type: ignore[index]
        "signals": artefacts["signals"]["signals"],  # type: ignore[index]
        "prediction_outputs": prediction_outputs,
        "scores": scores,
    }


def build_metric_catalogue(artefacts: dict[str, object]) -> dict[str, object]:
    return {
        "use_case_id": artefacts["metrics"]["use_case_id"],  # type: ignore[index]
        "metrics": artefacts["metrics"]["metrics"],  # type: ignore[index]
    }


def build_lineage(artefacts: dict[str, object]) -> dict[str, object]:
    lineage: list[dict[str, object]] = []
    for signal in artefacts["signals"]["signals"]:  # type: ignore[index]
        downstream_assets = ["predicted_fraud", "fraud_alert", "fraud_score"]
        lineage.append(
            {
                "asset_id": signal["signal_id"],
                "asset_type": "fraud_signal",
                "upstream_sources": [
                    {
                        "source": source_reference,
                        "source_type": "python_function" if "::" in source_reference else "design_reference",
                        "field": signal["signal_id"],
                    }
                    for source_reference in signal["source_references"]
                ],
                "transformations": [str(signal["logic"])],
                "downstream_assets": downstream_assets,
            }
        )
    for metric in artefacts["metrics"]["metrics"]:  # type: ignore[index]
        lineage.append(
            {
                "asset_id": metric["metric_id"],
                "asset_type": "evaluation_metric",
                "upstream_sources": [
                    {
                        "source": source_reference,
                        "source_type": "python_function" if "::" in source_reference else "design_reference",
                        "field": required_input,
                    }
                    for source_reference in metric["source_references"]
                    for required_input in metric["required_inputs"]
                ],
                "transformations": [str(metric["formula"])],
                "downstream_assets": ["certification_report"],
            }
        )
    return {"lineage": lineage}


def build_evaluation_questions(use_case: UseCase, artefacts: dict[str, object]) -> dict[str, object]:
    return {
        "use_case_id": use_case.use_case_id,
        "evaluation_questions": [
            {
                "question": question,
                "expected_assets": expected_assets_for_question(question, artefacts),
                "human_review_required": True,
            }
            for question in use_case.business_questions
        ],
    }


def expected_assets_for_question(question: str, artefacts: dict[str, object]) -> list[str]:
    lowered = question.lower()
    if "transaction" in lowered and "suspicious" in lowered:
        return ["predicted_fraud", "certified_transaction", "certified_fraud_alert"]
    if "why" in lowered or "contribute" in lowered:
        return [signal["signal_id"] for signal in artefacts["signals"]["signals"]]  # type: ignore[index]
    if "account" in lowered and "burst" in lowered:
        return ["account_burst_history_signal", "certified_business_account"]
    if "customer" in lowered:
        return ["certified_business_customer", "certified_business_account", "certified_transaction"]
    if "rule" in lowered or "alert" in lowered:
        return ["predicted_fraud", "fraud_score"]
    return ["certified_transaction"]
