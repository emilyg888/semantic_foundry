import unittest

from semantic_foundry.validators.artefact_schema_validator import validate_artefacts


def make_valid_artefacts() -> dict[str, object]:
    return {
        "glossary": {"use_case_id": "uc1", "generated_terms": [1, 2, 3, 4, 5]},
        "entities": {"use_case_id": "uc1", "entities": [1, 2, 3]},
        "relationships": {"use_case_id": "uc1", "relationships": [1]},
        "metrics": {"use_case_id": "uc1", "metrics": [1]},
        "signals": {"use_case_id": "uc1", "signals": [1, 2, 3]},
        "predictions": {"use_case_id": "uc1", "predictions": [1, 2]},
        "dq_rules": {"use_case_id": "uc1", "dq_rules": [1, 2, 3]},
        "dq_validation": {"use_case_id": "uc1", "dq_validation": {"status": "passed", "checks": []}},
        "policies": {"use_case_id": "uc1", "policies": [1]},
        "policy_validation": {"use_case_id": "uc1", "policy_validation": {"status": "passed", "checks": []}},
        "sql_validation": {"sql_validation": {"status": "passed", "validated_views": [], "checks": []}},
        "ai_context_cards": {"use_case_id": "uc1", "ai_context_cards": [1]},
        "semantic_manifest": {"run": {"run_id": "abc"}},
    }


class ArtefactSchemaValidatorTests(unittest.TestCase):
    def test_accepts_minimum_valid_payload(self) -> None:
        validate_artefacts(make_valid_artefacts())

    def test_rejects_missing_required_artefact_key(self) -> None:
        artefacts = make_valid_artefacts()
        del artefacts["signals"]

        with self.assertRaises(ValueError) as context:
            validate_artefacts(artefacts)

        self.assertIn("Missing artefact: signals", str(context.exception))

    def test_rejects_insufficient_glossary_terms(self) -> None:
        artefacts = make_valid_artefacts()
        artefacts["glossary"] = {"use_case_id": "uc1", "generated_terms": [1, 2, 3, 4]}

        with self.assertRaises(ValueError) as context:
            validate_artefacts(artefacts)

        self.assertIn("Glossary must contain at least 5 generated terms", str(context.exception))


if __name__ == "__main__":
    unittest.main()
