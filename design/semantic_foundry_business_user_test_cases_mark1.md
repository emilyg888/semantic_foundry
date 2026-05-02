# Semantic_Foundry MVP Business Test Cases

## Document Purpose

This file provides 5 business-facing test cases for validating the Semantic_Foundry MVP for the `business_banking_fraud_detection` use case.

## Test Environment

- Project: `semantic_foundry`
- Use case file: `examples/business_banking_fraud/use_case.yaml`
- Source fixture: `examples/business_banking_fraud/source/`
- Generated package: `outputs/business_banking_fraud_detection/`

---

## Business Test Case 1: Verify Use Case Scope

**Business objective**  
Confirm the generated discovery output reflects the intended fraud investigation scope.

**Business user**  
Fraud Operations Lead

**Preconditions**

- The `discover` command has been executed.
- The user can review the CLI JSON output.

**Test steps**

1. Run the `discover` command.
2. Review `semantic_layer_candidates`.
3. Review `signal_layer_candidates`.
4. Review `alert_layer_candidates`.

**Expected outcome**

- The output includes the core business entities.
- The output includes core merchant-related semantic fields used in fraud analysis.
- The output includes fraud-relevant signals.
- The output includes a human-review flag for fraud alerts.

**Checklist**

- [ ] `business_customer` is present.
- [ ] `business_account` is present.
- [ ] `merchant` is present as a semantic entity.
- [ ] `transaction` is present.
- [ ] `merchant_id` is present in semantic business fields.
- [ ] `merchant_category` is present in semantic business fields.
- [ ] `merchant_risk_rating` is present in semantic business fields.
- [ ] A merchant-to-transaction relationship is present.
- [ ] `predicted_fraud` appears in the alert layer.
- [ ] `requires_human_review` is set to `true`.

---

## Business Test Case 2: Verify Business Glossary Quality

**Business objective**  
Confirm that the generated glossary terms are understandable to business stakeholders.

**Business user**  
Business Banking Product Owner

**Preconditions**

- The `build` command has been executed.
- `outputs/business_banking_fraud_detection/01_semantic_catalogue/glossary.yaml` exists.

**Test steps**

1. Open `01_semantic_catalogue/glossary.yaml`.
2. Review the terms for customer, account, transaction, fraud signal, and fraud alert.
3. Review owner assignment and sensitivity labels.

**Expected outcome**

- Terms are described in business language.
- Owners are assigned.
- Sensitive banking concepts are appropriately classified.

**Checklist**

- [ ] At least 5 business terms are present.
- [ ] `customer` has a business-readable definition.
- [ ] `account` has a business-readable definition.
- [ ] `transaction` has a business-readable definition.
- [ ] Each reviewed term includes an owner.
- [ ] Each reviewed term includes a sensitivity label.

---

## Business Test Case 3: Verify Fraud Signal Interpretability

**Business objective**  
Confirm that fraud signals can be understood and explained by fraud analysts.

**Business user**  
Fraud Analyst

**Preconditions**

- The `build` command has been executed.
- `outputs/business_banking_fraud_detection/02_signal_catalogue/signals.yaml` exists.

**Test steps**

1. Open `02_signal_catalogue/signals.yaml`.
2. Review the feature and signal definitions.
3. Check whether the signal set supports analyst explanation of suspicious behaviour.

**Expected outcome**

- Core signals are understandable.
- The signal set supports first-pass fraud triage.
- Experimental signals are clearly marked.

**Checklist**

- [ ] `abs_amount` is present.
- [ ] `txn_count` is present.
- [ ] `same_ts_count` is present.
- [ ] `is_spike` is present.
- [ ] `is_velocity` is present.
- [ ] `is_anomaly` is present.
- [ ] `account_had_burst` is clearly marked as experimental or non-final.

---

## Business Test Case 4: Verify Governance and Control Coverage

**Business objective**  
Confirm that minimum governance controls are included before business review.

**Business user**  
Risk Manager

**Preconditions**

- The `build` command has been executed.
- `05_governance_controls/dq_rules.yaml`, `05_governance_controls/policies.yaml`, and `07_delivery_pack/certification_report.md` exist.

**Test steps**

1. Open `05_governance_controls/dq_rules.yaml`.
2. Open `05_governance_controls/policies.yaml`.
3. Open `07_delivery_pack/certification_report.md`.
4. Review blocking issues and usage controls.

**Expected outcome**

- Data quality rules cover key integrity checks.
- Policy controls restrict unsafe usage.
- Blocking issues are explicit for stakeholders.

**Checklist**

- [ ] A transaction primary key quality rule exists.
- [ ] An account-to-customer relationship quality rule exists.
- [ ] A transaction-to-account relationship quality rule exists.
- [ ] Restricted transaction usage is called out in policy rules.
- [ ] Synthetic label caveats are documented.
- [ ] Blocking issues are visible in the certification report.

---

## Business Test Case 5: Verify MVP Delivery Pack Readiness

**Business objective**  
Confirm the generated package is complete enough for business playback and stakeholder review.

**Business user**  
Consulting Engagement Lead

**Preconditions**

- The `build` command has been executed.
- The output folder exists.

**Test steps**

1. Open `outputs/business_banking_fraud_detection/`.
2. Verify the expected artefacts are present.
3. Review whether the output can support a stakeholder workshop.

**Expected outcome**

- The package contains the expected MVP artefacts.
- The artefacts are reviewable by both business and delivery stakeholders.
- The report provides clear next actions.

**Checklist**

- [ ] `01_semantic_catalogue/glossary.yaml` exists.
- [ ] `01_semantic_catalogue/entities.yaml` exists.
- [ ] `01_semantic_catalogue/relationships.yaml` exists.
- [ ] `03_prediction_catalogue/predictions.yaml` exists.
- [ ] `04_evaluation_metric_catalogue/metrics.yaml` exists.
- [ ] `02_signal_catalogue/signals.yaml` exists.
- [ ] `05_governance_controls/dq_rules.yaml` exists.
- [ ] `05_governance_controls/policies.yaml` exists.
- [ ] `07_delivery_pack/semantic_manifest.yaml` exists.
- [ ] `07_delivery_pack/semantic_views.sql` exists.
- [ ] `07_delivery_pack/certification_report.md` exists.

---

## Overall Exit Criteria

- [ ] All 5 business test cases have been executed.
- [ ] No unresolved critical business-definition issue remains.
- [ ] No governance blocker is incorrectly treated as approved.
- [ ] Stakeholders agree the MVP package is suitable for review.
