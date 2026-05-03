import unittest

from semantic_foundry.validators.sql_validator import SqlValidationError, validate_semantic_sql


VALID_SQL = """
create or replace view certified_customer as
select customer_id, customer_name, country, risk_rating from customers;
create or replace view certified_account as
select account_id, customer_id, account_type, opened_date from accounts;
create or replace view certified_merchant as
select merchant_id, merchant_category, merchant_risk_rating from transactions;
create or replace view certified_fraud_model_run as
select model_run_id, evaluated_transaction_count, labelled_fraud_transaction_count from model_runs;
create or replace view certified_transaction as
select txn_id, account_id, merchant_id, txn_timestamp, amount, fraud_flag from transactions;
create or replace view certified_fraud_signal as
select txn_id, account_id, abs_amount, txn_count, same_ts_count, is_spike, is_velocity, predicted_fraud, fraud_score from scored;
create or replace view certified_fraud_alert as
select alert_id, txn_id, account_id, predicted_fraud, fraud_score, primary_alert_reason from alerts;
"""


class SqlValidatorTests(unittest.TestCase):
    def test_validate_semantic_sql_accepts_required_views_and_columns(self) -> None:
        report = validate_semantic_sql(VALID_SQL)

        self.assertEqual(report["sql_validation"]["status"], "passed")
        self.assertIn("certified_transaction", report["sql_validation"]["validated_views"])
        self.assertIn("certified_fraud_alert", report["sql_validation"]["validated_views"])
        self.assertEqual(len(report["sql_validation"]["checks"]), 7)

    def test_validate_semantic_sql_rejects_missing_required_view(self) -> None:
        broken_sql = VALID_SQL.replace("create or replace view certified_merchant as", "-- removed merchant view")

        with self.assertRaises(SqlValidationError) as context:
            validate_semantic_sql(broken_sql)

        self.assertIn("Missing required view: certified_merchant", str(context.exception))

    def test_validate_semantic_sql_rejects_missing_required_column(self) -> None:
        broken_sql = VALID_SQL.replace("fraud_flag", "")

        with self.assertRaises(SqlValidationError) as context:
            validate_semantic_sql(broken_sql)

        self.assertIn("Missing required columns for certified_transaction: fraud_flag", str(context.exception))


if __name__ == "__main__":
    unittest.main()
