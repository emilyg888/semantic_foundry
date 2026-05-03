from pathlib import Path
import tempfile
import textwrap
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build
from semantic_foundry.validators.source_schema_validator import SourceSchemaValidationError


class SourceSchemaBuildFailureIntegrationTests(unittest.TestCase):
    def test_build_fails_when_required_detector_source_is_missing(self) -> None:
        use_case_path = Path("examples/business_banking_fraud/use_case.yaml")

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_root = Path(tmp_dir) / "source"
            fraud_dir = source_root / "fraud"
            fraud_dir.mkdir(parents=True, exist_ok=True)
            (fraud_dir / "features.py").write_text(
                textwrap.dedent(
                    """
                    def build_features():
                        abs_amount = 1
                        return {"abs_amount": abs_amount}
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(SourceSchemaValidationError) as context:
                build(
                    BuildRequest(
                        source_path=source_root,
                        use_case_path=use_case_path,
                        output_root=Path(tmp_dir) / "outputs",
                        target="generic_sql",
                    )
                )

        self.assertIn("fraud/detector.py", str(context.exception))
