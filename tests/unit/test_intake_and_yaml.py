from pathlib import Path
import tempfile
import textwrap
import unittest

from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.simple_yaml import dump_yaml, load_simple_yaml


class SimpleYamlTests(unittest.TestCase):
    def test_round_trips_nested_mapping_and_list(self) -> None:
        payload = {
            "use_case": {
                "use_case_id": "fraud_case",
                "primary_users": ["fraud analyst", "risk manager"],
                "owners": {"transaction": "Fraud Operations Lead"},
            }
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "sample.yaml"
            path.write_text(dump_yaml(payload) + "\n", encoding="utf-8")

            loaded = load_simple_yaml(path)

        self.assertEqual(loaded, payload)

    def test_loads_json_payload_as_yaml_compatible_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "sample.json"
            path.write_text('{"use_case": {"use_case_id": "fraud_case"}}', encoding="utf-8")

            loaded = load_simple_yaml(path)

        self.assertEqual(loaded["use_case"]["use_case_id"], "fraud_case")


class IntakeLoaderTests(unittest.TestCase):
    def test_load_use_case_parses_example_fixture(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        self.assertEqual(use_case.use_case_id, "business_banking_fraud_detection")
        self.assertIn("fraud analyst", use_case.primary_users)
        self.assertEqual(use_case.target, "generic_sql")

    def test_load_use_case_rejects_missing_required_fields(self) -> None:
        invalid_yaml = textwrap.dedent(
            """
            use_case:
              use_case_id: invalid_case
              primary_users:
                - fraud analyst
            """
        ).strip()

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "invalid.yaml"
            path.write_text(invalid_yaml + "\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                load_use_case(path)

        self.assertIn("missing required fields", str(context.exception))


if __name__ == "__main__":
    unittest.main()
