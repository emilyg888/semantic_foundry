from pathlib import Path
import tempfile
import unittest

from semantic_foundry.config import InventorySummary, SourceFile
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.scanners.source_inventory import build_source_inventory
from semantic_foundry.validators.source_schema_validator import (
    SourceSchemaValidationError,
    validate_source_schema,
)


class SourceSchemaValidatorTests(unittest.TestCase):
    def test_accepts_fixture_and_returns_non_blocking_warning(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        inventory = build_source_inventory(Path("examples/business_banking_fraud/source"))

        report = validate_source_schema(use_case, inventory)

        self.assertEqual(report.blocking_findings, [])
        self.assertTrue(
            any("evaluation_runner" in finding.issue for finding in report.findings),
            "Expected non-blocking evaluation_runner warning",
        )

    def test_rejects_missing_required_detector_file(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        inventory = InventorySummary(
            root="tmp",
            files=[
                SourceFile(
                    path="fraud/features.py",
                    category="python",
                    suffix=".py",
                    role="feature_engineering",
                )
            ],
        )

        with self.assertRaises(SourceSchemaValidationError) as context:
            validate_source_schema(use_case, inventory)

        self.assertIn("Required source file is missing: fraud/detector.py", str(context.exception))


if __name__ == "__main__":
    unittest.main()
