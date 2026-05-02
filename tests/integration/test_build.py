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
            "01_semantic_catalogue/glossary.yaml",
            "01_semantic_catalogue/entities.yaml",
            "01_semantic_catalogue/relationships.yaml",
            "02_signal_catalogue/signals.yaml",
            "03_prediction_catalogue/predictions.yaml",
            "04_evaluation_metric_catalogue/metrics.yaml",
            "05_governance_controls/dq_rules.yaml",
            "05_governance_controls/policies.yaml",
            "05_governance_controls/issue_register.yaml",
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
        signals = (output_dir / "02_signal_catalogue" / "signals.yaml").read_text(encoding="utf-8")
        predictions = (output_dir / "03_prediction_catalogue" / "predictions.yaml").read_text(encoding="utf-8")
        metrics = (output_dir / "04_evaluation_metric_catalogue" / "metrics.yaml").read_text(encoding="utf-8")
        entities = (output_dir / "01_semantic_catalogue" / "entities.yaml").read_text(encoding="utf-8")
        relationships = (output_dir / "01_semantic_catalogue" / "relationships.yaml").read_text(encoding="utf-8")
        sql = (output_dir / "07_delivery_pack" / "semantic_views.sql").read_text(encoding="utf-8")
        report = (output_dir / "07_delivery_pack" / "certification_report.md").read_text(encoding="utf-8")

        self.assertIn('"fraud_alert"', glossary)
        self.assertIn('"model_run"', glossary)
        self.assertIn('"amount_spike_signal"', signals)
        self.assertIn('"predicted_fraud"', predictions)
        self.assertIn('"fraud_alert_volume"', metrics)
        self.assertIn('metric_type: "operational_metric"', metrics)
        self.assertIn('metric_type: "evaluation_metric"', metrics)
        self.assertIn('grain: "model_run"', metrics)
        self.assertIn('"merchant"', entities)
        self.assertIn('"accepts"', relationships)
        self.assertIn('"occurs_at"', relationships)
        self.assertIn('"transacts_with"', relationships)
        self.assertIn("create or replace view certified_fraud_model_run as", sql)
        self.assertIn("create or replace view certified_merchant as", sql)
        self.assertIn("Blocking Issues", report)


if __name__ == "__main__":
    unittest.main()
