import unittest

from semantic_foundry.validators.certification_validator import evaluate_certification_gate


def make_artefacts() -> dict[str, object]:
    return {
        "glossary": {
            "generated_terms": [
                {"term": "customer", "review_status": "draft", "owner": "Owner", "sensitivity": "restricted"},
                {"term": "transaction", "review_status": "draft", "owner": "Owner", "sensitivity": "restricted"},
            ]
        },
        "entities": {
            "entities": [
                {
                    "entity_id": "certified_transaction",
                    "review_status": "draft",
                    "certification_status": "draft",
                    "owner": "Owner",
                    "source_references": ["dataset::transactions"],
                }
            ]
        },
        "signals": {
            "signals": [
                {"signal_id": "amount_spike_signal", "status": "experimental", "owner": "Owner", "source_references": ["f.py::x"]}
            ]
        },
        "predictions": {
            "predictions": [
                {"prediction_id": "predicted_fraud", "status": "candidate", "owner": "Owner", "source_references": ["f.py::y"]}
            ]
        },
        "metrics": {
            "metrics": [
                {"metric_id": "fraud_precision", "status": "draft", "owner": "Owner", "source_references": ["f.py::z"]}
            ]
        },
        "policies": {"policies": [{"policy_id": "p1"}]},
        "ai_context_cards": {"ai_context_cards": [{"asset_id": "certified_transaction_fraud_signal"}]},
        "dq_validation": {"dq_validation": {"status": "passed"}},
        "policy_validation": {"policy_validation": {"status": "passed"}},
        "sql_validation": {"sql_validation": {"status": "passed"}},
        "issue_register": {"issues": []},
    }


class CertificationValidatorTests(unittest.TestCase):
    def test_returns_draft_when_validations_pass_but_approvals_are_still_draft(self) -> None:
        gate = evaluate_certification_gate(make_artefacts())

        self.assertEqual(gate.validation_status, "passed")
        self.assertEqual(gate.result, "draft")
        self.assertFalse(next(req for req in gate.requirements if req.name == "business_definition_approved").passed)

    def test_returns_candidate_when_requirements_are_satisfied(self) -> None:
        artefacts = make_artefacts()
        artefacts["glossary"]["generated_terms"][0]["review_status"] = "candidate"  # type: ignore[index]
        artefacts["glossary"]["generated_terms"][1]["review_status"] = "candidate"  # type: ignore[index]
        artefacts["entities"]["entities"][0]["review_status"] = "candidate"  # type: ignore[index]
        artefacts["entities"]["entities"][0]["certification_status"] = "candidate"  # type: ignore[index]
        artefacts["signals"]["signals"][0]["status"] = "candidate"  # type: ignore[index]
        artefacts["metrics"]["metrics"][0]["status"] = "candidate"  # type: ignore[index]

        gate = evaluate_certification_gate(artefacts)

        self.assertEqual(gate.result, "candidate")
        self.assertEqual(gate.blockers, [])

    def test_returns_not_certifiable_when_blocking_issue_exists(self) -> None:
        artefacts = make_artefacts()
        artefacts["issue_register"] = {
            "issues": [
                {
                    "severity": "high",
                    "asset": "fraud_precision",
                    "issue": "Synthetic labels are not production-confirmed outcomes.",
                    "blocking": True,
                }
            ]
        }

        gate = evaluate_certification_gate(artefacts)

        self.assertEqual(gate.result, "not_certifiable")
        self.assertIn("Synthetic labels are not production-confirmed outcomes.", gate.blockers)


if __name__ == "__main__":
    unittest.main()
