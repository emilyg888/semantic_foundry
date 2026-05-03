from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from semantic_foundry.builders.report_builder import build_certification_report
from semantic_foundry.review.approval_model import ApprovalRecord, ReviewAsset
from semantic_foundry.simple_yaml import dump_yaml, load_simple_yaml
from semantic_foundry.validators.certification_validator import (
    CertificationGateReport,
    evaluate_certification_gate,
    load_certification_artefacts,
)


REVIEW_APPROVALS_FILE = "05_governance_controls/review_approvals.yaml"
PUBLISH_LOG_FILE = "07_delivery_pack/publish_log.yaml"
REVIEWABLE_FILES = {
    "glossary": ("01_semantic_catalogue/glossary.yaml", "generated_terms"),
    "entities": ("01_semantic_catalogue/entities.yaml", "entities"),
    "signals": ("02_signal_catalogue/signals.yaml", "signals"),
    "predictions": ("03_prediction_catalogue/predictions.yaml", "predictions"),
    "metrics": ("04_evaluation_metric_catalogue/metrics.yaml", "metrics"),
}
ISSUE_REGISTER_FILE = "05_governance_controls/issue_register.yaml"
MANIFEST_FILE = "07_delivery_pack/semantic_manifest.yaml"
REPORT_FILE = "07_delivery_pack/certification_report.md"


@dataclass(slots=True)
class PackageReviewState:
    package_path: Path
    artefacts: dict[str, object]
    review_assets: list[ReviewAsset]
    approvals: list[dict[str, object]]
    issues: list[dict[str, object]]
    gate: CertificationGateReport


def load_package_review_state(package_path: Path) -> PackageReviewState:
    artefacts = load_certification_artefacts(package_path)
    review_assets = collect_review_assets(artefacts)
    approvals_payload = load_optional_yaml(package_path / REVIEW_APPROVALS_FILE, {"approvals": []})
    issue_register = artefacts["issue_register"]
    gate = evaluate_certification_gate(artefacts)
    return PackageReviewState(
        package_path=package_path,
        artefacts=artefacts,
        review_assets=review_assets,
        approvals=list(approvals_payload.get("approvals", [])),
        issues=list(issue_register.get("issues", [])),  # type: ignore[union-attr]
        gate=gate,
    )


def approve_asset(package_path: Path, asset_type: str, asset_id: str, reviewer: str, comments: str = "") -> None:
    update_asset(
        package_path=package_path,
        asset_type=asset_type,
        asset_id=asset_id,
        reviewer=reviewer,
        comments=comments,
        decision="approved",
        target_status="candidate",
    )


def reject_asset(
    package_path: Path,
    asset_type: str,
    asset_id: str,
    reviewer: str,
    comments: str,
    blocking: bool,
    severity: str,
) -> None:
    update_asset(
        package_path=package_path,
        asset_type=asset_type,
        asset_id=asset_id,
        reviewer=reviewer,
        comments=comments,
        decision="rejected",
        target_status="draft",
    )
    if comments.strip():
        add_issue(
            package_path=package_path,
            asset=asset_id,
            issue=comments.strip(),
            severity=severity,
            blocking=blocking,
            reported_by=reviewer,
        )


def update_owner(package_path: Path, asset_type: str, asset_id: str, owner: str) -> None:
    path, collection_key = reviewable_path_and_key(asset_type)
    payload = load_simple_yaml(package_path / path)
    item = find_asset_item(payload[collection_key], asset_type, asset_id)  # type: ignore[index]
    item["owner"] = owner
    write_yaml(package_path / path, payload)
    refresh_delivery_pack(package_path)


def add_issue(
    package_path: Path,
    asset: str,
    issue: str,
    severity: str,
    blocking: bool,
    reported_by: str,
) -> None:
    issue_register_path = package_path / ISSUE_REGISTER_FILE
    payload = load_simple_yaml(issue_register_path)
    issues = list(payload.get("issues", []))
    issues.append(
        {
            "severity": severity,
            "asset": asset,
            "issue": issue,
            "blocking": blocking,
            "status": "open",
            "reported_by": reported_by,
            "updated_at": timestamp_now(),
        }
    )
    payload["issues"] = issues
    write_yaml(issue_register_path, payload)
    refresh_delivery_pack(package_path)


def resolve_issue(package_path: Path, issue_text: str, resolver: str, resolution_note: str = "") -> None:
    issue_register_path = package_path / ISSUE_REGISTER_FILE
    payload = load_simple_yaml(issue_register_path)
    issues = list(payload.get("issues", []))
    for issue in issues:
        if str(issue.get("issue")) != issue_text:
            continue
        issue["status"] = "resolved"
        issue["blocking"] = False
        issue["resolved_by"] = resolver
        issue["resolution_note"] = resolution_note
        issue["updated_at"] = timestamp_now()
        break
    payload["issues"] = issues
    write_yaml(issue_register_path, payload)
    refresh_delivery_pack(package_path)


def publish_review_package(package_path: Path, publisher: str, notes: str = "") -> CertificationGateReport:
    gate = refresh_delivery_pack(package_path)
    publish_log_path = package_path / PUBLISH_LOG_FILE
    payload = load_optional_yaml(publish_log_path, {"publish_events": []})
    events = list(payload.get("publish_events", []))
    events.append(
        {
            "published_by": publisher,
            "notes": notes,
            "published_at": timestamp_now(),
            "certification_result": gate.result,
            "validation_status": gate.validation_status,
        }
    )
    payload["publish_events"] = events
    write_yaml(publish_log_path, payload)
    return gate


def refresh_delivery_pack(package_path: Path) -> CertificationGateReport:
    artefacts = load_certification_artefacts(package_path)
    gate = evaluate_certification_gate(artefacts)
    manifest_path = package_path / MANIFEST_FILE
    manifest = load_simple_yaml(manifest_path)
    manifest["run"]["validation_status"] = gate.validation_status  # type: ignore[index]
    manifest["run"]["certification_status"] = gate.result  # type: ignore[index]
    manifest["run"]["last_reviewed_at"] = timestamp_now()  # type: ignore[index]
    write_yaml(manifest_path, manifest)
    report_path = package_path / REPORT_FILE
    report_path.write_text(
        build_certification_report(extract_use_case_id(artefacts), gate),
        encoding="utf-8",
    )
    return gate


def collect_review_assets(artefacts: dict[str, object]) -> list[ReviewAsset]:
    assets: list[ReviewAsset] = []
    assets.extend(
        build_review_assets(
            artefacts["glossary"]["generated_terms"],  # type: ignore[index]
            asset_type="glossary",
            file_key="glossary",
            id_key="term",
            name_key="term",
            status_key="review_status",
        )
    )
    assets.extend(
        build_review_assets(
            artefacts["entities"]["entities"],  # type: ignore[index]
            asset_type="entities",
            file_key="entities",
            id_key="entity_id",
            name_key="name",
            status_key="review_status",
        )
    )
    assets.extend(
        build_review_assets(
            artefacts["signals"]["signals"],  # type: ignore[index]
            asset_type="signals",
            file_key="signals",
            id_key="signal_id",
            name_key="signal_id",
            status_key="status",
        )
    )
    assets.extend(
        build_review_assets(
            artefacts["predictions"]["predictions"],  # type: ignore[index]
            asset_type="predictions",
            file_key="predictions",
            id_key="prediction_id",
            name_key="name",
            status_key="status",
        )
    )
    assets.extend(
        build_review_assets(
            artefacts["metrics"]["metrics"],  # type: ignore[index]
            asset_type="metrics",
            file_key="metrics",
            id_key="metric_id",
            name_key="name",
            status_key="status",
        )
    )
    return assets


def build_review_assets(
    items: object,
    asset_type: str,
    file_key: str,
    id_key: str,
    name_key: str,
    status_key: str,
) -> list[ReviewAsset]:
    if not isinstance(items, list):
        return []
    review_assets: list[ReviewAsset] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        review_assets.append(
            ReviewAsset(
                asset_type=asset_type,
                asset_id=str(item.get(id_key, "")),
                display_name=str(item.get(name_key, item.get(id_key, ""))),
                owner=str(item.get("owner", "")),
                status=str(item.get(status_key, "")),
                file_key=file_key,
                index=index,
                source_references=[str(ref) for ref in item.get("source_references", [])] if isinstance(item.get("source_references"), list) else [],
            )
        )
    return review_assets


def update_asset(
    package_path: Path,
    asset_type: str,
    asset_id: str,
    reviewer: str,
    comments: str,
    decision: str,
    target_status: str,
) -> None:
    path, collection_key = reviewable_path_and_key(asset_type)
    payload = load_simple_yaml(package_path / path)
    item = find_asset_item(payload[collection_key], asset_type, asset_id)  # type: ignore[index]
    if asset_type == "entities":
        item["review_status"] = target_status
        item["certification_status"] = target_status
    elif asset_type == "glossary":
        item["review_status"] = target_status
    else:
        item["status"] = target_status
    write_yaml(package_path / path, payload)
    append_approval_record(package_path, ApprovalRecord(asset_type, asset_id, decision, reviewer, comments, timestamp_now()))
    refresh_delivery_pack(package_path)


def append_approval_record(package_path: Path, record: ApprovalRecord) -> None:
    approvals_path = package_path / REVIEW_APPROVALS_FILE
    payload = load_optional_yaml(approvals_path, {"approvals": []})
    approvals = list(payload.get("approvals", []))
    approvals.append(record.as_dict())
    payload["approvals"] = approvals
    write_yaml(approvals_path, payload)


def reviewable_path_and_key(asset_type: str) -> tuple[str, str]:
    if asset_type not in REVIEWABLE_FILES:
        raise ValueError(f"Unsupported review asset type: {asset_type}")
    return REVIEWABLE_FILES[asset_type]


def find_asset_item(items: object, asset_type: str, asset_id: str) -> dict[str, object]:
    if not isinstance(items, list):
        raise ValueError(f"Review asset collection for {asset_type} is not a list")
    id_key = {
        "glossary": "term",
        "entities": "entity_id",
        "signals": "signal_id",
        "predictions": "prediction_id",
        "metrics": "metric_id",
    }[asset_type]
    for item in items:
        if isinstance(item, dict) and str(item.get(id_key, "")) == asset_id:
            return item
    raise ValueError(f"Could not find {asset_type} asset: {asset_id}")


def extract_use_case_id(artefacts: dict[str, object]) -> str:
    for key in ("glossary", "entities", "signals", "predictions", "metrics"):
        payload = artefacts.get(key)
        if isinstance(payload, dict) and str(payload.get("use_case_id", "")).strip():
            return str(payload["use_case_id"])
    return "unknown_use_case"


def load_optional_yaml(path: Path, default: dict[str, object]) -> dict[str, object]:
    if not path.exists():
        return dict(default)
    return load_simple_yaml(path)


def write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(payload) + "\n", encoding="utf-8")


def timestamp_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
