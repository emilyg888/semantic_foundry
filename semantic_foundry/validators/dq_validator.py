from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from semantic_foundry.config import UseCase


@dataclass(slots=True)
class DqValidationFinding:
    rule_id: str
    asset: str
    severity: str
    issue: str
    blocking: bool
    checked_rows: int
    invalid_row_count: int


@dataclass(slots=True)
class DqRuleCheck:
    rule_id: str
    asset: str
    severity: str
    blocking: bool
    status: str
    checked_rows: int
    invalid_row_count: int
    detail: str

    def as_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "asset": self.asset,
            "severity": self.severity,
            "blocking": self.blocking,
            "status": self.status,
            "checked_rows": self.checked_rows,
            "invalid_row_count": self.invalid_row_count,
            "detail": self.detail,
        }


@dataclass(slots=True)
class DqValidationReport:
    use_case_id: str
    evaluated_datasets: list[str]
    checks: list[DqRuleCheck]
    findings: list[DqValidationFinding]

    @property
    def blocking_findings(self) -> list[DqValidationFinding]:
        return [finding for finding in self.findings if finding.blocking]

    @property
    def status(self) -> str:
        if self.blocking_findings:
            return "failed"
        if self.findings:
            return "warning"
        return "passed"

    def as_artefact(self) -> dict[str, object]:
        return {
            "use_case_id": self.use_case_id,
            "dq_validation": {
                "status": self.status,
                "evaluated_datasets": self.evaluated_datasets,
                "checks": [check.as_dict() for check in self.checks],
                "failed_checks": [
                    {
                        "rule_id": finding.rule_id,
                        "asset": finding.asset,
                        "severity": finding.severity,
                        "blocking": finding.blocking,
                        "issue": finding.issue,
                        "checked_rows": finding.checked_rows,
                        "invalid_row_count": finding.invalid_row_count,
                    }
                    for finding in self.findings
                ],
            },
        }

    def raise_if_blocking(self) -> None:
        if not self.blocking_findings:
            return
        failures = ", ".join(
            f"{finding.rule_id} ({finding.invalid_row_count} invalid rows)"
            for finding in self.blocking_findings
        )
        raise DqValidationError(f"Blocking DQ validation failures: {failures}")


class DqValidationError(ValueError):
    """Raised when blocking DQ validation failures are detected."""


def validate_dq_rules(
    use_case: UseCase,
    source_path: Path,
    dq_rules_artefact: dict[str, object],
) -> DqValidationReport:
    datasets = load_datasets(source_path, use_case.source_dataset_names)
    rules = {
        rule["rule_id"]: rule
        for rule in dq_rules_artefact["dq_rules"]  # type: ignore[index]
        if isinstance(rule, dict) and "rule_id" in rule
    }

    customer_ids = collect_non_empty_values(datasets["customers"], "customer_id")
    account_ids = collect_non_empty_values(datasets["accounts"], "account_id")
    merchant_ids = collect_non_empty_values(datasets["merchants"], "merchant_id")

    checks = [
        evaluate_primary_key_rule(
            rule=rules["dq_transactions_primary_key"],
            rows=datasets["transactions"],
            key="txn_id",
        ),
        evaluate_foreign_key_rule(
            rule=rules["dq_accounts_customer_fk"],
            rows=datasets["accounts"],
            key="customer_id",
            valid_values=customer_ids,
            allow_blank=False,
        ),
        evaluate_foreign_key_rule(
            rule=rules["dq_transactions_account_fk"],
            rows=datasets["transactions"],
            key="account_id",
            valid_values=account_ids,
            allow_blank=False,
        ),
        evaluate_timestamp_rule(
            rule=rules["dq_transactions_timestamp"],
            rows=datasets["transactions"],
            key="timestamp",
        ),
        evaluate_foreign_key_rule(
            rule=rules["dq_transactions_merchant_fk"],
            rows=datasets["transactions"],
            key="merchant_id",
            valid_values=merchant_ids,
            allow_blank=True,
        ),
    ]

    findings = [
        DqValidationFinding(
            rule_id=check.rule_id,
            asset=check.asset,
            severity=check.severity,
            issue=check.detail,
            blocking=check.blocking,
            checked_rows=check.checked_rows,
            invalid_row_count=check.invalid_row_count,
        )
        for check in checks
        if check.status != "passed"
    ]

    return DqValidationReport(
        use_case_id=use_case.use_case_id,
        evaluated_datasets=sorted(datasets),
        checks=checks,
        findings=findings,
    )


def load_datasets(source_path: Path, dataset_names: list[str]) -> dict[str, list[dict[str, str]]]:
    if not dataset_names:
        raise DqValidationError("Use case must declare source datasets for DQ validation")

    datasets: dict[str, list[dict[str, str]]] = {}
    for dataset_name in dataset_names:
        dataset_path = resolve_dataset_path(source_path, dataset_name)
        with dataset_path.open(encoding="utf-8", newline="") as handle:
            datasets[dataset_name] = list(csv.DictReader(handle))
    return datasets


def resolve_dataset_path(source_path: Path, dataset_name: str) -> Path:
    direct_path = source_path / f"{dataset_name}.csv"
    if direct_path.exists():
        return direct_path

    matches = sorted(source_path.rglob(f"{dataset_name}.csv"))
    if not matches:
        raise DqValidationError(f"Missing dataset file for DQ validation: {dataset_name}.csv")
    if len(matches) > 1:
        raise DqValidationError(f"Multiple dataset files found for DQ validation: {dataset_name}.csv")
    return matches[0]


def collect_non_empty_values(rows: list[dict[str, str]], key: str) -> set[str]:
    return {row.get(key, "").strip() for row in rows if row.get(key, "").strip()}


def evaluate_primary_key_rule(
    rule: dict[str, object],
    rows: list[dict[str, str]],
    key: str,
) -> DqRuleCheck:
    seen: set[str] = set()
    invalid_row_count = 0
    for row in rows:
        value = row.get(key, "").strip()
        if not value or value in seen:
            invalid_row_count += 1
            continue
        seen.add(value)
    return build_rule_check(rule, len(rows), invalid_row_count)


def evaluate_foreign_key_rule(
    rule: dict[str, object],
    rows: list[dict[str, str]],
    key: str,
    valid_values: set[str],
    allow_blank: bool,
) -> DqRuleCheck:
    invalid_row_count = 0
    for row in rows:
        value = row.get(key, "").strip()
        if not value and allow_blank:
            continue
        if not value or value not in valid_values:
            invalid_row_count += 1
    return build_rule_check(rule, len(rows), invalid_row_count)


def evaluate_timestamp_rule(
    rule: dict[str, object],
    rows: list[dict[str, str]],
    key: str,
) -> DqRuleCheck:
    invalid_row_count = 0
    for row in rows:
        value = row.get(key, "").strip()
        if not value or not is_parseable_timestamp(value):
            invalid_row_count += 1
    return build_rule_check(rule, len(rows), invalid_row_count)


def build_rule_check(
    rule: dict[str, object],
    checked_rows: int,
    invalid_row_count: int,
) -> DqRuleCheck:
    severity = str(rule["severity"])
    blocking = severity == "critical"
    status = "failed" if invalid_row_count else "passed"
    detail = str(rule["check"])
    if invalid_row_count:
        detail = f"{rule['check']} ({invalid_row_count} invalid rows)"
    return DqRuleCheck(
        rule_id=str(rule["rule_id"]),
        asset=str(rule["asset"]),
        severity=severity,
        blocking=blocking,
        status=status,
        checked_rows=checked_rows,
        invalid_row_count=invalid_row_count,
        detail=detail,
    )


def is_parseable_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True
