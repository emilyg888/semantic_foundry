from pathlib import Path
import unittest

from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.scanners.python_logic_miner import mine_python_logic
from semantic_foundry.scanners.semantic_classifier import (
    build_governance_context,
    classify_alert_candidates,
    classify_semantic_candidates,
    classify_signal_candidates,
)


class SemanticClassifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        self.logic = mine_python_logic(Path("examples/business_banking_fraud/source"))

    def test_classifies_semantic_entities_relationships_and_fields(self) -> None:
        payload = classify_semantic_candidates(self.use_case, self.logic)

        self.assertEqual(
            payload["entities"],
            ["business_customer", "business_account", "merchant", "transaction"],
        )
        self.assertIn(
            {"from": "business_customer", "to": "business_account", "type": "owns"},
            payload["relationships"],
        )
        self.assertIn(
            {"from": "merchant", "to": "transaction", "type": "accepts"},
            payload["relationships"],
        )
        self.assertIn(
            {"from": "transaction", "to": "merchant", "type": "occurs_at"},
            payload["relationships"],
        )
        self.assertIn(
            {"from": "business_account", "to": "merchant", "type": "transacts_with"},
            payload["relationships"],
        )
        self.assertIn("amount", payload["business_fields"])
        self.assertIn("txn_timestamp", payload["business_fields"])
        self.assertIn("merchant_id", payload["business_fields"])
        self.assertIn("merchant_category", payload["business_fields"])
        self.assertIn("merchant_risk_rating", payload["business_fields"])

    def test_classifies_signal_and_alert_layers(self) -> None:
        signal_payload = classify_signal_candidates(self.use_case, self.logic)
        alert_payload = classify_alert_candidates(self.use_case, self.logic)

        self.assertIn("abs_amount", signal_payload["features"])
        self.assertIn("is_velocity", signal_payload["signals"])
        self.assertEqual(signal_payload["scores"], ["fraud_score"])
        self.assertEqual(alert_payload["outputs"], ["predicted_fraud"])
        self.assertTrue(alert_payload["requires_human_review"])

    def test_builds_governance_context(self) -> None:
        payload = build_governance_context(self.use_case)

        self.assertEqual(payload["target_platform"], "generic_sql")
        self.assertEqual(payload["owner_defaults"]["fraud_signal"], "Fraud Risk Owner")


if __name__ == "__main__":
    unittest.main()
