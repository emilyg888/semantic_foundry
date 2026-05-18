# Issues Pending Review

## Summary

| ID | Severity | Area | Issue | Recommended action | Status |
|---|---|---|---|---|---|
| ISSUE-001 | High | Governance | Default fraud package is still `not_certifiable` because synthetic fraud-label caveats remain blocking. | Resolve or explicitly approve synthetic-label limitation before claiming candidate or certified operational use. | Pending review |
| ISSUE-002 | Medium | Docs | Legacy architecture material exists in `design/semantic_foundry_architecture.md`, while housekeeping introduced `design/architecture.md` as the current operational reference. | Decide whether to consolidate or retain both docs with clearer ownership. | Pending review |
| ISSUE-003 | Medium | UI | Review cockpit actions were fixed in code, but full manual click-through validation was not performed in this housekeeping pass. | Manually verify approve/reject/update-owner/publish actions in the Streamlit UI. | Pending review |
| ISSUE-004 | Low | Housekeeping | No archive candidate met the skill threshold for safe archival. | Revisit only if duplicate or obsolete modules become clearer in future iterations. | Pending review |

## SIT Results

| Command | Result | Notes |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests` | Passed | 45 tests passed |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python main.py build --source examples/business_banking_fraud/source --use-case examples/business_banking_fraud/use_case.yaml --target generic_sql` | Passed | Built `outputs/business_banking_fraud_detection` |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python main.py certify --package outputs/business_banking_fraud_detection` | Passed | Certification command completed; result remained `not_certifiable` with `validation_status: passed` |

## Archived Code Review

| Original path | Archived path | Reason | Review needed? |
|---|---|---|---|
| None | None | No low-risk redundant code candidate met the archive threshold with sufficient evidence. | No |

## Detailed Issues

### ISSUE-001 — Default package remains not certifiable

- Severity: High
- Area: Governance
- Evidence:
  - `python main.py certify --package outputs/business_banking_fraud_detection`
  - blocking issue: `Synthetic fraud labels are suitable for accelerator validation only.`
- Impact:
  - The package should not be represented as operationally certifiable without further review or explicit acceptance of the synthetic-label boundary.
- Recommended action:
  - Resolve the label-governance issue or add an approved review decision that reclassifies the package for the intended use.
- Status: Pending review

### ISSUE-002 — Architecture document ownership is split

- Severity: Medium
- Area: Architecture
- Evidence:
  - Existing file: `design/semantic_foundry_architecture.md`
  - New housekeeping reference: `design/architecture.md`
- Impact:
  - Reviewers may be unsure which document is authoritative for current system shape.
- Recommended action:
  - Consolidate documents or clearly label one as strategic/reference and the other as current implementation architecture.
- Status: Pending review

### ISSUE-003 — Review cockpit still needs manual UI verification

- Severity: Medium
- Area: Tests
- Evidence:
  - Service-layer tests passed, but Streamlit UI interaction was not executed end-to-end in this housekeeping pass.
- Impact:
  - UI regressions could still exist despite service logic passing.
- Recommended action:
  - Perform a manual review-cockpit smoke test for asset approval, issue capture, and publish.
- Status: Pending review

### ISSUE-004 — No safe archive move performed

- Severity: Low
- Area: Code
- Evidence:
  - No file met the required dual-signal redundancy threshold while remaining low risk to move.
- Impact:
  - Some generated or exploratory artefacts may still warrant later cleanup, but no safe housekeeping move was justified now.
- Recommended action:
  - Reassess after future refactors or once duplicate/stale modules are explicitly confirmed.
- Status: Pending review
