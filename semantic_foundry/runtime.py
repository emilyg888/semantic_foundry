from __future__ import annotations

import shutil
from pathlib import Path

from semantic_foundry.builders.manifest_builder import build_semantic_manifest
from semantic_foundry.builders.report_builder import build_certification_report
from semantic_foundry.builders.semantic_sql_builder import build_semantic_sql
from semantic_foundry.config import BuildRequest
from semantic_foundry.generators.ai_contract_generator import build_ai_context_cards
from semantic_foundry.generators.dq_rule_generator import build_dq_rules
from semantic_foundry.generators.entity_model_generator import build_entities
from semantic_foundry.generators.glossary_generator import build_glossary
from semantic_foundry.generators.metric_generator import build_metrics
from semantic_foundry.generators.policy_generator import build_policies
from semantic_foundry.generators.prediction_generator import build_predictions
from semantic_foundry.generators.relationship_generator import build_relationships
from semantic_foundry.generators.signal_generator import build_signals
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.package.publisher import expected_generated_assets, publish_package
from semantic_foundry.scanners.python_logic_miner import mine_python_logic
from semantic_foundry.scanners.semantic_classifier import (
    build_governance_context,
    classify_alert_candidates,
    classify_semantic_candidates,
    classify_signal_candidates,
)
from semantic_foundry.scanners.source_inventory import build_source_inventory
from semantic_foundry.validators.artefact_schema_validator import validate_artefacts
from semantic_foundry.validators.certification_validator import build_issue_register


def discover(source_path: Path, use_case_path: Path) -> dict[str, object]:
    use_case = load_use_case(use_case_path)
    inventory = build_source_inventory(source_path)
    logic = mine_python_logic(source_path)
    return {
        "use_case_id": use_case.use_case_id,
        "discovery": {
            "inventory_counts": inventory.counts_by_category,
            "python_functions": [
                {
                    "module_path": function.module_path,
                    "function_name": function.function_name,
                    "assigned_names": function.assigned_names,
                    "return_names": function.return_names,
                }
                for function in logic
            ],
        },
        "semantic_layer_candidates": classify_semantic_candidates(use_case, logic),
        "signal_layer_candidates": classify_signal_candidates(use_case, logic),
        "alert_layer_candidates": classify_alert_candidates(use_case, logic),
        "governance_context": build_governance_context(use_case),
    }


def build(request: BuildRequest) -> Path:
    use_case = load_use_case(request.use_case_path)
    use_case.target = request.target
    inventory = build_source_inventory(request.source_path)
    logic = mine_python_logic(request.source_path)

    artefacts: dict[str, object] = {
        "glossary": build_glossary(use_case, logic),
        "entities": build_entities(use_case),
        "relationships": build_relationships(use_case),
        "signals": build_signals(use_case, logic),
        "predictions": build_predictions(use_case, logic),
        "metrics": build_metrics(use_case),
        "dq_rules": build_dq_rules(use_case),
        "policies": build_policies(use_case),
        "ai_context_cards": build_ai_context_cards(use_case),
        "issue_register": build_issue_register(),
    }

    semantic_sql = build_semantic_sql(use_case)
    certification_report = build_certification_report(use_case)

    manifest = build_semantic_manifest(
        use_case=use_case,
        inventory=inventory,
        generated_assets=expected_generated_assets(),
        source_path=request.source_path,
        use_case_path=request.use_case_path,
    )
    artefacts["semantic_manifest"] = manifest

    validate_artefacts(artefacts)

    output_dir = request.output_root / use_case.use_case_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    publish_package(output_dir, artefacts, semantic_sql, certification_report)
    return output_dir


def certify(package_path: Path) -> dict[str, object]:
    report_path = package_path / "07_delivery_pack" / "certification_report.md"
    manifest_path = package_path / "07_delivery_pack" / "semantic_manifest.yaml"
    return {
        "package_path": str(package_path),
        "certification_report_present": report_path.exists(),
        "semantic_manifest_present": manifest_path.exists(),
    }
