from pathlib import Path
import shutil
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build


class BuildIntegrationTests(unittest.TestCase):
    def test_build_generates_expected_mvp_package(self) -> None:
        output_root = Path("outputs/test_runs")
        if output_root.exists():
            shutil.rmtree(output_root)

        output_dir = build(
            BuildRequest(
                source_path=Path("examples/business_banking_fraud/source"),
                use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                output_root=output_root,
                target="generic_sql",
            )
        )

        expected_files = {
            "README.md",
            "package_manifest.yaml",
            "use_case.yaml",
            "discovery_report.json",
            "semantic_catalogue.yaml",
            "signal_catalogue.yaml",
            "metric_catalogue.yaml",
            "dq_rules.yaml",
            "policy_rules.yaml",
            "lineage.yaml",
            "ai_context_cards.yaml",
            "evaluation_questions.yaml",
            "semantic_views.sql",
            "certification_report.md",
            "01_semantic_catalogue/glossary.yaml",
            "01_semantic_catalogue/entities.yaml",
            "01_semantic_catalogue/relationships.yaml",
            "02_signal_catalogue/signals.yaml",
            "03_prediction_catalogue/predictions.yaml",
            "04_evaluation_metric_catalogue/metrics.yaml",
            "05_governance_controls/dq_rules.yaml",
            "05_governance_controls/dq_validation.yaml",
            "05_governance_controls/policies.yaml",
            "05_governance_controls/policy_validation.yaml",
            "05_governance_controls/issue_register.yaml",
            "05_governance_controls/sql_validation.yaml",
            "06_ai_consumption/ai_context_cards.yaml",
            "07_delivery_pack/semantic_manifest.yaml",
            "07_delivery_pack/semantic_views.sql",
            "07_delivery_pack/certification_report.md",
        }

        self.assertTrue(output_dir.exists())
        produced_files = {
            str(path.relative_to(output_dir))
            for path in output_dir.rglob("*")
            if path.is_file()
        }
        self.assertTrue(expected_files.issubset(produced_files))

        glossary = (output_dir / "01_semantic_catalogue" / "glossary.yaml").read_text(encoding="utf-8")
        package_manifest = (output_dir / "package_manifest.yaml").read_text(encoding="utf-8")
        discovery_report = (output_dir / "discovery_report.json").read_text(encoding="utf-8")
        semantic_catalogue = (output_dir / "semantic_catalogue.yaml").read_text(encoding="utf-8")
        signal_catalogue = (output_dir / "signal_catalogue.yaml").read_text(encoding="utf-8")
        metric_catalogue = (output_dir / "metric_catalogue.yaml").read_text(encoding="utf-8")
        lineage = (output_dir / "lineage.yaml").read_text(encoding="utf-8")
        evaluation_questions = (output_dir / "evaluation_questions.yaml").read_text(encoding="utf-8")
        package_index = (output_dir / "README.md").read_text(encoding="utf-8")
        signals = (output_dir / "02_signal_catalogue" / "signals.yaml").read_text(encoding="utf-8")
        predictions = (output_dir / "03_prediction_catalogue" / "predictions.yaml").read_text(encoding="utf-8")
        metrics = (output_dir / "04_evaluation_metric_catalogue" / "metrics.yaml").read_text(encoding="utf-8")
        entities = (output_dir / "01_semantic_catalogue" / "entities.yaml").read_text(encoding="utf-8")
        relationships = (output_dir / "01_semantic_catalogue" / "relationships.yaml").read_text(encoding="utf-8")
        issues = (output_dir / "05_governance_controls" / "issue_register.yaml").read_text(encoding="utf-8")
        dq_validation = (output_dir / "05_governance_controls" / "dq_validation.yaml").read_text(encoding="utf-8")
        policy_validation = (output_dir / "05_governance_controls" / "policy_validation.yaml").read_text(encoding="utf-8")
        sql_validation = (output_dir / "05_governance_controls" / "sql_validation.yaml").read_text(encoding="utf-8")
        manifest = (output_dir / "07_delivery_pack" / "semantic_manifest.yaml").read_text(encoding="utf-8")
        sql = (output_dir / "07_delivery_pack" / "semantic_views.sql").read_text(encoding="utf-8")
        report = (output_dir / "07_delivery_pack" / "certification_report.md").read_text(encoding="utf-8")

        self.assertIn("Semantic_Foundry Package Index", package_index)
        self.assertIn("01_semantic_catalogue/", package_index)
        self.assertIn("07_delivery_pack/", package_index)
        self.assertIn('package_id: "business_banking_fraud_detection"', package_manifest)
        self.assertIn('"semantic_layer_candidates"', discovery_report)
        self.assertIn("glossary_terms:", semantic_catalogue)
        self.assertIn("prediction_outputs:", signal_catalogue)
        self.assertIn("scores:", signal_catalogue)
        self.assertIn('"fraud_precision"', metric_catalogue)
        self.assertIn('"amount_spike_signal"', lineage)
        self.assertIn("evaluation_questions:", evaluation_questions)
        self.assertIn('"fraud_alert"', glossary)
        self.assertIn('"model_run"', glossary)
        self.assertIn('"amount_spike_signal"', signals)
        self.assertIn('"predicted_fraud"', predictions)
        self.assertIn('"fraud_alert_volume"', metrics)
        self.assertIn('metric_type: "operational_metric"', metrics)
        self.assertIn('metric_type: "evaluation_metric"', metrics)
        self.assertIn('grain: "model_run"', metrics)
        self.assertIn('"merchant"', entities)
        self.assertIn('"fraud_alert"', entities)
        self.assertIn('"accepts"', relationships)
        self.assertIn('"occurs_at"', relationships)
        self.assertIn('"transacts_with"', relationships)
        self.assertIn('"may_generate"', relationships)
        self.assertIn("evaluation_runner", issues)
        self.assertIn('status: "passed"', dq_validation)
        self.assertIn('"dq_transactions_primary_key"', dq_validation)
        self.assertIn('status: "passed"', policy_validation)
        self.assertIn('"high_risk_human_review_control"', policy_validation)
        self.assertIn('status: "passed"', sql_validation)
        self.assertIn('certification_status: "not_certifiable"', manifest)
        self.assertIn('"certified_fraud_signal"', sql_validation)
        self.assertIn('"certified_fraud_alert"', sql_validation)
        self.assertIn("create or replace view certified_fraud_model_run as", sql)
        self.assertIn("create or replace view certified_merchant as", sql)
        self.assertIn("create or replace view certified_fraud_alert as", sql)
        self.assertIn("Result: `not_certifiable`", report)
        self.assertIn("Synthetic fraud labels are suitable for accelerator validation only.", report)


if __name__ == "__main__":
    unittest.main()
