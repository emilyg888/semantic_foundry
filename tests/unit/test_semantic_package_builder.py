from pathlib import Path
import unittest

from semantic_foundry.builders.semantic_package_builder import (
    build_evaluation_questions,
    build_lineage,
    build_metric_catalogue,
    build_package_manifest,
    build_semantic_catalogue,
    build_signal_catalogue,
)
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.runtime import build_discovery_report
from semantic_foundry.scanners.python_logic_miner import mine_python_logic
from semantic_foundry.scanners.source_inventory import build_source_inventory


def make_artefacts() -> dict[str, object]:
    return {
        "glossary": {"use_case_id": "uc1", "generated_terms": [{"term": "customer"}]},
        "entities": {"use_case_id": "uc1", "entities": [{"entity_id": "business_customer", "source_references": ["dataset::customers"]}]},
        "relationships": {"use_case_id": "uc1", "relationships": [{"relationship_name": "owns"}]},
        "signals": {
            "use_case_id": "uc1",
            "signals": [
                {
                    "signal_id": "amount_spike_signal",
                    "logic": "abs_amount > 15000",
                    "source_references": ["fraud/detector.py::predict_fraud"],
                }
            ],
        },
        "predictions": {
            "use_case_id": "uc1",
            "predictions": [
                {
                    "prediction_id": "predicted_fraud",
                    "name": "Predicted Fraud",
                    "prediction_type": "binary_flag",
                    "evaluation_subject": "transaction",
                    "definition": "Flags suspicious transactions.",
                    "logic": "is_spike",
                    "owner": "Fraud Operations Lead",
                    "status": "candidate",
                    "source_references": ["fraud/detector.py::predict_fraud"],
                },
                {
                    "prediction_id": "fraud_score",
                    "name": "Fraud Score",
                    "prediction_type": "risk_score",
                    "evaluation_subject": "transaction",
                    "definition": "Composite score.",
                    "logic": "weighted sum",
                    "owner": "Fraud Analytics Lead",
                    "status": "draft",
                    "source_references": ["fraud/detector.py::predict_fraud"],
                },
            ],
        },
        "metrics": {
            "use_case_id": "uc1",
            "metrics": [
                {
                    "metric_id": "fraud_precision",
                    "formula": "tp / (tp + fp)",
                    "required_inputs": ["true_positive", "false_positive"],
                    "source_references": ["fraud/detector.py::predict_fraud"],
                }
            ],
        },
        "policies": {"policies": [{"policy_id": "policy_human_review_required"}]},
        "ai_context_cards": {"use_case_id": "uc1", "ai_context_cards": [{"asset_id": "certified_fraud_alert"}]},
    }


class SemanticPackageBuilderTests(unittest.TestCase):
    def test_build_package_manifest_contains_root_file_contract(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        class Gate:
            result = "draft"

        manifest = build_package_manifest(use_case, Gate())

        self.assertEqual(manifest["package_id"], use_case.use_case_id)
        self.assertEqual(manifest["artefacts"]["lineage"], "lineage.yaml")

    def test_build_catalogues_and_lineage(self) -> None:
        artefacts = make_artefacts()

        semantic_catalogue = build_semantic_catalogue(artefacts)
        signal_catalogue = build_signal_catalogue(artefacts)
        metric_catalogue = build_metric_catalogue(artefacts)
        lineage = build_lineage(artefacts)

        self.assertIn("glossary_terms", semantic_catalogue)
        self.assertIn("prediction_outputs", signal_catalogue)
        self.assertIn("scores", signal_catalogue)
        self.assertEqual(metric_catalogue["metrics"][0]["metric_id"], "fraud_precision")
        self.assertEqual(lineage["lineage"][0]["asset_id"], "amount_spike_signal")

    def test_build_evaluation_questions_maps_business_questions_to_assets(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        questions = build_evaluation_questions(use_case, make_artefacts())

        self.assertEqual(questions["use_case_id"], use_case.use_case_id)
        self.assertTrue(any("predicted_fraud" in row["expected_assets"] for row in questions["evaluation_questions"]))

    def test_build_discovery_report_preserves_structured_discovery(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        inventory = build_source_inventory(Path("examples/business_banking_fraud/source"))
        logic = mine_python_logic(Path("examples/business_banking_fraud/source"))

        report = build_discovery_report(use_case, inventory, logic)

        self.assertIn("semantic_layer_candidates", report)
        self.assertIn("signal_layer_candidates", report)
        self.assertIn("alert_layer_candidates", report)


if __name__ == "__main__":
    unittest.main()
