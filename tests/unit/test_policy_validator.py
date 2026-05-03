from pathlib import Path
import unittest

from semantic_foundry.generators.ai_contract_generator import build_ai_context_cards
from semantic_foundry.generators.policy_generator import build_policies
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.validators.policy_validator import validate_policies


class PolicyValidatorTests(unittest.TestCase):
    def test_accepts_fixture_policy_and_ai_controls(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        report = validate_policies(
            use_case=use_case,
            policies_artefact=build_policies(use_case),
            ai_context_cards_artefact=build_ai_context_cards(use_case),
        )

        self.assertEqual(report.status, "passed")
        self.assertEqual(report.blocking_findings, [])
        self.assertEqual(len(report.checks), 3)

    def test_rejects_high_risk_use_case_without_human_review_guardrail(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        policies = build_policies(use_case)
        ai_cards = build_ai_context_cards(use_case)
        ai_cards["ai_context_cards"][0]["refusal_rule"] = "Explain features only."  # type: ignore[index]

        report = validate_policies(
            use_case=use_case,
            policies_artefact=policies,
            ai_context_cards_artefact=ai_cards,
        )

        self.assertEqual(report.status, "failed")
        self.assertEqual(report.blocking_findings[0].check_id, "high_risk_human_review_control")

    def test_rejects_ai_cards_without_disallowed_actions(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        policies = build_policies(use_case)
        ai_cards = build_ai_context_cards(use_case)
        ai_cards["ai_context_cards"][0]["disallowed_actions"] = ["Summarise behaviour"]  # type: ignore[index]

        report = validate_policies(
            use_case=use_case,
            policies_artefact=policies,
            ai_context_cards_artefact=ai_cards,
        )

        self.assertEqual(report.status, "failed")
        self.assertTrue(
            any(finding.check_id == "ai_context_disallowed_actions" for finding in report.blocking_findings)
        )


if __name__ == "__main__":
    unittest.main()
