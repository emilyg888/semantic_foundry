from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from semantic_foundry.simple_yaml import load_simple_yaml
from semantic_foundry.validators.dq_validator import DqValidationFinding
from semantic_foundry.validators.policy_validator import PolicyValidationFinding
from semantic_foundry.validators.source_schema_validator import SourceSchemaFinding


@dataclass(slots=True)
class CertificationRequirement:
    name: str
    passed: bool
    detail: str

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


@dataclass(slots=True)
class CertificationGateReport:
    result: str
    validation_status: str
    requirements: list[CertificationRequirement]
    blockers: list[str]
    asset_stage_counts: dict[str, int]

    def as_dict(self) -> dict[str, object]:
        return {
            "certification_gate": {
                "asset": "semantic_package",
                "required": {requirement.name: requirement.passed for requirement in self.requirements},
                "details": [requirement.as_dict() for requirement in self.requirements],
                "blockers": self.blockers,
                "validation_status": self.validation_status,
                "asset_stage_counts": self.asset_stage_counts,
                "result": self.result,
            }
        }


REQUIRED_CERTIFICATION_FILES = {
    "glossary": "01_semantic_catalogue/glossary.yaml",
    "entities": "01_semantic_catalogue/entities.yaml",
    "signals": "02_signal_catalogue/signals.yaml",
    "predictions": "03_prediction_catalogue/predictions.yaml",
    "metrics": "04_evaluation_metric_catalogue/metrics.yaml",
    "policies": "05_governance_controls/policies.yaml",
    "dq_validation": "05_governance_controls/dq_validation.yaml",
    "policy_validation": "05_governance_controls/policy_validation.yaml",
    "sql_validation": "05_governance_controls/sql_validation.yaml",
    "issue_register": "05_governance_controls/issue_register.yaml",
    "ai_context_cards": "06_ai_consumption/ai_context_cards.yaml",
}


def build_issue_register(
    source_schema_findings: list[SourceSchemaFinding] | None = None,
    dq_findings: list[DqValidationFinding] | None = None,
    policy_findings: list[PolicyValidationFinding] | None = None,
) -> dict[str, object]:
    issues = [
        {
            "severity": "high",
            "asset": "fraud_precision",
            "issue": "Synthetic fraud labels are suitable for accelerator validation only.",
            "blocking": True,
            "status": "open",
        },
        {
            "severity": "medium",
            "asset": "account_had_burst",
            "issue": "Experimental signal requires calibration on production history.",
            "blocking": False,
            "status": "open",
        },
    ]
    for finding in source_schema_findings or []:
        issues.append(
            {
                "severity": finding.severity,
                "asset": finding.asset,
                "issue": finding.issue,
                "blocking": finding.blocking,
                "status": "open",
            }
        )
    for finding in dq_findings or []:
        issues.append(
            {
                "severity": finding.severity,
                "asset": finding.asset,
                "issue": finding.issue,
                "blocking": finding.blocking,
                "status": "open",
            }
        )
    for finding in policy_findings or []:
        issues.append(
            {
                "severity": finding.severity,
                "asset": finding.check_id,
                "issue": finding.issue,
                "blocking": finding.blocking,
                "status": "open",
            }
        )
    return {"issues": issues}


def evaluate_certification_gate(artefacts: dict[str, object]) -> CertificationGateReport:
    glossary_terms = list(artefacts["glossary"]["generated_terms"])  # type: ignore[index]
    entities = list(artefacts["entities"]["entities"])  # type: ignore[index]
    signals = list(artefacts["signals"]["signals"])  # type: ignore[index]
    predictions = list(artefacts["predictions"]["predictions"])  # type: ignore[index]
    metrics = list(artefacts["metrics"]["metrics"])  # type: ignore[index]
    policies = list(artefacts["policies"]["policies"])  # type: ignore[index]
    ai_context_cards = list(artefacts["ai_context_cards"]["ai_context_cards"])  # type: ignore[index]
    issues = list(artefacts["issue_register"]["issues"])  # type: ignore[index]

    business_definition_approved = statuses_all_at_or_above(glossary_terms, "review_status", {"candidate"}) and statuses_all_at_or_above(
        entities, "review_status", {"candidate"}
    )
    owner_assigned = owners_present(glossary_terms + entities + signals + predictions + metrics)
    dq_rules_passed = nested_status_equals(artefacts["dq_validation"], "dq_validation", "passed")  # type: ignore[arg-type]
    sensitivity_classified = all(str(term.get("sensitivity", "")).strip() for term in glossary_terms if isinstance(term, dict))
    policy_rules_defined = bool(policies) and nested_status_equals(artefacts["policy_validation"], "policy_validation", "passed")  # type: ignore[arg-type]
    ai_context_card_created = bool(ai_context_cards)
    lineage_documented = all(
        isinstance(asset, dict) and isinstance(asset.get("source_references"), list) and bool(asset["source_references"])
        for asset in entities + signals + predictions + metrics
    )
    threshold_approved = statuses_all_at_or_above(signals + predictions + metrics, "status", {"candidate"})

    requirements = [
        CertificationRequirement(
            name="business_definition_approved",
            passed=business_definition_approved,
            detail="Glossary and entity review statuses must be promoted to candidate.",
        ),
        CertificationRequirement(
            name="owner_assigned",
            passed=owner_assigned,
            detail="All semantic assets require an assigned owner.",
        ),
        CertificationRequirement(
            name="dq_rules_passed",
            passed=dq_rules_passed,
            detail="DQ validation must pass with no blocking failures.",
        ),
        CertificationRequirement(
            name="sensitivity_classified",
            passed=sensitivity_classified,
            detail="Glossary terms must carry sensitivity classification.",
        ),
        CertificationRequirement(
            name="policy_rules_defined",
            passed=policy_rules_defined,
            detail="Policy validation must pass for restricted assets and review controls.",
        ),
        CertificationRequirement(
            name="ai_context_card_created",
            passed=ai_context_card_created,
            detail="At least one AI context card must exist.",
        ),
        CertificationRequirement(
            name="lineage_documented",
            passed=lineage_documented,
            detail="Generated assets require source references for traceability.",
        ),
        CertificationRequirement(
            name="threshold_approved",
            passed=threshold_approved,
            detail="Signals, predictions, and metrics must be promoted beyond draft or experimental status.",
        ),
    ]

    validation_status = (
        "passed"
        if nested_status_equals(artefacts["dq_validation"], "dq_validation", "passed")  # type: ignore[arg-type]
        and nested_status_equals(artefacts["policy_validation"], "policy_validation", "passed")  # type: ignore[arg-type]
        and nested_status_equals(artefacts["sql_validation"], "sql_validation", "passed")  # type: ignore[arg-type]
        else "failed"
    )
    blockers = build_blockers(issues, requirements, validation_status)
    asset_stage_counts = count_asset_stages(glossary_terms, entities, signals, predictions, metrics)

    if blockers:
        result = "not_certifiable"
    elif any(not requirement.passed for requirement in requirements):
        result = "draft"
    else:
        result = "candidate"

    return CertificationGateReport(
        result=result,
        validation_status=validation_status,
        requirements=requirements,
        blockers=blockers,
        asset_stage_counts=asset_stage_counts,
    )


def certify_package(package_path: Path) -> dict[str, object]:
    required_paths = required_certification_paths(package_path)
    missing_files = [str(path.relative_to(package_path)) for path in required_paths.values() if not path.exists()]
    report_path = package_path / "07_delivery_pack" / "certification_report.md"
    manifest_path = package_path / "07_delivery_pack" / "semantic_manifest.yaml"
    if not report_path.exists():
        missing_files.append(str(report_path.relative_to(package_path)))
    if not manifest_path.exists():
        missing_files.append(str(manifest_path.relative_to(package_path)))

    if missing_files:
        return {
            "package_path": str(package_path),
            "certification_report_present": report_path.exists(),
            "semantic_manifest_present": manifest_path.exists(),
            "certification_result": "not_certifiable",
            "validation_status": "failed",
            "blockers": [f"Missing required certification artefact: {filename}" for filename in missing_files],
            "requirements": {},
            "asset_stage_counts": {},
        }

    artefacts = load_certification_artefacts(package_path)
    gate = evaluate_certification_gate(artefacts)
    return {
        "package_path": str(package_path),
        "certification_report_present": report_path.exists(),
        "semantic_manifest_present": manifest_path.exists(),
        "certification_result": gate.result,
        "validation_status": gate.validation_status,
        "blockers": gate.blockers,
        "requirements": {requirement.name: requirement.passed for requirement in gate.requirements},
        "asset_stage_counts": gate.asset_stage_counts,
    }


def statuses_all_at_or_above(items: list[object], key: str, allowed_statuses: set[str]) -> bool:
    relevant = [item for item in items if isinstance(item, dict) and key in item]
    if not relevant:
        return False
    return all(str(item.get(key, "")).lower() in allowed_statuses for item in relevant)


def owners_present(items: list[object]) -> bool:
    return all(isinstance(item, dict) and str(item.get("owner", "")).strip() for item in items)


def nested_status_equals(payload: dict[str, Any], key: str, expected: str) -> bool:
    nested = payload.get(key, {})
    return isinstance(nested, dict) and str(nested.get("status", "")).lower() == expected


def build_blockers(issues: list[object], requirements: list[CertificationRequirement], validation_status: str) -> list[str]:
    blockers = [
        str(issue.get("issue"))
        for issue in issues
        if isinstance(issue, dict)
        and bool(issue.get("blocking"))
        and str(issue.get("status", "open")).lower() != "resolved"
        and str(issue.get("issue", "")).strip()
    ]
    if validation_status != "passed":
        blockers.append("One or more deterministic validation gates failed.")
    for requirement in requirements:
        if not requirement.passed and requirement.name in {"owner_assigned", "dq_rules_passed", "policy_rules_defined", "ai_context_card_created"}:
            blockers.append(f"Required certification condition not met: {requirement.name}")
    return deduplicate_preserving_order(blockers)


def count_asset_stages(
    glossary_terms: list[object],
    entities: list[object],
    signals: list[object],
    predictions: list[object],
    metrics: list[object],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in glossary_terms:
        increment_count(counts, status_for_item(item, "review_status"))
    for item in entities:
        increment_count(counts, status_for_item(item, "certification_status"))
    for item in signals + predictions + metrics:
        increment_count(counts, status_for_item(item, "status"))
    return counts


def status_for_item(item: object, key: str) -> str:
    if not isinstance(item, dict):
        return "unknown"
    return str(item.get(key, "unknown")).lower()


def increment_count(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def deduplicate_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def required_certification_paths(package_path: Path) -> dict[str, Path]:
    return {name: package_path / relative_path for name, relative_path in REQUIRED_CERTIFICATION_FILES.items()}


def load_certification_artefacts(package_path: Path) -> dict[str, object]:
    return {name: load_simple_yaml(path) for name, path in required_certification_paths(package_path).items()}
