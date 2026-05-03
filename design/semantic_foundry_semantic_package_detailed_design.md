# Semantic_Foundry Semantic Package — Detailed Design

## 1. Purpose

A **semantic package** is the versioned, reviewable, and deployable bundle produced by **Semantic_Foundry** for a specific business use case.

It converts existing enterprise data, analytical code, feature logic, business assumptions, and governance requirements into a governed semantic-layer package that can be reviewed, certified, and implemented on a target data platform.

For the Business Banking Fraud Detection example, the semantic package defines:

- Business entities such as customer, account, transaction, fraud alert, and model run
- Behavioural fraud signals such as amount spike, velocity burst, anomaly, and fraud score
- Evaluation metrics such as fraud precision, fraud recall, and F1 score
- Data quality controls
- Policy and human-review rules
- Semantic SQL views
- AI consumption contracts
- Certification status and blocking issues

The package is not just a set of SQL views. It is a complete business meaning, governance, and AI-readiness contract.

---

## 2. Design principles

### 2.1 Business use case first

Semantic_Foundry should start with the business use case, not with all available data sources.

For example:

> Build a governed semantic package that allows fraud analysts and AI copilots to detect, explain, and evaluate suspicious business banking transactions.

This keeps the scope concrete and prevents the accelerator from becoming a generic metadata scanner.

### 2.2 Separate semantic layer, signal layer, and evaluation layer

The design should not mix everything into one catalogue.

```text
Semantic Layer
    Defines stable business meaning:
    Customer, Account, Transaction, Fraud Alert, Fraud Label, Model Run

Signal Layer
    Defines behavioural evidence:
    Amount Spike, Velocity Burst, Statistical Anomaly, Fraud Score

Evaluation Layer
    Defines detector performance:
    Precision, Recall, F1 Score, False Positive Rate, False Negative Rate
```

### 2.3 AI proposes, rules validate, humans certify

```text
LLM / AI Agent
    proposes glossary terms, definitions, signals, policies, and AI cards

Deterministic Validators
    check schema, naming, formulas, DQ rules, SQL validity, and certification gates

Human Review
    approves business meaning, ownership, policy boundaries, and production readiness
```

### 2.4 Package before platform-specific implementation

The first package should be target-neutral.

Supported targets may include:

- Generic SQL
- Snowflake
- Databricks
- dbt
- Power BI semantic models
- Looker / LookML
- Custom YAML-driven semantic services

The initial MVP should prioritise generic SQL and YAML artefacts before expanding to dbt or other ETL scanners.

---

## 3. Semantic package concept

A semantic package is a folder containing all artefacts required to understand, review, certify, and deploy a semantic layer for one use case.

```text
semantic_package/
├── package_manifest.yaml
├── use_case.yaml
├── discovery_report.json
├── semantic_catalogue.yaml
├── signal_catalogue.yaml
├── metric_catalogue.yaml
├── dq_rules.yaml
├── policy_rules.yaml
├── lineage.yaml
├── semantic_views.sql
├── ai_context_cards.yaml
├── evaluation_questions.yaml
└── certification_report.md
```

The package acts like a software release bundle, but for business meaning.

```text
Software package contains:
- code
- config
- tests
- documentation
- version
- release notes

Semantic package contains:
- business definitions
- entities
- metrics
- signals
- SQL/views
- DQ rules
- policies
- lineage
- AI context
- certification status
```

---

## 4. Package lifecycle

```text
Discovery
   ↓
Classification
   ↓
Catalogue Generation
   ↓
Validation
   ↓
Human Review
   ↓
Certification
   ↓
Deployment
   ↓
Monitoring / Evolution
```

### 4.1 Discovery

Inputs are scanned or supplied:

- Existing Python, SQL, notebooks, or feature pipelines
- Warehouse or lakehouse tables
- Use case description
- Existing metrics
- Business rules
- Policy constraints
- Known data quality issues

For the current MVP, discovery is focused on Python AST mining.

### 4.2 Classification

Discovered artefacts are classified into layers:

```text
Discovered artefacts
      ↓
Classify into:
├── semantic_entities
├── semantic_fields
├── signal_features
├── fraud_signals
├── prediction_outputs
├── evaluation_metrics
└── governance_controls
```

### 4.3 Catalogue generation

The classified artefacts are converted into YAML catalogues:

- Semantic catalogue
- Signal catalogue
- Metric catalogue
- DQ rules
- Policy rules
- AI context cards

### 4.4 Validation

Validation checks include:

- YAML schema validation
- Required field validation
- Formula validation
- SQL syntax validation
- Naming standard validation
- Ownership completeness
- DQ control completeness
- Certification gate checks

### 4.5 Human review

Business, data, risk, and technical owners review the generated artefacts.

Possible statuses:

```text
draft
candidate
business_review_required
dq_validation_required
policy_review_required
certified
experimental
rejected
retired
```

### 4.6 Deployment

Certified or candidate artefacts can be deployed into the target platform.

For the MVP, deployment may simply mean generating SQL and YAML files for review.

### 4.7 Monitoring and evolution

Over time, semantic packages should be versioned and compared.

Important changes include:

- Definition changes
- Metric formula changes
- Signal threshold changes
- DQ rule changes
- Policy rule changes
- Certification status changes
- Deprecated assets

---

## 5. Top-level package manifest

The manifest describes the semantic package as a whole.

```yaml
package_id: business_banking_fraud_detection
package_name: Business Banking Fraud Detection Semantic Package
version: 0.1.0
status: draft
created_by: Semantic_Foundry
target_platform: generic_sql

business_domain: Business Banking
use_case_type: fraud_detection
risk_level: high
requires_human_review: true

owners:
  business_owner: Head of Business Banking
  data_owner: Head of Business Banking
  fraud_risk_owner: Fraud Risk Owner
  analytics_owner: Fraud Analytics Lead
  operations_owner: Fraud Operations Lead

artefacts:
  use_case: use_case.yaml
  discovery_report: discovery_report.json
  semantic_catalogue: semantic_catalogue.yaml
  signal_catalogue: signal_catalogue.yaml
  metric_catalogue: metric_catalogue.yaml
  dq_rules: dq_rules.yaml
  policy_rules: policy_rules.yaml
  lineage: lineage.yaml
  semantic_views: semantic_views.sql
  ai_context_cards: ai_context_cards.yaml
  certification_report: certification_report.md
```

---

## 6. Use case specification

The use case file anchors the package in business purpose.

```yaml
use_case_id: business_banking_fraud_detection
name: Business Banking Fraud Detection
business_objective: >
  Detect, explain, and evaluate suspicious business banking transactions
  using governed transaction, account, customer, signal, and detector
  evaluation assets.

primary_users:
  - fraud analyst
  - fraud operations lead
  - fraud risk owner
  - fraud analytics lead
  - data scientist

business_questions:
  - Which transactions were flagged as suspicious?
  - Why was a transaction flagged?
  - Which signals contributed to the alert?
  - How well did the detector perform in this run?
  - What is the trade-off between fraud precision and fraud recall?
  - Which accounts show burst behaviour?

decision_type: analyst_assisted
automation_level: human_in_the_loop
risk_level: high
target_platform: generic_sql

requires_human_review: true

approved_use:
  - fraud triage
  - fraud signal explanation
  - detector evaluation
  - analyst investigation support

disallowed_use:
  - fully automated adverse customer action
  - closing accounts without human review
  - declaring a customer guilty of fraud
```

---

## 7. Discovery report

The discovery report records what Semantic_Foundry found from code, schema, and configuration.

Current MVP output example:

```json
{
  "use_case_id": "business_banking_fraud_detection",
  "inventory_counts": {
    "python": 2
  },
  "python_functions": [
    {
      "module_path": "fraud/detector.py",
      "function_name": "predict_fraud",
      "assigned_names": [
        "fraud_score",
        "is_anomaly",
        "is_burst",
        "is_spike",
        "is_velocity",
        "predicted_fraud"
      ],
      "return_names": [
        "fraud_score",
        "is_anomaly",
        "is_spike",
        "is_velocity",
        "predicted_fraud"
      ]
    },
    {
      "module_path": "fraud/features.py",
      "function_name": "build_features",
      "assigned_names": [
        "abs_amount",
        "account_had_burst",
        "account_zscore",
        "avg_amount",
        "is_burst",
        "std_amount",
        "txn_count",
        "z_score"
      ],
      "return_names": [
        "abs_amount",
        "account_had_burst",
        "account_zscore",
        "is_burst",
        "same_ts_count",
        "txn_count",
        "z_score"
      ]
    }
  ],
  "scope": {
    "entities": [
      "customer",
      "account",
      "transaction"
    ],
    "signals": [
      "abs_amount",
      "txn_count",
      "same_ts_count",
      "z_score",
      "account_zscore",
      "is_burst",
      "account_had_burst",
      "is_spike",
      "is_velocity",
      "is_anomaly",
      "predicted_fraud",
      "fraud_score"
    ],
    "owners": {
      "customer": "Head of Business Banking",
      "account": "Head of Business Banking",
      "transaction": "Fraud Operations Lead",
      "fraud_signal": "Fraud Risk Owner",
      "fraud_alert": "Fraud Operations Lead",
      "fraud_score": "Fraud Analytics Lead"
    },
    "target": "generic_sql",
    "requires_human_review": true
  }
}
```

This is not yet the semantic package. It is a discovery input used to create the package.

---

## 8. Artefact classification model

The classifier converts raw discovered names into semantic layers.

### 8.1 Classification categories

| Category | Description | Examples |
|---|---|---|
| semantic_entity | Stable business object | customer, account, transaction |
| semantic_field | Business field or attribute | amount, timestamp, merchant_category |
| signal_feature | Derived feature used by a signal | abs_amount, same_ts_count, z_score |
| fraud_signal | Behavioural fraud evidence | is_spike, is_velocity, is_anomaly |
| prediction_output | Detector output | predicted_fraud |
| score | Composite score | fraud_score |
| evaluation_metric | Model/run performance metric | fraud_precision, fraud_recall, fraud_f1_score |
| policy_rule | Governance or use constraint | human_review_required |
| dq_rule | Data quality control | txn_id_not_null |

### 8.2 Example classification output

```yaml
classified_assets:
  semantic_entities:
    - name: business_customer
      source_name: customer
      confidence: 0.90
      reason: Known fraud use case entity

    - name: business_account
      source_name: account
      confidence: 0.90
      reason: Known fraud use case entity

    - name: transaction
      source_name: transaction
      confidence: 0.95
      reason: Core event entity for transaction fraud

  signal_features:
    - name: abs_amount
      source_name: abs_amount
      confidence: 0.90
      reason: Derived transaction amount feature

    - name: same_ts_count
      source_name: same_ts_count
      confidence: 0.85
      reason: Count-based transaction velocity feature

    - name: z_score
      source_name: z_score
      confidence: 0.90
      reason: Statistical anomaly feature

  fraud_signals:
    - name: amount_spike_signal
      source_name: is_spike
      confidence: 0.95
      reason: Boolean flag beginning with is_ and returned by predict_fraud

    - name: velocity_burst_signal
      source_name: is_velocity
      confidence: 0.95
      reason: Boolean velocity flag returned by predict_fraud

    - name: statistical_anomaly_signal
      source_name: is_anomaly
      confidence: 0.95
      reason: Boolean anomaly flag returned by predict_fraud

  prediction_outputs:
    - name: predicted_fraud
      source_name: predicted_fraud
      confidence: 0.95
      reason: Prediction output returned by detector

  scores:
    - name: fraud_score
      source_name: fraud_score
      confidence: 0.90
      reason: Composite fraud score returned by detector
```

### 8.3 Heuristic rules for MVP

The first version can use deterministic heuristics.

```text
starts with "is_"            → signal flag
contains "score"             → score
contains "predicted"         → prediction output
contains "z_score"           → statistical feature
contains "count"             → count feature
matches known entity names   → semantic entity
matches known metric names   → evaluation metric
```

Later, an LLM can enrich definitions and resolve ambiguous classification.

---

## 9. Semantic catalogue

The semantic catalogue defines stable business meaning.

### 9.1 Entity schema

```yaml
entities:
  - entity_id: string
    name: string
    description: string
    domain: string
    grain: string
    primary_key: string
    owner: string
    sensitivity: string
    certification_status: string
    source_references:
      - string
```

### 9.2 Fraud use case semantic catalogue

```yaml
entities:
  - entity_id: business_customer
    name: Business Customer
    description: A commercial banking customer with a business banking relationship.
    domain: Business Banking
    grain: one row per business customer
    primary_key: customer_id
    owner: Head of Business Banking
    sensitivity: confidential
    certification_status: draft
    source_references:
      - use_case.yaml
      - discovery_report.json

  - entity_id: business_account
    name: Business Account
    description: A financial account owned by a business customer.
    domain: Business Banking
    grain: one row per business account
    primary_key: account_id
    owner: Head of Business Banking
    sensitivity: restricted
    certification_status: draft
    source_references:
      - use_case.yaml
      - discovery_report.json

  - entity_id: transaction
    name: Transaction
    description: A debit or credit movement posted against a business banking account.
    domain: Payments
    grain: one row per transaction event
    primary_key: txn_id
    owner: Fraud Operations Lead
    sensitivity: restricted
    certification_status: draft
    source_references:
      - fraud/features.py
      - fraud/detector.py

  - entity_id: fraud_alert
    name: Fraud Alert
    description: A transaction or account event flagged for fraud analyst review.
    domain: Fraud Operations
    grain: one row per flagged transaction event
    primary_key: alert_id
    owner: Fraud Operations Lead
    sensitivity: restricted
    certification_status: candidate
    source_references:
      - fraud/detector.py::predict_fraud

  - entity_id: fraud_model_run
    name: Fraud Detection Model Run
    description: A detector evaluation run used to calculate fraud performance metrics.
    domain: Fraud Analytics
    grain: one row per detector evaluation run
    primary_key: model_run_id
    owner: Fraud Analytics Lead
    sensitivity: internal
    certification_status: draft
    source_references:
      - design/semantic_foundry_detailed_design.md
```

### 9.3 Relationship schema

```yaml
relationships:
  - relationship_id: string
    from_entity: string
    to_entity: string
    relationship_name: string
    cardinality: string
    join_key: string
    certification_status: string
```

### 9.4 Fraud relationships

```yaml
relationships:
  - relationship_id: customer_owns_account
    from_entity: business_customer
    to_entity: business_account
    relationship_name: owns
    cardinality: one_to_many
    join_key: customer_id
    certification_status: draft

  - relationship_id: account_has_transaction
    from_entity: business_account
    to_entity: transaction
    relationship_name: has
    cardinality: one_to_many
    join_key: account_id
    certification_status: draft

  - relationship_id: transaction_generates_alert
    from_entity: transaction
    to_entity: fraud_alert
    relationship_name: may_generate
    cardinality: one_to_zero_or_many
    join_key: txn_id
    certification_status: candidate
```

---

## 10. Signal catalogue

The signal catalogue defines behavioural evidence.

### 10.1 Signal schema

```yaml
signals:
  - signal_id: string
    name: string
    source_field: string
    entity: string
    signal_type: string
    definition: string
    business_interpretation: string
    logic: string
    threshold: string
    owner: string
    explainability: string
    approved_use:
      - string
    disallowed_use:
      - string
    known_limitations:
      - string
    status: string
    source_references:
      - string
```

### 10.2 Fraud signal catalogue

```yaml
signals:
  - signal_id: amount_spike_signal
    name: Amount Spike Signal
    source_field: is_spike
    entity: transaction
    signal_type: rule_based
    definition: Indicates that a transaction amount exceeds a suspicious amount threshold.
    business_interpretation: The transaction amount may be unusually large and warrants review.
    logic: abs_amount > spike_threshold
    threshold: configured by detector
    owner: Fraud Risk Owner
    explainability: high
    approved_use:
      - fraud triage
      - analyst explanation
      - signal monitoring
    disallowed_use:
      - sole basis for adverse customer action
    known_limitations:
      - threshold requires fraud risk owner approval
      - may create false positives for legitimate high-value business payments
    status: candidate
    source_references:
      - fraud/detector.py::predict_fraud

  - signal_id: velocity_burst_signal
    name: Velocity Burst Signal
    source_field: is_velocity
    entity: transaction
    signal_type: rule_based
    definition: Indicates rapid repeated transaction activity for the same account.
    business_interpretation: Multiple transactions occurring close together may indicate automated or coordinated suspicious behaviour.
    logic: same_ts_count >= velocity_threshold
    threshold: configured by detector
    owner: Fraud Risk Owner
    explainability: high
    approved_use:
      - fraud triage
      - burst behaviour detection
      - analyst explanation
    disallowed_use:
      - sole basis for adverse customer action
    known_limitations:
      - exact time window must be confirmed
      - same timestamp may be too narrow compared with practical fraud behaviour
    status: candidate
    source_references:
      - fraud/features.py::build_features
      - fraud/detector.py::predict_fraud

  - signal_id: statistical_anomaly_signal
    name: Statistical Anomaly Signal
    source_field: is_anomaly
    entity: transaction
    signal_type: statistical
    definition: Indicates that a transaction amount is statistically unusual compared with observed transaction behaviour.
    business_interpretation: The transaction may be abnormal compared with historical or population-level transaction distribution.
    logic: abs(z_score) > anomaly_threshold
    threshold: configured by detector
    owner: Fraud Risk Owner
    explainability: medium
    approved_use:
      - anomaly screening
      - fraud triage
      - detector evaluation
    disallowed_use:
      - final fraud determination without analyst review
    known_limitations:
      - sensitive to data distribution drift
      - may be unstable with small samples
      - depends on correct treatment of transaction amount
    status: candidate
    source_references:
      - fraud/features.py::build_features
      - fraud/detector.py::predict_fraud

  - signal_id: account_burst_history_signal
    name: Account Burst History Signal
    source_field: account_had_burst
    entity: business_account
    signal_type: historical_behaviour
    definition: Indicates that the account has previously shown burst transaction behaviour.
    business_interpretation: Prior burst activity may indicate elevated account-level monitoring interest.
    logic: account_had_burst = true
    threshold: not applicable
    owner: Fraud Risk Owner
    explainability: medium
    approved_use:
      - account monitoring
      - analyst context
    disallowed_use:
      - direct customer action without transaction-level evidence
    known_limitations:
      - may contaminate current transaction risk with historical account behaviour
      - may increase recall while reducing precision
    status: experimental
    source_references:
      - fraud/features.py::build_features
```

---

## 11. Prediction and alert layer

### 11.1 Prediction output schema

```yaml
prediction_outputs:
  - prediction_id: string
    name: string
    source_field: string
    entity: string
    definition: string
    logic: string
    owner: string
    requires_human_review: boolean
    approved_use:
      - string
    disallowed_use:
      - string
    status: string
```

### 11.2 Fraud prediction output

```yaml
prediction_outputs:
  - prediction_id: predicted_fraud
    name: Predicted Fraud Indicator
    source_field: predicted_fraud
    entity: transaction
    definition: Indicates that the detector flagged the transaction as suspicious based on one or more fraud signals.
    logic: is_spike OR is_velocity OR is_anomaly
    owner: Fraud Operations Lead
    requires_human_review: true
    approved_use:
      - fraud analyst review queue
      - alert explanation
      - detector evaluation
    disallowed_use:
      - final fraud determination
      - account closure without human investigation
      - adverse customer action without review
    status: candidate
    source_references:
      - fraud/detector.py::predict_fraud
```

### 11.3 Fraud score

```yaml
scores:
  - score_id: fraud_score
    name: Fraud Score
    source_field: fraud_score
    entity: transaction
    definition: Composite score representing the strength or count of fraud signal evidence for a transaction.
    owner: Fraud Analytics Lead
    score_type: composite_rule_score
    requires_human_review: true
    status: draft
    source_references:
      - fraud/detector.py::predict_fraud
```

---

## 12. Metric catalogue

The metric catalogue separates performance metrics from fraud signals.

### 12.1 Metric schema

```yaml
metrics:
  - metric_id: string
    name: string
    metric_type: string
    definition: string
    grain: string
    formula: string
    owner: string
    status: string
    required_inputs:
      - string
    interpretation:
      high_value_means: string
      low_value_means: string
    caveats:
      - string
    source_references:
      - string
```

### 12.2 Fraud precision

```yaml
metrics:
  - metric_id: fraud_precision
    name: Fraud Precision
    metric_type: evaluation_metric
    evaluation_subject: fraud_detector
    definition: Proportion of flagged transactions that match the available fraud label.
    grain: model_run
    formula: true_positive / nullif(true_positive + false_positive, 0)
    owner: Fraud Analytics Lead
    status: draft
    required_inputs:
      - true_positive
      - false_positive
      - predicted_fraud
      - fraud_label
    interpretation:
      high_value_means: Fewer false positive alerts and cleaner analyst queues.
      low_value_means: Many flagged transactions do not match the available fraud label.
    caveats:
      - If fraud_label is synthetic or weakly labelled, this metric evaluates against the available label, not confirmed real-world fraud.
    source_references:
      - fraud/detector.py::predict_fraud
      - design/semantic_foundry_detailed_design.md
```

### 12.3 Fraud recall

```yaml
metrics:
  - metric_id: fraud_recall
    name: Fraud Recall
    metric_type: evaluation_metric
    evaluation_subject: fraud_detector
    definition: Proportion of labelled fraud transactions that were flagged by the detector.
    grain: model_run
    formula: true_positive / nullif(true_positive + false_negative, 0)
    owner: Fraud Analytics Lead
    status: draft
    required_inputs:
      - true_positive
      - false_negative
      - predicted_fraud
      - fraud_label
    interpretation:
      high_value_means: More labelled fraud transactions are detected.
      low_value_means: More labelled fraud transactions are missed.
    caveats:
      - If fraud_label is synthetic or weakly labelled, recall does not prove real-world fraud coverage.
    source_references:
      - fraud/detector.py::predict_fraud
      - design/semantic_foundry_detailed_design.md
```

### 12.4 Fraud F1 score

```yaml
metrics:
  - metric_id: fraud_f1_score
    name: Fraud F1 Score
    metric_type: evaluation_metric
    evaluation_subject: fraud_detector
    definition: Harmonic mean of fraud precision and fraud recall for a detector evaluation run.
    grain: model_run
    formula: 2 * fraud_precision * fraud_recall / nullif(fraud_precision + fraud_recall, 0)
    owner: Fraud Analytics Lead
    status: draft
    required_inputs:
      - fraud_precision
      - fraud_recall
      - true_positive
      - false_positive
      - false_negative
    interpretation:
      high_value_means: The detector has a better balance between alert quality and fraud coverage.
      low_value_means: The detector is weak on precision, recall, or both.
    caveats:
      - F1 assumes precision and recall are equally important.
      - Business cost weighting may require a different metric.
      - Fraud detection often needs additional metrics such as alert volume, false positive rate, analyst capacity, customer friction, and fraud loss exposure.
    source_references:
      - fraud/detector.py::predict_fraud
      - design/semantic_foundry_detailed_design.md
```

---

## 13. Data quality rules

DQ rules are deterministic controls used to assess whether semantic assets can be trusted.

### 13.1 DQ rule schema

```yaml
dq_rules:
  - rule_id: string
    name: string
    entity: string
    column: string
    rule_type: string
    expression: string
    severity: string
    failure_action: string
    certification_impact: string
```

### 13.2 Fraud DQ rules

```yaml
dq_rules:
  - rule_id: customer_id_not_null
    name: Customer ID must not be null
    entity: business_customer
    column: customer_id
    rule_type: completeness
    expression: customer_id IS NOT NULL
    severity: critical
    failure_action: block_certification
    certification_impact: business_customer cannot be certified

  - rule_id: customer_id_unique
    name: Customer ID must be unique
    entity: business_customer
    column: customer_id
    rule_type: uniqueness
    expression: customer_id IS UNIQUE
    severity: critical
    failure_action: block_certification
    certification_impact: business_customer grain is invalid

  - rule_id: account_customer_valid
    name: Account customer link must be valid
    entity: business_account
    column: customer_id
    rule_type: referential_integrity
    expression: accounts.customer_id exists in customers.customer_id
    severity: critical
    failure_action: block_certification
    certification_impact: business_account relationship to customer cannot be certified

  - rule_id: transaction_account_valid
    name: Transaction account link must be valid
    entity: transaction
    column: account_id
    rule_type: referential_integrity
    expression: transactions.account_id exists in accounts.account_id
    severity: critical
    failure_action: block_certification
    certification_impact: transaction relationship to account cannot be certified

  - rule_id: transaction_amount_not_null
    name: Transaction amount must not be null
    entity: transaction
    column: amount
    rule_type: completeness
    expression: amount IS NOT NULL
    severity: high
    failure_action: warning_or_block
    certification_impact: amount-based fraud signals cannot be certified

  - rule_id: transaction_timestamp_not_null
    name: Transaction timestamp must not be null
    entity: transaction
    column: timestamp
    rule_type: completeness
    expression: timestamp IS NOT NULL
    severity: high
    failure_action: warning_or_block
    certification_impact: velocity-based fraud signals cannot be certified

  - rule_id: fraud_label_boolean
    name: Fraud label must be boolean
    entity: transaction
    column: fraud_label
    rule_type: validity
    expression: fraud_label IN (true, false)
    severity: high
    failure_action: warning_or_block
    certification_impact: evaluation metrics cannot be certified
```

---

## 14. Policy rules

Policy rules define safe use boundaries.

### 14.1 Policy rule schema

```yaml
policy_rules:
  - rule_id: string
    name: string
    applies_to:
      - string
    rule: string
    enforcement: string
    severity: string
    certification_impact: string
```

### 14.2 Fraud policy rules

```yaml
policy_rules:
  - rule_id: fraud_human_review_required
    name: Human review required for fraud outputs
    applies_to:
      - predicted_fraud
      - fraud_score
      - fraud_alert
    rule: Fraud predictions and scores must support analyst review and must not be used as the sole basis for adverse customer action.
    enforcement: ai_response_guardrail
    severity: critical
    certification_impact: fraud alerts cannot be certified for operational use without human review policy

  - rule_id: restricted_transaction_access
    name: Restricted access for transaction-level data
    applies_to:
      - transaction
      - fraud_signal
      - fraud_alert
    rule: Transaction-level records require restricted access.
    enforcement: rbac
    severity: critical
    certification_impact: semantic views cannot be certified without access controls

  - rule_id: explainability_required
    name: Fraud alerts require explainability
    applies_to:
      - fraud_alert
      - predicted_fraud
    rule: Every fraud alert must include contributing signal reasons.
    enforcement: semantic_contract
    severity: high
    certification_impact: fraud alert layer cannot be certified without signal reason mapping

  - rule_id: evaluation_required
    name: Detector performance evaluation required
    applies_to:
      - predicted_fraud
      - fraud_score
    rule: Precision, recall, F1 score, false positives, and false negatives should be monitored by detector run.
    enforcement: evaluation_gate
    severity: high
    certification_impact: detector outputs remain candidate until evaluation metrics exist
```

---

## 15. Lineage

The lineage file traces semantic assets back to source code and physical data.

### 15.1 Lineage schema

```yaml
lineage:
  - asset_id: string
    asset_type: string
    upstream_sources:
      - source: string
        source_type: string
        field: string
    transformations:
      - string
    downstream_assets:
      - string
```

### 15.2 Fraud lineage examples

```yaml
lineage:
  - asset_id: amount_spike_signal
    asset_type: fraud_signal
    upstream_sources:
      - source: fraud/features.py::build_features
        source_type: python_function
        field: abs_amount
      - source: fraud/detector.py::predict_fraud
        source_type: python_function
        field: is_spike
    transformations:
      - abs_amount derived from absolute transaction amount
      - is_spike derived from amount threshold comparison
    downstream_assets:
      - predicted_fraud
      - fraud_alert
      - fraud_score

  - asset_id: velocity_burst_signal
    asset_type: fraud_signal
    upstream_sources:
      - source: fraud/features.py::build_features
        source_type: python_function
        field: same_ts_count
      - source: fraud/detector.py::predict_fraud
        source_type: python_function
        field: is_velocity
    transformations:
      - same_ts_count derived from count of transactions for same account and timestamp
      - is_velocity derived from threshold comparison
    downstream_assets:
      - predicted_fraud
      - fraud_alert
      - fraud_score

  - asset_id: fraud_precision
    asset_type: evaluation_metric
    upstream_sources:
      - source: predicted_fraud
        source_type: prediction_output
      - source: fraud_label
        source_type: label
    transformations:
      - true positives and false positives calculated by comparing predicted_fraud to fraud_label
      - fraud_precision calculated as TP / (TP + FP)
    downstream_assets:
      - certification_report
```

---

## 16. Semantic SQL views

The MVP should generate basic SQL views. These are drafts, not production-ready warehouse models.

### 16.1 Certified transaction draft

```sql
CREATE OR REPLACE VIEW certified_transaction AS
SELECT
    txn_id,
    account_id,
    amount,
    ABS(amount) AS abs_amount,
    txn_type,
    merchant_category,
    timestamp,
    fraud_flag AS fraud_label
FROM transactions;
```

### 16.2 Certified transaction fraud signal draft

```sql
CREATE OR REPLACE VIEW certified_transaction_fraud_signal AS
SELECT
    txn_id,
    account_id,
    abs_amount,
    same_ts_count,
    z_score,
    account_zscore,
    is_burst,
    account_had_burst,
    is_spike,
    is_velocity,
    is_anomaly,
    fraud_score,
    predicted_fraud
FROM transaction_features;
```

### 16.3 Certified fraud alert draft

```sql
CREATE OR REPLACE VIEW certified_fraud_alert AS
SELECT
    txn_id,
    account_id,
    predicted_fraud,
    fraud_score,
    is_spike,
    is_velocity,
    is_anomaly,
    CASE
        WHEN is_velocity THEN 'Velocity burst'
        WHEN is_spike THEN 'Amount spike'
        WHEN is_anomaly THEN 'Statistical anomaly'
        ELSE 'No alert'
    END AS primary_alert_reason
FROM certified_transaction_fraud_signal
WHERE predicted_fraud = TRUE;
```

### 16.4 Fraud model run metrics draft

```sql
CREATE OR REPLACE VIEW fraud_model_run_metrics AS
SELECT
    model_run_id,
    SUM(CASE WHEN predicted_fraud = TRUE AND fraud_label = TRUE THEN 1 ELSE 0 END) AS true_positive,
    SUM(CASE WHEN predicted_fraud = TRUE AND fraud_label = FALSE THEN 1 ELSE 0 END) AS false_positive,
    SUM(CASE WHEN predicted_fraud = FALSE AND fraud_label = TRUE THEN 1 ELSE 0 END) AS false_negative,
    SUM(CASE WHEN predicted_fraud = FALSE AND fraud_label = FALSE THEN 1 ELSE 0 END) AS true_negative,

    true_positive / NULLIF(true_positive + false_positive, 0) AS fraud_precision,
    true_positive / NULLIF(true_positive + false_negative, 0) AS fraud_recall,
    2 * fraud_precision * fraud_recall / NULLIF(fraud_precision + fraud_recall, 0) AS fraud_f1_score
FROM fraud_predictions
GROUP BY model_run_id;
```

Note: SQL dialects vary in whether aliases can be reused in the same SELECT. A production renderer should generate dialect-safe SQL.

---

## 17. AI context cards

AI context cards define how AI systems can safely consume semantic assets.

### 17.1 AI context card schema

```yaml
ai_context_cards:
  - asset: string
    business_description: string
    allowed_questions:
      - string
    disallowed_questions:
      - string
    required_caveats:
      - string
    safe_join_paths:
      - string
    default_filters:
      - string
    sensitive_fields:
      - string
    refusal_rules:
      - string
```

### 17.2 Fraud alert AI context card

```yaml
ai_context_cards:
  - asset: certified_fraud_alert
    business_description: >
      Contains transactions flagged as suspicious based on candidate fraud signal rules.
      Fraud alerts are indicators for analyst review, not final determinations of fraud.

    allowed_questions:
      - Why was this transaction flagged?
      - Which fraud signals contributed to this alert?
      - What is the fraud score for this transaction?
      - Which accounts have the most alerts?
      - What is the detector precision for this model run?

    disallowed_questions:
      - Is this customer definitely committing fraud?
      - Should this customer account be closed automatically?
      - Should this transaction be blocked without review?
      - Should we report this customer without investigation?

    required_caveats:
      - Fraud alerts are indicators, not final determinations.
      - Human review is required.
      - Signal thresholds require business approval.
      - Evaluation metrics depend on the quality of the available fraud label.

    safe_join_paths:
      - certified_fraud_alert.account_id -> certified_business_account.account_id
      - certified_business_account.customer_id -> certified_business_customer.customer_id

    default_filters:
      - predicted_fraud = true

    sensitive_fields:
      - customer_name
      - account_id
      - txn_id
      - transaction_amount

    refusal_rules:
      - Refuse to make final fraud determinations about a customer.
      - Refuse to recommend adverse action without human investigation.
      - Refuse to expose restricted transaction-level details to unauthorised users.
```

---

## 18. Certification report

The certification report is the human-readable review output.

### 18.1 Report structure

```markdown
# Certification Report: Business Banking Fraud Detection

## Package Summary

## Overall Status

## Generated Artefacts

## Certifiable Assets

## Candidate Assets

## Experimental Assets

## Blocking Issues

## Governance Gaps

## Data Quality Gaps

## AI Usage Boundaries

## Recommended Next Actions
```

### 18.2 Example certification report content

```markdown
# Certification Report: Business Banking Fraud Detection

## Package Summary

Semantic_Foundry generated a draft semantic package for business banking fraud detection.

The package contains:
- 5 semantic entities
- 4 fraud signals
- 1 prediction output
- 1 fraud score
- 3 evaluation metrics
- 7 data quality rules
- 4 policy rules
- 1 AI context card

## Overall Status

Status: Candidate with blocking issues

## Candidate Assets

- Transaction
- Fraud Alert
- Amount Spike Signal
- Velocity Burst Signal
- Statistical Anomaly Signal
- Predicted Fraud Indicator

## Experimental Assets

- Account Burst History Signal

## Draft Assets

- Business Customer
- Business Account
- Fraud Model Run
- Fraud Precision
- Fraud Recall
- Fraud F1 Score

## Blocking Issues

1. The source and meaning of `fraud_label` must be confirmed.
2. Signal thresholds require Fraud Risk Owner approval.
3. Transaction-level access controls must be implemented.
4. Human review policy must be approved before operational use.
5. DQ checks must be executed against actual physical tables.
6. The exact time window for velocity burst detection must be clarified.
7. SQL views are draft and require platform-specific validation.

## AI Usage Boundaries

Allowed:
- Explain why a transaction was flagged
- Identify contributing fraud signals
- Summarise detector performance metrics
- Support analyst investigation

Not allowed:
- Declare a customer guilty of fraud
- Recommend account closure without human review
- Use predicted fraud as sole basis for adverse action

## Recommended Next Actions

1. Confirm fraud label provenance.
2. Validate signal definitions with fraud analysts.
3. Approve or revise thresholds.
4. Execute DQ rules against sample data.
5. Review policy and human-review rules.
6. Validate generated SQL on target platform.
7. Promote approved assets from draft to candidate or certified.
```

---

## 19. Internal code architecture

The next build phase should focus on output quality, not additional scanners.

### 19.1 Recommended module structure

```text
semantic_foundry/
├── cli.py
├── config.py
│
├── discovery/
│   ├── discovery_model.py
│   └── discovery_loader.py
│
├── classifiers/
│   └── artefact_classifier.py
│
├── catalogues/
│   ├── semantic_catalogue_builder.py
│   ├── signal_catalogue_builder.py
│   ├── metric_catalogue_builder.py
│   ├── dq_catalogue_builder.py
│   ├── policy_catalogue_builder.py
│   └── lineage_builder.py
│
├── renderers/
│   ├── yaml_renderer.py
│   ├── sql_renderer.py
│   └── markdown_report_renderer.py
│
├── validators/
│   ├── catalogue_schema_validator.py
│   ├── formula_validator.py
│   ├── sql_validator.py
│   └── certification_validator.py
│
├── packages/
│   ├── package_manifest.py
│   └── package_writer.py
│
└── templates/
    ├── package_manifest.yaml.j2
    ├── semantic_catalogue.yaml.j2
    ├── signal_catalogue.yaml.j2
    ├── metric_catalogue.yaml.j2
    ├── dq_rules.yaml.j2
    ├── policy_rules.yaml.j2
    ├── lineage.yaml.j2
    ├── ai_context_cards.yaml.j2
    └── certification_report.md.j2
```

---

## 20. Canonical internal models

### 20.1 Discovered artefact

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class DiscoveredArtefact:
    name: str
    source_type: str
    source_reference: str
    function_name: Optional[str] = None
    module_path: Optional[str] = None
    discovered_as: Optional[str] = None
```

Example:

```json
{
  "name": "is_velocity",
  "source_type": "python_ast",
  "source_reference": "fraud/detector.py::predict_fraud",
  "function_name": "predict_fraud",
  "module_path": "fraud/detector.py",
  "discovered_as": "return_name"
}
```

### 20.2 Classified artefact

```python
@dataclass
class ClassifiedArtefact:
    name: str
    source_name: str
    layer: str
    asset_type: str
    confidence: float
    reason: str
    source_reference: str
```

Example:

```json
{
  "name": "velocity_burst_signal",
  "source_name": "is_velocity",
  "layer": "signal_layer",
  "asset_type": "fraud_signal",
  "confidence": 0.95,
  "reason": "Boolean velocity flag returned by predict_fraud",
  "source_reference": "fraud/detector.py::predict_fraud"
}
```

### 20.3 Semantic asset

```python
@dataclass
class SemanticAsset:
    asset_id: str
    name: str
    asset_type: str
    description: str
    grain: Optional[str]
    owner: str
    sensitivity: str
    certification_status: str
```

### 20.4 Signal asset

```python
@dataclass
class SignalAsset:
    signal_id: str
    name: str
    source_field: str
    entity: str
    signal_type: str
    definition: str
    logic: str
    owner: str
    status: str
```

### 20.5 Metric asset

```python
@dataclass
class MetricAsset:
    metric_id: str
    name: str
    metric_type: str
    definition: str
    grain: str
    formula: str
    owner: str
    status: str
```

---

## 21. CLI design

### 21.1 Build command

```bash
semantic-foundry build \
  --use-case examples/business_banking_fraud/use_case.yaml \
  --discovery outputs/business_banking_fraud/discovery_report.json \
  --target generic_sql \
  --out outputs/business_banking_fraud_semantic_package
```

### 21.2 Validate command

```bash
semantic-foundry validate \
  --package outputs/business_banking_fraud_semantic_package
```

### 21.3 Render command

```bash
semantic-foundry render \
  --package outputs/business_banking_fraud_semantic_package \
  --format markdown
```

### 21.4 Package command

```bash
semantic-foundry package \
  --package outputs/business_banking_fraud_semantic_package \
  --version 0.1.0
```

---

## 22. Build pipeline

```text
Load use_case.yaml
      ↓
Load discovery_report.json
      ↓
Extract discovered artefacts
      ↓
Classify artefacts
      ↓
Build semantic catalogue
      ↓
Build signal catalogue
      ↓
Build metric catalogue
      ↓
Build DQ rules
      ↓
Build policy rules
      ↓
Build lineage
      ↓
Render semantic SQL
      ↓
Render AI context cards
      ↓
Run validators
      ↓
Generate certification report
      ↓
Write semantic package
```

---

## 23. Validation gates

### 23.1 Package validation

Checks:

- Required files exist
- Manifest references valid files
- YAML files parse correctly
- Package ID matches use case ID
- Version exists

### 23.2 Catalogue validation

Checks:

- Every asset has an ID
- Every asset has a name
- Every asset has an owner
- Every asset has a status
- Every signal maps to an entity
- Every metric has a grain and formula

### 23.3 Policy validation

Checks:

- High-risk use cases have human review policy
- Transaction-level data has restricted access rule
- Fraud prediction outputs have disallowed-use boundaries
- AI context cards contain required caveats

### 23.4 Certification validation

Checks:

- No high-risk asset can be certified without owner
- No prediction output can be certified without policy rule
- No evaluation metric can be certified without label definition
- No signal can be certified without source reference and approved use
- No semantic entity can be certified without grain and primary key

---

## 24. MVP build priorities

### 24.1 Build now

1. Artefact classifier
2. Semantic catalogue generator
3. Signal catalogue generator
4. Metric catalogue generator
5. Policy and DQ catalogue generator
6. Certification report renderer
7. Package writer
8. Basic validators

### 24.2 Defer

1. dbt scanner
2. Airflow scanner
3. Power BI scanner
4. Looker scanner
5. ETL lineage scanner
6. Snowflake-specific deployment
7. Databricks-specific deployment

Reason:

> More scanners increase input coverage, but the current product risk is output value. Prove that the package generated from one use case is useful, reviewable, and credible before expanding connectors.

---

## 25. MVP success criteria

The next MVP is successful when one command can generate a complete semantic package for the fraud use case.

### 25.1 Functional success

```text
Given:
- use_case.yaml
- discovery_report.json from Python AST mining

Generate:
- package_manifest.yaml
- semantic_catalogue.yaml
- signal_catalogue.yaml
- metric_catalogue.yaml
- dq_rules.yaml
- policy_rules.yaml
- lineage.yaml
- semantic_views.sql
- ai_context_cards.yaml
- certification_report.md
```

### 25.2 Quality success

The package should clearly answer:

| Question | Expected answer |
|---|---|
| What business entities are in scope? | Customer, Account, Transaction, Fraud Alert, Model Run |
| What behavioural signals are in scope? | Amount Spike, Velocity Burst, Statistical Anomaly, Account Burst History |
| What prediction outputs exist? | Predicted Fraud, Fraud Score |
| What evaluation metrics exist? | Precision, Recall, F1 Score |
| What governance boundaries apply? | Human review, restricted access, explainability required |
| What blocks certification? | Label provenance, thresholds, DQ execution, policy approval |
| How can AI safely use this package? | Via AI context cards and refusal rules |

---

## 26. Consulting delivery use

For a consulting agency, the semantic package is the main reusable deliverable.

### 26.1 Client-facing story

```text
We started with your existing fraud detection scripts.

Semantic_Foundry discovered:
- business entities
- feature logic
- signal candidates
- fraud prediction outputs
- evaluation metrics
- governance gaps

It generated:
- semantic catalogue
- signal catalogue
- metric catalogue
- policy rules
- data quality rules
- draft SQL views
- AI context cards
- certification report
```

### 26.2 Consulting engagement stages

```text
Week 1: Use case intake and discovery
Week 2: Semantic package generation
Week 3: Business and risk review
Week 4: DQ validation and semantic view implementation
Week 5: AI consumption contract and demo
Week 6: Certification roadmap and scale-out plan
```

---

## 27. Key design distinction

The semantic package should not be confused with the semantic layer.

| Concept | Meaning |
|---|---|
| Semantic package | Portable bundle of definitions, rules, views, policies, and metadata |
| Semantic layer | Implemented governed layer in the data platform |
| Signal layer | Behavioural indicators built on top of semantic assets |
| Evaluation layer | Metrics used to assess detector/model performance |
| AI contract | Rules for how AI can consume the semantic assets |

A package is a reviewable and deployable unit.

```text
Semantic Package
      ↓
Deployment / Review / Certification
      ↓
Enterprise Semantic Layer
      ↓
Signal Layer and AI Consumption
```

---

## 28. Recommended next implementation task

Build:

```text
Artefact Classifier + Catalogue Generator + Certification Report
```

Input:

```text
- current discovery JSON
- use_case.yaml
- owner defaults
- target platform
```

Output:

```text
- semantic_catalogue.yaml
- signal_catalogue.yaml
- metric_catalogue.yaml
- dq_rules.yaml
- policy_rules.yaml
- ai_context_cards.yaml
- certification_report.md
```

This is the shortest path from scaffolding to visible consulting value.

---

## 29. Summary

A Semantic_Foundry semantic package is the bridge between messy client reality and governed AI-ready data.

It converts:

```text
Existing code, tables, features, and assumptions
```

Into:

```text
A governed, reviewable, certifiable semantic package
```

For the fraud use case, this means moving from Python functions such as `build_features` and `predict_fraud` to a business-ready package containing:

- Business Customer
- Business Account
- Transaction
- Fraud Alert
- Amount Spike Signal
- Velocity Burst Signal
- Statistical Anomaly Signal
- Predicted Fraud Indicator
- Fraud Score
- Fraud Precision
- Fraud Recall
- Fraud F1 Score
- DQ rules
- Policy rules
- AI usage boundaries
- Certification report

That is the point where Semantic_Foundry becomes more than a scanner. It becomes a semantic-layer accelerator.
