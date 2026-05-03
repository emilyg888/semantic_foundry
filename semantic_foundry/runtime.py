from __future__ import annotations

import shutil
from pathlib import Path

from semantic_foundry.builders.manifest_builder import build_semantic_manifest
from semantic_foundry.builders.package_index_builder import build_package_index
from semantic_foundry.builders.report_builder import build_certification_report
from semantic_foundry.builders.semantic_package_builder import (
    build_evaluation_questions,
    build_lineage,
    build_metric_catalogue,
    build_package_manifest,
    build_semantic_catalogue,
    build_signal_catalogue,
)
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
from semantic_foundry.simple_yaml import load_simple_yaml
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
from semantic_foundry.validators.certification_validator import (
    build_issue_register,
    certify_package,
    evaluate_certification_gate,
)
from semantic_foundry.validators.dq_validator import validate_dq_rules
from semantic_foundry.validators.policy_validator import validate_policies
from semantic_foundry.validators.source_schema_validator import validate_source_schema
from semantic_foundry.validators.sql_validator import validate_semantic_sql


def discover(source_path: Path, use_case_path: Path) -> dict[str, object]:
    use_case = load_use_case(use_case_path)
    inventory = build_source_inventory(source_path)
    logic = mine_python_logic(source_path)
    return build_discovery_report(use_case, inventory, logic)


def build_discovery_report(use_case: object, inventory: object, logic: object) -> dict[str, object]:
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
    source_schema_report = validate_source_schema(use_case, inventory)
    logic = mine_python_logic(request.source_path)
    discovery_report = build_discovery_report(use_case, inventory, logic)
    dq_rules = build_dq_rules(use_case)
    dq_validation_report = validate_dq_rules(use_case, request.source_path, dq_rules)
    ai_context_cards = build_ai_context_cards(use_case)
    policies = build_policies(use_case)
    policy_validation_report = validate_policies(use_case, policies, ai_context_cards)

    artefacts: dict[str, object] = {
        "glossary": build_glossary(use_case, logic),
        "entities": build_entities(use_case),
        "relationships": build_relationships(use_case),
        "signals": build_signals(use_case, logic),
        "predictions": build_predictions(use_case, logic),
        "metrics": build_metrics(use_case),
        "dq_rules": dq_rules,
        "policies": policies,
        "ai_context_cards": ai_context_cards,
        "dq_validation": dq_validation_report.as_artefact(),
        "policy_validation": policy_validation_report.as_artefact(),
        "issue_register": build_issue_register(
            source_schema_findings=source_schema_report.findings,
            dq_findings=dq_validation_report.findings,
            policy_findings=policy_validation_report.findings,
        ),
    }

    semantic_sql = build_semantic_sql(use_case)
    artefacts["sql_validation"] = validate_semantic_sql(semantic_sql)
    gate = evaluate_certification_gate(artefacts)
    certification_report = build_certification_report(use_case.use_case_id, gate)
    package_index = build_package_index(use_case)
    artefacts["package_manifest"] = build_package_manifest(use_case, gate)
    artefacts["use_case_package"] = load_simple_yaml(request.use_case_path)
    artefacts["discovery_report"] = discovery_report
    artefacts["semantic_catalogue"] = build_semantic_catalogue(artefacts)
    artefacts["signal_catalogue"] = build_signal_catalogue(artefacts)
    artefacts["metric_catalogue"] = build_metric_catalogue(artefacts)
    artefacts["dq_rules_package"] = artefacts["dq_rules"]
    artefacts["policy_rules_package"] = {"policy_rules": artefacts["policies"]["policies"]}  # type: ignore[index]
    artefacts["lineage"] = build_lineage(artefacts)
    artefacts["ai_context_cards_package"] = artefacts["ai_context_cards"]
    artefacts["evaluation_questions"] = build_evaluation_questions(use_case, artefacts)

    manifest = build_semantic_manifest(
        use_case=use_case,
        inventory=inventory,
        generated_assets=expected_generated_assets(),
        source_path=request.source_path,
        use_case_path=request.use_case_path,
        validation_status=gate.validation_status,
        certification_status=gate.result,
    )
    artefacts["semantic_manifest"] = manifest

    validate_artefacts(artefacts)
    dq_validation_report.raise_if_blocking()
    policy_validation_report.raise_if_blocking()

    output_dir = request.output_root / use_case.use_case_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    publish_package(output_dir, artefacts, semantic_sql, certification_report, package_index)
    return output_dir


def certify(package_path: Path) -> dict[str, object]:
    return certify_package(package_path)
