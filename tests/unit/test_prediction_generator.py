from pathlib import Path
import unittest

from semantic_foundry.generators.prediction_generator import build_predictions
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.scanners.python_logic_miner import mine_python_logic


class PredictionGeneratorTests(unittest.TestCase):
    def test_build_predictions_creates_prediction_catalogue(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        logic = mine_python_logic(Path("examples/business_banking_fraud/source"))

        payload = build_predictions(use_case, logic)
        prediction_ids = [prediction["prediction_id"] for prediction in payload["predictions"]]

        self.assertEqual(prediction_ids, ["predicted_fraud", "fraud_score"])

        predicted_fraud = next(
            prediction for prediction in payload["predictions"] if prediction["prediction_id"] == "predicted_fraud"
        )
        self.assertEqual(predicted_fraud["prediction_type"], "alert_prediction")
        self.assertIn("is_velocity", predicted_fraud["required_inputs"])

        fraud_score = next(
            prediction for prediction in payload["predictions"] if prediction["prediction_id"] == "fraud_score"
        )
        self.assertEqual(fraud_score["prediction_type"], "risk_score")
        self.assertEqual(fraud_score["evaluation_subject"], "transaction")


if __name__ == "__main__":
    unittest.main()
