from pathlib import Path
import unittest

from semantic_foundry.generators.metric_generator import build_metrics
from semantic_foundry.intake.intake_loader import load_use_case


class MetricGeneratorTests(unittest.TestCase):
    def test_build_metrics_includes_operational_and_evaluation_metrics(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        payload = build_metrics(use_case)
        metric_ids = [metric["metric_id"] for metric in payload["metrics"]]

        self.assertEqual(
            metric_ids,
            [
                "fraud_alert_volume",
                "fraud_precision",
                "fraud_recall",
                "false_positive_rate",
                "false_negative_rate",
                "f1_score",
            ],
        )

        alert_volume = next(metric for metric in payload["metrics"] if metric["metric_id"] == "fraud_alert_volume")
        self.assertEqual(alert_volume["metric_type"], "operational_metric")
        self.assertEqual(alert_volume["grain"], "day")
        self.assertIn("predicted_fraud", alert_volume["required_inputs"])

        f1_score = next(metric for metric in payload["metrics"] if metric["metric_id"] == "f1_score")
        self.assertEqual(f1_score["metric_type"], "evaluation_metric")
        self.assertEqual(f1_score["grain"], "model_run")
        self.assertIn("precision", f1_score["required_inputs"])
        self.assertIn("recall", f1_score["required_inputs"])


if __name__ == "__main__":
    unittest.main()
