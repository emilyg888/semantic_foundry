from __future__ import annotations

import json
from pathlib import Path

from semantic_foundry.simple_yaml import dump_yaml


FILE_PATH_BY_ARTEFACT = {
    "glossary": "01_semantic_catalogue/glossary.yaml",
    "entities": "01_semantic_catalogue/entities.yaml",
    "relationships": "01_semantic_catalogue/relationships.yaml",
    "signals": "02_signal_catalogue/signals.yaml",
    "predictions": "03_prediction_catalogue/predictions.yaml",
    "metrics": "04_evaluation_metric_catalogue/metrics.yaml",
    "dq_rules": "05_governance_controls/dq_rules.yaml",
    "dq_validation": "05_governance_controls/dq_validation.yaml",
    "policies": "05_governance_controls/policies.yaml",
    "policy_validation": "05_governance_controls/policy_validation.yaml",
    "issue_register": "05_governance_controls/issue_register.yaml",
    "sql_validation": "05_governance_controls/sql_validation.yaml",
    "ai_context_cards": "06_ai_consumption/ai_context_cards.yaml",
    "semantic_manifest": "07_delivery_pack/semantic_manifest.yaml",
}
DELIVERY_PACK_FILES = {
    "semantic_views.sql": "07_delivery_pack/semantic_views.sql",
    "certification_report.md": "07_delivery_pack/certification_report.md",
}
PACKAGE_INDEX_FILE = "README.md"
ROOT_PACKAGE_FILES = {
    "package_manifest": ("package_manifest.yaml", "yaml"),
    "use_case_package": ("use_case.yaml", "yaml"),
    "discovery_report": ("discovery_report.json", "json"),
    "semantic_catalogue": ("semantic_catalogue.yaml", "yaml"),
    "signal_catalogue": ("signal_catalogue.yaml", "yaml"),
    "metric_catalogue": ("metric_catalogue.yaml", "yaml"),
    "dq_rules_package": ("dq_rules.yaml", "yaml"),
    "policy_rules_package": ("policy_rules.yaml", "yaml"),
    "lineage": ("lineage.yaml", "yaml"),
    "ai_context_cards_package": ("ai_context_cards.yaml", "yaml"),
    "evaluation_questions": ("evaluation_questions.yaml", "yaml"),
}
ROOT_TEXT_FILES = {
    "semantic_views.sql": "semantic_views.sql",
    "certification_report.md": "certification_report.md",
}


def expected_generated_assets() -> list[str]:
    return (
        [PACKAGE_INDEX_FILE]
        + [path for path, _ in ROOT_PACKAGE_FILES.values()]
        + list(ROOT_TEXT_FILES.values())
        + list(FILE_PATH_BY_ARTEFACT.values())
        + list(DELIVERY_PACK_FILES.values())
    )


def publish_package(
    output_dir: Path,
    artefacts: dict[str, object],
    semantic_sql: str,
    certification_report: str,
    package_index: str,
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_assets: list[str] = []

    index_target = output_dir / PACKAGE_INDEX_FILE
    index_target.write_text(package_index, encoding="utf-8")
    generated_assets.append(PACKAGE_INDEX_FILE)

    for artefact_name, (filename, file_format) in ROOT_PACKAGE_FILES.items():
        payload = artefacts[artefact_name]
        target = output_dir / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        if file_format == "json":
            target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        else:
            target.write_text(dump_yaml(payload) + "\n", encoding="utf-8")
        generated_assets.append(filename)

    root_sql_target = output_dir / ROOT_TEXT_FILES["semantic_views.sql"]
    root_sql_target.write_text(semantic_sql, encoding="utf-8")
    generated_assets.append(ROOT_TEXT_FILES["semantic_views.sql"])

    root_report_target = output_dir / ROOT_TEXT_FILES["certification_report.md"]
    root_report_target.write_text(certification_report, encoding="utf-8")
    generated_assets.append(ROOT_TEXT_FILES["certification_report.md"])

    for artefact_name, filename in FILE_PATH_BY_ARTEFACT.items():
        payload = artefacts[artefact_name]
        target = output_dir / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(dump_yaml(payload) + "\n", encoding="utf-8")
        generated_assets.append(filename)

    sql_target = output_dir / DELIVERY_PACK_FILES["semantic_views.sql"]
    sql_target.parent.mkdir(parents=True, exist_ok=True)
    sql_target.write_text(semantic_sql, encoding="utf-8")
    generated_assets.append(DELIVERY_PACK_FILES["semantic_views.sql"])

    report_target = output_dir / DELIVERY_PACK_FILES["certification_report.md"]
    report_target.parent.mkdir(parents=True, exist_ok=True)
    report_target.write_text(certification_report, encoding="utf-8")
    generated_assets.append(DELIVERY_PACK_FILES["certification_report.md"])
    return generated_assets
