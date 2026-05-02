from __future__ import annotations

from semantic_foundry.config import UseCase


def build_certification_report(use_case: UseCase) -> str:
    return f"""# Semantic_Foundry Certification Report

## Use Case
{use_case.use_case_id}

## Generated Semantic Assets
- certified_business_customer
- certified_business_account
- certified_merchant
- certified_fraud_model_run
- certified_transaction
- certified_transaction_fraud_signal
- certified_fraud_alert

## Certification Summary
| Asset | Status | Reason |
|---|---|---|
| certified_business_customer | Draft | Business owner confirmation required |
| certified_business_account | Candidate | Relationship and DQ rules drafted |
| certified_merchant | Draft | Merchant semantic definition and ownership require review |
| certified_fraud_model_run | Draft | Evaluation-run semantics and aggregated inputs require review |
| certified_transaction | Candidate | Transaction DQ rules generated |
| certified_transaction_fraud_signal | Candidate | Signal thresholds require approval |
| certified_fraud_alert | Candidate | Human review policy required |

## Blocking Issues
1. Synthetic fraud labels are not production-confirmed outcomes.
2. Spike and velocity thresholds require Fraud Risk Owner approval.
3. Account-level burst signal may inflate false positives.
4. Restricted transaction access policy must be implemented.

## Recommended Next Actions
1. Confirm business definitions with Fraud Risk and Operations.
2. Validate thresholds using production historical data.
3. Implement RBAC for transaction-level semantic views.
4. Run DQ checks on real warehouse tables.
5. Pilot AI copilot against certified-only views.
"""
