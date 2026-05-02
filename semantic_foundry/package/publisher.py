from __future__ import annotations

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
    "policies": "05_governance_controls/policies.yaml",
    "issue_register": "05_governance_controls/issue_register.yaml",
    "ai_context_cards": "06_ai_consumption/ai_context_cards.yaml",
    "semantic_manifest": "07_delivery_pack/semantic_manifest.yaml",
}
DELIVERY_PACK_FILES = {
    "semantic_views.sql": "07_delivery_pack/semantic_views.sql",
    "certification_report.md": "07_delivery_pack/certification_report.md",
}


def expected_generated_assets() -> list[str]:
    return list(FILE_PATH_BY_ARTEFACT.values()) + list(DELIVERY_PACK_FILES.values())


def publish_package(output_dir: Path, artefacts: dict[str, object], semantic_sql: str, certification_report: str) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_assets: list[str] = []

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
