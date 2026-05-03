from pathlib import Path
import tempfile
import textwrap
import unittest

from semantic_foundry.generators.dq_rule_generator import build_dq_rules
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.validators.dq_validator import validate_dq_rules


class DqValidatorTests(unittest.TestCase):
    def test_accepts_fixture_data_and_returns_passed_report(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))
        report = validate_dq_rules(
            use_case=use_case,
            source_path=Path("examples/business_banking_fraud/source"),
            dq_rules_artefact=build_dq_rules(use_case),
        )

        self.assertEqual(report.status, "passed")
        self.assertEqual(report.blocking_findings, [])
        self.assertEqual(len(report.checks), 5)
        self.assertIn("merchants", report.evaluated_datasets)

    def test_returns_blocking_failure_for_duplicate_transaction_primary_key(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_root = Path(tmp_dir)
            self.write_fixture_csvs(
                source_root,
                transactions_csv="""
                txn_id,account_id,merchant_id,timestamp,amount,transaction_type,merchant_category,merchant_risk_rating,fraud_label
                TXN001,ACC001,M001,2026-04-01T09:15:00+10:00,4200.5,card_present,office_supplies,low,false
                TXN001,ACC002,M002,2026-04-01T09:16:00+10:00,18000.0,wire,logistics,medium,true
                """,
            )

            report = validate_dq_rules(
                use_case=use_case,
                source_path=source_root,
                dq_rules_artefact=build_dq_rules(use_case),
            )

        self.assertEqual(report.status, "failed")
        self.assertEqual(len(report.blocking_findings), 1)
        self.assertEqual(report.blocking_findings[0].rule_id, "dq_transactions_primary_key")

    def test_returns_non_blocking_warning_for_unparseable_timestamp(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_root = Path(tmp_dir)
            self.write_fixture_csvs(
                source_root,
                transactions_csv="""
                txn_id,account_id,merchant_id,timestamp,amount,transaction_type,merchant_category,merchant_risk_rating,fraud_label
                TXN001,ACC001,M001,not-a-timestamp,4200.5,card_present,office_supplies,low,false
                TXN002,ACC002,M002,2026-04-01T09:16:00+10:00,18000.0,wire,logistics,medium,true
                """,
            )

            report = validate_dq_rules(
                use_case=use_case,
                source_path=source_root,
                dq_rules_artefact=build_dq_rules(use_case),
            )

        self.assertEqual(report.status, "warning")
        self.assertEqual(report.blocking_findings, [])
        self.assertEqual(len(report.findings), 1)
        self.assertEqual(report.findings[0].rule_id, "dq_transactions_timestamp")
        self.assertFalse(report.findings[0].blocking)

    def write_fixture_csvs(self, source_root: Path, transactions_csv: str) -> None:
        (source_root / "customers.csv").write_text(
            textwrap.dedent(
                """
                customer_id,customer_name,country,risk_rating
                CUST001,Acme Pty Ltd,AU,medium
                CUST002,Harbour Trading,AU,high
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (source_root / "accounts.csv").write_text(
            textwrap.dedent(
                """
                account_id,customer_id,account_name,account_status
                ACC001,CUST001,Operating Account,active
                ACC002,CUST002,Collections Account,active
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (source_root / "merchants.csv").write_text(
            textwrap.dedent(
                """
                merchant_id,merchant_name,merchant_category,merchant_risk_rating
                M001,Northwind Supplies,office_supplies,low
                M002,Global Freight,logistics,medium
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (source_root / "transactions.csv").write_text(
            textwrap.dedent(transactions_csv).strip() + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
