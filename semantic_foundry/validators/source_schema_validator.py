from __future__ import annotations

from dataclasses import dataclass

from semantic_foundry.config import InventorySummary, UseCase


@dataclass(slots=True)
class SourceSchemaFinding:
    severity: str
    asset: str
    issue: str
    blocking: bool


@dataclass(slots=True)
class SourceSchemaValidationReport:
    findings: list[SourceSchemaFinding]

    @property
    def blocking_findings(self) -> list[SourceSchemaFinding]:
        return [finding for finding in self.findings if finding.blocking]


class SourceSchemaValidationError(ValueError):
    def __init__(self, findings: list[SourceSchemaFinding]) -> None:
        self.findings = findings
        summary = "; ".join(finding.issue for finding in findings)
        super().__init__(f"Source schema validation failed: {summary}")


REQUIRED_ROLE_BY_PATH = {
    "fraud/features.py": "feature_engineering",
    "fraud/detector.py": "fraud_detector",
}

OPTIONAL_ROLE_BY_PATH = {
    "fraud/run_fraud.py": "evaluation_runner",
}


def validate_source_schema(use_case: UseCase, inventory: InventorySummary) -> SourceSchemaValidationReport:
    findings: list[SourceSchemaFinding] = []
    files_by_path = {item.path: item for item in inventory.files}

    for path, expected_role in REQUIRED_ROLE_BY_PATH.items():
        source_file = files_by_path.get(path)
        if source_file is None:
            findings.append(
                SourceSchemaFinding(
                    severity="critical",
                    asset="source_schema",
                    issue=f"Required source file is missing: {path}",
                    blocking=True,
                )
            )
            continue
        if source_file.category != "python":
            findings.append(
                SourceSchemaFinding(
                    severity="critical",
                    asset="source_schema",
                    issue=f"Required source file has wrong category: {path} must be python.",
                    blocking=True,
                )
            )
        if source_file.role != expected_role:
            findings.append(
                SourceSchemaFinding(
                    severity="critical",
                    asset="source_schema",
                    issue=f"Required source role mismatch for {path}: expected {expected_role}.",
                    blocking=True,
                )
            )

    python_count = inventory.counts_by_category.get("python", 0)
    if python_count < 2:
        findings.append(
            SourceSchemaFinding(
                severity="critical",
                asset="source_schema",
                issue="At least two python source files are required for fraud feature and detector discovery.",
                blocking=True,
            )
        )

    for path, expected_role in OPTIONAL_ROLE_BY_PATH.items():
        source_file = files_by_path.get(path)
        if source_file is None:
            findings.append(
                SourceSchemaFinding(
                    severity="medium",
                    asset="source_schema",
                    issue=f"Optional source role not found: {expected_role} ({path}). Model-run semantics remain inferred.",
                    blocking=False,
                )
            )

    if not use_case.source_dataset_names:
        findings.append(
            SourceSchemaFinding(
                severity="high",
                asset="source_schema",
                issue="Use case does not declare source dataset names.",
                blocking=True,
            )
        )

    report = SourceSchemaValidationReport(findings=findings)
    if report.blocking_findings:
        raise SourceSchemaValidationError(report.blocking_findings)
    return report
