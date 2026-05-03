from __future__ import annotations

from semantic_foundry.validators.certification_validator import CertificationGateReport


def build_certification_report(use_case_id: str, gate: CertificationGateReport) -> str:
    requirement_rows = "\n".join(
        f"| {requirement.name} | {'Passed' if requirement.passed else 'Pending'} | {requirement.detail} |"
        for requirement in gate.requirements
    )
    blocker_lines = "\n".join(
        f"{index}. {blocker}" for index, blocker in enumerate(gate.blockers, start=1)
    ) or "1. No blocking issues detected."
    next_action_lines = "\n".join(
        f"{index}. {action}" for index, action in enumerate(recommended_next_actions(gate), start=1)
    )
    asset_stage_rows = "\n".join(
        f"| {stage} | {count} |" for stage, count in sorted(gate.asset_stage_counts.items())
    )
    return f"""# Semantic_Foundry Certification Report

## Use Case
{use_case_id}

## Certification Result
- Result: `{gate.result}`
- Validation status: `{gate.validation_status}`

## Requirement Summary
| Requirement | Status | Detail |
|---|---|---|
{requirement_rows}

## Asset Stage Counts
| Stage | Count |
|---|---|
{asset_stage_rows}

## Blocking Issues
{blocker_lines}

## Recommended Next Actions
{next_action_lines}
"""


def recommended_next_actions(gate: CertificationGateReport) -> list[str]:
    actions: list[str] = []
    for requirement in gate.requirements:
        if requirement.passed:
            continue
        if requirement.name == "business_definition_approved":
            actions.append("Promote glossary and entity definitions from draft to candidate through business review.")
        elif requirement.name == "threshold_approved":
            actions.append("Approve draft and experimental metrics, signals, and predictions with Fraud Analytics and Risk.")
        elif requirement.name == "owner_assigned":
            actions.append("Assign owners to every semantic asset before certification review.")
        elif requirement.name == "dq_rules_passed":
            actions.append("Resolve blocking DQ issues and rerun deterministic validation.")
        elif requirement.name == "policy_rules_defined":
            actions.append("Close policy gaps and rerun policy validation.")
        elif requirement.name == "ai_context_card_created":
            actions.append("Create AI context cards with allowed and disallowed usage guidance.")
    if gate.blockers:
        actions.append("Resolve blocking issues in the issue register before requesting certification.")
    if not actions:
        actions.append("Package is ready to advance to the next review stage.")
    return actions
