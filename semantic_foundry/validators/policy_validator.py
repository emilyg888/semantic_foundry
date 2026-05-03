from __future__ import annotations

from dataclasses import dataclass

from semantic_foundry.config import UseCase


HIGH_RISK_LEVELS = {"high", "critical"}


@dataclass(slots=True)
class PolicyValidationFinding:
    check_id: str
    severity: str
    issue: str
    blocking: bool


@dataclass(slots=True)
class PolicyCheck:
    check_id: str
    status: str
    severity: str
    blocking: bool
    detail: str

    def as_dict(self) -> dict[str, object]:
        return {
            "check_id": self.check_id,
            "status": self.status,
            "severity": self.severity,
            "blocking": self.blocking,
            "detail": self.detail,
        }


@dataclass(slots=True)
class PolicyValidationReport:
    use_case_id: str
    checks: list[PolicyCheck]
    findings: list[PolicyValidationFinding]

    @property
    def blocking_findings(self) -> list[PolicyValidationFinding]:
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
            "policy_validation": {
                "status": self.status,
                "checks": [check.as_dict() for check in self.checks],
                "failed_checks": [
                    {
                        "check_id": finding.check_id,
                        "severity": finding.severity,
                        "blocking": finding.blocking,
                        "issue": finding.issue,
                    }
                    for finding in self.findings
                ],
            },
        }

    def raise_if_blocking(self) -> None:
        if not self.blocking_findings:
            return
        failures = ", ".join(finding.check_id for finding in self.blocking_findings)
        raise PolicyValidationError(f"Blocking policy validation failures: {failures}")


class PolicyValidationError(ValueError):
    """Raised when blocking policy validation failures are detected."""


def validate_policies(
    use_case: UseCase,
    policies_artefact: dict[str, object],
    ai_context_cards_artefact: dict[str, object],
) -> PolicyValidationReport:
    policies = list(policies_artefact["policies"])  # type: ignore[index]
    ai_context_cards = list(ai_context_cards_artefact["ai_context_cards"])  # type: ignore[index]

    findings: list[PolicyValidationFinding] = []
    checks = [
        validate_high_risk_human_review(use_case, policies, ai_context_cards, findings),
        validate_restricted_asset_controls(policies, findings),
        validate_ai_context_disallowed_actions(ai_context_cards, findings),
    ]
    return PolicyValidationReport(use_case_id=use_case.use_case_id, checks=checks, findings=findings)


def validate_high_risk_human_review(
    use_case: UseCase,
    policies: list[object],
    ai_context_cards: list[object],
    findings: list[PolicyValidationFinding],
) -> PolicyCheck:
    if use_case.risk_level.lower() not in HIGH_RISK_LEVELS:
        return PolicyCheck(
            check_id="high_risk_human_review_control",
            status="passed",
            severity="info",
            blocking=False,
            detail="Use case is not marked high risk.",
        )

    review_policy_present = any(
        isinstance(policy, dict)
        and bool(policy.get("review_required"))
        and "analyst" in str(policy.get("approved_use", "")).lower()
        and contains_human_review_guardrail(str(policy.get("disallowed_use", "")))
        for policy in policies
    )
    ai_card_present = any(
        isinstance(card, dict)
        and contains_human_review_guardrail(str(card.get("refusal_rule", "")))
        for card in ai_context_cards
    )
    passed = review_policy_present and ai_card_present
    detail = "High-risk use case includes human-review policy and AI refusal guardrail."
    if not passed:
        detail = "High-risk use case is missing required human-review policy or AI refusal guardrail."
        findings.append(
            PolicyValidationFinding(
                check_id="high_risk_human_review_control",
                severity="critical",
                issue=detail,
                blocking=True,
            )
        )
    return PolicyCheck(
        check_id="high_risk_human_review_control",
        status="passed" if passed else "failed",
        severity="critical",
        blocking=True,
        detail=detail,
    )


def validate_restricted_asset_controls(
    policies: list[object],
    findings: list[PolicyValidationFinding],
) -> PolicyCheck:
    restricted_policies = [
        policy
        for policy in policies
        if isinstance(policy, dict) and str(policy.get("classification", "")).lower() == "restricted"
    ]
    passed = bool(restricted_policies) and all(
        str(policy.get("approved_use", "")).strip() and str(policy.get("disallowed_use", "")).strip()
        for policy in restricted_policies
    )
    detail = "Restricted assets carry approved and disallowed use controls."
    if not passed:
        detail = "Restricted assets are missing approved or disallowed use controls."
        findings.append(
            PolicyValidationFinding(
                check_id="restricted_asset_controls",
                severity="critical",
                issue=detail,
                blocking=True,
            )
        )
    return PolicyCheck(
        check_id="restricted_asset_controls",
        status="passed" if passed else "failed",
        severity="critical",
        blocking=True,
        detail=detail,
    )


def validate_ai_context_disallowed_actions(
    ai_context_cards: list[object],
    findings: list[PolicyValidationFinding],
) -> PolicyCheck:
    disallowed_tokens = {"auto", "without analyst approval", "confirmed fraud", "block"}
    passed = bool(ai_context_cards) and all(
        isinstance(card, dict)
        and isinstance(card.get("disallowed_actions"), list)
        and len(card["disallowed_actions"]) >= 2
        and any(
            any(token in str(action).lower() for token in disallowed_tokens)
            for action in card["disallowed_actions"]
        )
        for card in ai_context_cards
    )
    detail = "AI context cards include disallowed actions for unsafe fraud handling."
    if not passed:
        detail = "AI context cards are missing required disallowed-action guardrails."
        findings.append(
            PolicyValidationFinding(
                check_id="ai_context_disallowed_actions",
                severity="critical",
                issue=detail,
                blocking=True,
            )
        )
    return PolicyCheck(
        check_id="ai_context_disallowed_actions",
        status="passed" if passed else "failed",
        severity="critical",
        blocking=True,
        detail=detail,
    )


def contains_human_review_guardrail(text: str) -> bool:
    lowered = text.lower()
    return "human review" in lowered or "analyst approval" in lowered
