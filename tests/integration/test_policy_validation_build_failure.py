from pathlib import Path
import unittest
from unittest.mock import patch

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build
from semantic_foundry.validators.policy_validator import PolicyValidationError


class PolicyValidationBuildFailureIntegrationTests(unittest.TestCase):
    def test_build_fails_when_ai_context_omits_human_review_guardrail(self) -> None:
        broken_ai_context = {
            "use_case_id": "business_banking_fraud_detection",
            "ai_context_cards": [
                {
                    "asset_id": "certified_transaction_fraud_signal",
                    "approved_questions": ["Which transactions are suspicious?"],
                    "refusal_rule": "Explain only.",
                    "allowed_actions": ["Explain contributing fraud signals"],
                    "disallowed_actions": ["Use uncertified synthetic labels as production truth"],
                }
            ],
        }

        with patch("semantic_foundry.runtime.build_ai_context_cards", return_value=broken_ai_context):
            with self.assertRaises(PolicyValidationError) as context:
                build(
                    BuildRequest(
                        source_path=Path("examples/business_banking_fraud/source"),
                        use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                        output_root=Path("outputs/policy_failure_runs"),
                        target="generic_sql",
                    )
                )

        self.assertIn("high_risk_human_review_control", str(context.exception))


if __name__ == "__main__":
    unittest.main()
