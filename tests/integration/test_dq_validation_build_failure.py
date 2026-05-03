from pathlib import Path
import shutil
import tempfile
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build
from semantic_foundry.validators.dq_validator import DqValidationError


class DqValidationBuildFailureIntegrationTests(unittest.TestCase):
    def test_build_fails_when_transactions_primary_key_is_not_unique(self) -> None:
        fixture_root = Path("examples/business_banking_fraud/source")
        use_case_path = Path("examples/business_banking_fraud/use_case.yaml")

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_root = Path(tmp_dir) / "source"
            shutil.copytree(fixture_root, source_root)
            (source_root / "transactions.csv").write_text(
                "\n".join(
                    [
                        "txn_id,account_id,merchant_id,timestamp,amount,transaction_type,merchant_category,merchant_risk_rating,fraud_label",
                        "TXN001,ACC001,M001,2026-04-01T09:15:00+10:00,4200.5,card_present,office_supplies,low,false",
                        "TXN001,ACC002,M002,2026-04-01T09:16:00+10:00,18000.0,wire,logistics,medium,true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(DqValidationError) as context:
                build(
                    BuildRequest(
                        source_path=source_root,
                        use_case_path=use_case_path,
                        output_root=Path(tmp_dir) / "outputs",
                        target="generic_sql",
                    )
                )

        self.assertIn("dq_transactions_primary_key", str(context.exception))


if __name__ == "__main__":
    unittest.main()
