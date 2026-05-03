from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SqlValidationFinding:
    view_name: str
    required_columns: list[str]
    result: str
    issue: str | None = None


class SqlValidationError(ValueError):
    def __init__(self, findings: list[SqlValidationFinding]) -> None:
        self.findings = findings
        summary = "; ".join(f"{finding.view_name}: {finding.issue}" for finding in findings if finding.issue)
        super().__init__(f"SQL validation failed: {summary}")


REQUIRED_SQL_VIEWS = {
    "certified_customer": ["customer_id", "customer_name", "country", "risk_rating"],
    "certified_account": ["account_id", "customer_id", "account_type", "opened_date"],
    "certified_merchant": ["merchant_id", "merchant_category", "merchant_risk_rating"],
    "certified_fraud_model_run": ["model_run_id", "evaluated_transaction_count", "labelled_fraud_transaction_count"],
    "certified_transaction": ["txn_id", "account_id", "merchant_id", "txn_timestamp", "amount", "fraud_flag"],
    "certified_fraud_signal": [
        "txn_id",
        "account_id",
        "abs_amount",
        "txn_count",
        "same_ts_count",
        "is_spike",
        "is_velocity",
        "predicted_fraud",
        "fraud_score",
    ],
    "certified_fraud_alert": ["alert_id", "txn_id", "account_id", "predicted_fraud", "fraud_score", "primary_alert_reason"],
}


def validate_semantic_sql(sql_text: str) -> dict[str, object]:
    lowered = sql_text.lower()
    findings: list[SqlValidationFinding] = []
    validated_views: list[str] = []

    for view_name, required_columns in REQUIRED_SQL_VIEWS.items():
        section = extract_view_section(lowered, view_name)
        if section is None:
            findings.append(
                SqlValidationFinding(
                    view_name=view_name,
                    required_columns=required_columns,
                    result="failed",
                    issue=f"Missing required view: {view_name}",
                )
            )
            continue

        missing_columns = [column for column in required_columns if column.lower() not in section]
        if missing_columns:
            findings.append(
                SqlValidationFinding(
                    view_name=view_name,
                    required_columns=required_columns,
                    result="failed",
                    issue=f"Missing required columns for {view_name}: {', '.join(missing_columns)}",
                )
            )
            continue

        validated_views.append(view_name)
        findings.append(
            SqlValidationFinding(
                view_name=view_name,
                required_columns=required_columns,
                result="passed",
            )
        )

    failed = [finding for finding in findings if finding.result == "failed"]
    if failed:
        raise SqlValidationError(failed)

    return {
        "sql_validation": {
            "status": "passed",
            "validated_views": validated_views,
            "checks": [
                {
                    "view_name": finding.view_name,
                    "required_columns": finding.required_columns,
                    "result": finding.result,
                }
                for finding in findings
            ],
        }
    }


def extract_view_section(sql_text: str, view_name: str) -> str | None:
    marker = f"create or replace view {view_name} as"
    start = sql_text.find(marker)
    if start == -1:
        return None
    next_start = sql_text.find("create or replace view ", start + len(marker))
    if next_start == -1:
        next_start = len(sql_text)
    return sql_text[start:next_start]
