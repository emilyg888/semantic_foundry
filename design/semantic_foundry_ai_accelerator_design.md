# Semantic_Foundry AI Accelerator Design

## Purpose

**Semantic_Foundry** is an AI-assisted consulting accelerator for building an enterprise semantic layer for a specific business use case when business glossary, logical model, metrics, semantic views, and governance controls are missing or immature.

The accelerator takes an existing analytical dataset, data warehouse/lake tables, scripts, SQL, notebooks, or feature pipeline and converts them into governed, certified, AI-ready semantic assets.

Core principle:

```text
LLM proposes.
Code enforces.
Business certifies.
```

For the business banking fraud scenario, the accelerator turns existing data and fraud detection logic into a governed fraud semantic layer containing customers, accounts, transactions, fraud signals, alert metrics, data quality controls, policy gates, and AI-safe explanation contracts.

---

## Input and Output

### Inputs

```text
Business use case description
Existing datasets / warehouse tables
Existing SQL / Python / dbt / notebooks
Column names and sample data
Existing reports or ML features
Known business rules
Known data quality issues
Known policies / privacy constraints
```

### Fraud example input

```text
Use case:
- Fraud detection for SME business banking

Tables / datasets:
- customers
- accounts
- transactions

Code assets:
- dataset generators
- feature engineering
- rule-based fraud detection
- logistic regression baseline
- validators
- DuckDB loader

Existing analytical concepts:
- fraud_flag
- predicted_fraud
- abs_amount
- txn_count
- same_ts_count
- z_score
- account_zscore
- is_spike
- is_velocity
- is_anomaly
- is_burst
- account_had_burst
- fraud_score
```

### Outputs

```text
semantic_foundry_output/
├── 01_domain_blueprint/
│   ├── business_use_case.md
│   ├── domain_concept_model.md
│   └── stakeholder_raci.md
│
├── 02_glossary/
│   ├── business_glossary.yaml
│   └── term_candidates_review.md
│
├── 03_logical_model/
│   ├── entity_model.yaml
│   ├── relationship_model.yaml
│   └── grain_definitions.yaml
│
├── 04_metrics_and_signals/
│   ├── metric_catalogue.yaml
│   ├── signal_catalogue.yaml
│   └── fraud_typology_mapping.yaml
│
├── 05_semantic_views/
│   ├── certified_customer.sql
│   ├── certified_account.sql
│   ├── certified_transaction.sql
│   ├── certified_fraud_signal.sql
│   └── semantic_manifest.yaml
│
├── 06_governance_controls/
│   ├── dq_rules.yaml
│   ├── policy_rules.yaml
│   ├── lineage.yaml
│   ├── certification_checklist.yaml
│   └── issue_register.yaml
│
├── 07_ai_consumption/
│   ├── ai_context_cards.yaml
│   ├── text_to_sql_guardrails.yaml
│   ├── approved_questions.yaml
│   ├── refusal_rules.yaml
│   └── evaluation_questions.yaml
│
└── 08_delivery_pack/
    ├── semantic_layer_readout.md
    ├── implementation_backlog.md
    └── scale_out_roadmap.md
```

---

## Reference Architecture

```text
                      ┌─────────────────────────────┐
                      │ Business Use Case Intake     │
                      │ Fraud, churn, risk, service  │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────┐
│                  Semantic_Foundry AI Accelerator                │
├────────────────────────────────────────────────────────────────┤
│  1. Data Profiler                                                │
│  2. Code & Logic Miner                                           │
│  3. Business Concept Extractor                                   │
│  4. Entity Model Builder                                         │
│  5. Metric & Signal Designer                                     │
│  6. DQ Rule Generator                                            │
│  7. Policy & Sensitivity Classifier                              │
│  8. Semantic View Generator                                      │
│  9. AI Contract Generator                                        │
│ 10. Certification Gate                                           │
└────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ Governed Semantic Layer      │
                      │ Certified and AI-ready       │
                      └─────────────────────────────┘
```

---

## Accelerator Modules

### 1. Use Case Intake Agent

Converts a business objective into a scoped semantic build request.

Example:

```yaml
use_case_id: business_banking_fraud_detection
business_objective: Detect suspicious SME banking transactions and explain contributing signals.
primary_users:
  - fraud analyst
  - financial crime operations
  - risk manager
  - data scientist
business_questions:
  - Which transactions are suspicious?
  - Why was a transaction flagged?
  - Which accounts show burst behaviour?
  - Which customer segments carry higher fraud signal exposure?
  - Which rules contribute most to alerts?
decision_type: analyst_assisted
automation_level: human_in_the_loop
risk_level: high
```

---

### 2. Data Profiler

Discovers physical datasets, keys, relationships, grain, data types, and candidate sensitive fields.

Fraud example:

```yaml
tables:
  customers:
    grain: one row per business customer
    primary_key: customer_id
    candidate_sensitive_fields:
      - name
      - country
      - risk_rating

  accounts:
    grain: one row per business account
    primary_key: account_id
    foreign_keys:
      - customer_id

  transactions:
    grain: one row per transaction event
    primary_key: txn_id
    foreign_keys:
      - account_id
    time_column: timestamp
    label_column: fraud_flag
```

---

### 3. Code and Logic Miner

Extracts hidden business logic from code, SQL, notebooks, dbt, and feature pipelines.

Fraud example extracted logic:

```text
abs_amount = absolute value of transaction amount
txn_count = transaction count by account
same_ts_count = number of transactions for same account at same timestamp
z_score = global z-score of absolute transaction amount
account_zscore = account-level z-score of absolute transaction amount
is_burst = same_ts_count >= 3
account_had_burst = account had at least one burst transaction
is_spike = abs_amount > threshold
is_velocity = same_ts_count >= threshold
is_anomaly = abs(z_score) > threshold
predicted_fraud = is_spike OR is_velocity OR is_anomaly
```

Candidate signal output:

```yaml
candidate_signals:
  - signal_name: transaction_amount_spike
    source_logic: abs_amount > spike_threshold
    default_threshold: 20000
    business_interpretation: Transaction amount materially exceeds expected range.
    certification_status: candidate

  - signal_name: transaction_velocity_burst
    source_logic: same_ts_count >= same_ts_threshold
    default_threshold: 3
    business_interpretation: Multiple transactions occurred for the same account at the same timestamp.
    certification_status: candidate

  - signal_name: statistical_amount_anomaly
    source_logic: abs(z_score) > zscore_threshold
    default_threshold: 3.0
    business_interpretation: Transaction amount is statistically unusual compared with the global transaction distribution.
    certification_status: candidate
```

---

### 4. Target Semantic Model

```text
Business Customer
        │ owns
        ▼
Business Account
        │ has
        ▼
Transaction
        │ produces
        ▼
Fraud Signal
        │ contributes to
        ▼
Fraud Alert / Fraud Score
```

Core entities:

| Entity | Grain | Description |
|---|---:|---|
| Business Customer | One row per customer | SME or business banking customer |
| Business Account | One row per account | Business account owned by a customer |
| Transaction | One row per transaction event | Monetary event on an account |
| Fraud Signal | One row per transaction-signal pair or derived signal value | Explainable suspicious behaviour indicator |
| Fraud Alert | One row per flagged transaction/account event | Operational alert requiring review |
| Fraud Evaluation | One row per model/rule evaluation run | Measures detector performance |

---

### 5. Business Glossary Generator

Produces draft terms for business review.

```yaml
terms:
  - name: Business Customer
    definition: A commercial customer that holds or has held a business banking relationship.
    domain: Business Banking
    owner: Business Banking Data Owner
    sensitivity: confidential
    certification_status: draft

  - name: Business Account
    definition: A bank account used for business banking activity and linked to a business customer.
    domain: Business Banking
    owner: Business Banking Data Owner
    sensitivity: confidential
    certification_status: draft

  - name: Transaction
    definition: A recorded credit or debit event against a business account.
    domain: Payments
    owner: Payments Data Owner
    sensitivity: restricted
    certification_status: candidate

  - name: Fraud Signal
    definition: A calculated indicator that suggests potentially suspicious transaction or account behaviour.
    domain: Fraud Risk
    owner: Fraud Risk Owner
    sensitivity: restricted
    certification_status: candidate

  - name: Velocity Burst
    definition: Multiple transactions for the same account occurring at the same timestamp or within a defined short time window.
    domain: Fraud Risk
    owner: Fraud Risk Owner
    certification_status: candidate

  - name: Amount Spike
    definition: A transaction whose absolute amount exceeds an approved suspicious-amount threshold.
    domain: Fraud Risk
    owner: Fraud Risk Owner
    certification_status: candidate
```

---

### 6. Metrics and Signals

Semantic_Foundry separates **metrics** from **signals**.

Metrics are aggregate measures. Signals are explainable behavioural indicators.

#### Candidate metrics

```yaml
metrics:
  - name: fraud_alert_count
    definition: Count of transactions flagged as predicted fraud.
    grain: daily, account, customer, merchant_category
    formula: count where predicted_fraud = true
    owner: Fraud Operations
    certification_status: candidate

  - name: confirmed_fraud_rate
    definition: Percentage of transactions labelled as confirmed fraud.
    formula: confirmed_fraud_transactions / total_transactions
    owner: Fraud Risk
    certification_status: candidate

  - name: detector_precision
    definition: Percentage of predicted fraud transactions that are confirmed fraud.
    formula: true_positive / (true_positive + false_positive)
    owner: Fraud Analytics
    certification_status: candidate

  - name: detector_recall
    definition: Percentage of confirmed fraud transactions detected by the detector.
    formula: true_positive / (true_positive + false_negative)
    owner: Fraud Analytics
    certification_status: candidate
```

#### Candidate signals

```yaml
signals:
  - name: amount_spike_signal
    entity: Transaction
    logic: abs_amount > spike_threshold
    default_threshold: 20000
    explainability: high
    approved_use: fraud triage and analyst prioritisation
    disallowed_use: sole basis for adverse customer action
    certification_status: candidate

  - name: velocity_burst_signal
    entity: Transaction
    logic: same_ts_count >= same_ts_threshold
    default_threshold: 3
    explainability: high
    approved_use: identify rapid repeated transaction behaviour
    certification_status: candidate

  - name: statistical_anomaly_signal
    entity: Transaction
    logic: abs(z_score) > zscore_threshold
    default_threshold: 3.0
    explainability: medium
    approved_use: anomaly screening
    certification_status: candidate

  - name: account_level_burst_signal
    entity: Account
    logic: account_had_burst = true
    explainability: medium
    known_limitation: May contaminate account history by flagging normal transactions from previously bursty accounts.
    certification_status: experimental
```

---

### 7. Semantic View Design

Minimum semantic views:

```text
certified_business_customer
certified_business_account
certified_transaction
certified_transaction_fraud_signal
certified_fraud_alert
```

Example semantic asset contract:

```yaml
asset: certified_transaction_fraud_signal
grain: one row per transaction with derived fraud signals
owner: Fraud Analytics Owner
sensitivity: restricted
certification_status: candidate
approved_use:
  - fraud triage
  - fraud analyst explanation
  - model/rule evaluation
disallowed_use:
  - fully automated adverse action without human review
known_limitations:
  - thresholds are calibrated against current data distribution
  - statistical anomaly may drift as transaction behaviour changes
  - synthetic labels may not represent real confirmed fraud
```

---

### 8. Data Quality Rule Generator

```yaml
dq_rules:
  - id: customer_id_not_null
    entity: Business Customer
    column: customer_id
    rule_type: completeness
    expression: customer_id IS NOT NULL
    severity: critical

  - id: account_customer_valid
    entity: Business Account
    rule_type: referential_integrity
    expression: accounts.customer_id exists in customers.customer_id
    severity: critical

  - id: transaction_account_valid
    entity: Transaction
    rule_type: referential_integrity
    expression: transactions.account_id exists in accounts.account_id
    severity: critical

  - id: fraud_flag_boolean
    entity: Transaction
    column: fraud_flag
    rule_type: validity
    expression: fraud_flag IN (true, false)
    severity: high
```

Certification status is then driven by deterministic checks:

```text
DQ failed → Not certifiable
DQ warning → Candidate
DQ passed + owner approved → Certified
```

---

### 9. Policy and Governance Layer

```yaml
policy_rules:
  - id: fraud_human_review_required
    applies_to:
      - certified_fraud_alert
      - certified_transaction_fraud_signal
    rule: Fraud predictions must support analyst review, not fully automated adverse action.
    enforcement: ai_response_guardrail
    severity: critical

  - id: restricted_transaction_access
    applies_to:
      - certified_transaction
      - certified_transaction_fraud_signal
      - certified_fraud_alert
    rule: Transaction-level records require restricted access.
    enforcement: rbac
    severity: critical

  - id: explainability_required
    applies_to:
      - certified_fraud_alert
    rule: Every fraud alert must include contributing signal reasons.
    enforcement: semantic_contract
    severity: high
```

---

### 10. AI Consumption Contracts

AI context card example:

```yaml
ai_context_card:
  asset: certified_fraud_alert
  business_description: >
    Contains transactions flagged as suspicious based on certified fraud signal rules.
  allowed_questions:
    - Which transactions were flagged as suspicious?
    - Why was this transaction flagged?
    - Which fraud signals contributed to the alert?
    - What is the precision and recall of the current detector?
  disallowed_questions:
    - Should this customer be automatically exited?
    - Should this transaction be blocked without review?
    - Is this customer definitely committing fraud?
  required_caveats:
    - Fraud alerts are indicators, not final determinations.
    - Human review is required.
    - Thresholds and signals must be monitored for drift.
  safe_join_paths:
    - certified_fraud_alert.account_id -> certified_business_account.account_id
    - certified_business_account.customer_id -> certified_business_customer.customer_id
  default_filters:
    - predicted_fraud = true
  sensitive_fields:
    - customer_name
    - account_id
    - transaction_id
```

---

## Accelerator Workflow

```text
Step 1: Use case intake
    ↓
Step 2: Profile existing data and code
    ↓
Step 3: Extract candidate business concepts
    ↓
Step 4: Generate draft glossary
    ↓
Step 5: Generate logical entity model
    ↓
Step 6: Generate candidate metrics and signals
    ↓
Step 7: Generate DQ and policy controls
    ↓
Step 8: Generate semantic views
    ↓
Step 9: Generate AI context contracts
    ↓
Step 10: Run validation gates
    ↓
Step 11: Human review and certification
    ↓
Step 12: Publish semantic layer package
```

---

## Where AI Should and Should Not Be Used

### Use AI for judgement-heavy work

```text
Business concept extraction
Glossary drafting
Entity modelling suggestions
Metric and signal interpretation
Policy classification suggestions
AI context card generation
Documentation generation
Review question generation
```

### Use deterministic logic for control

```text
Schema profiling
Primary key checks
Foreign key checks
Data type checks
DQ validation
SQL generation validation
Lineage dependency extraction
Certification gate enforcement
Policy rule enforcement
Metric formula testing
```

---

## MVP Build

```text
semantic-foundry build --use-case fraud_detection --source ./bb_datasets
```

Produces:

```text
outputs/fraud_detection_semantic_layer/
├── glossary.yaml
├── entities.yaml
├── metrics.yaml
├── signals.yaml
├── dq_rules.yaml
├── policies.yaml
├── semantic_views.sql
├── ai_context_cards.yaml
└── certification_report.md
```

---

## Proposed Project Folder Structure

```text
semantic_foundry/
├── README.md
├── pyproject.toml
│
├── semantic_foundry/
│   ├── cli.py
│   ├── config.py
│   │
│   ├── intake/
│   ├── scanners/
│   ├── generators/
│   ├── builders/
│   ├── validators/
│   ├── review/
│   └── templates/
│
├── examples/
│   └── business_banking_fraud/
│
├── tests/
└── outputs/
```

---

## Consulting Engagement Model

### 4-week accelerator

```text
Week 1: Use case intake + data/code profiling
Week 2: Draft glossary + entity model + metrics/signals
Week 3: Build semantic views + DQ/policy controls
Week 4: AI consumption contracts + certification readout
```

### 6-week accelerator

```text
Week 1: Discovery and scope
Week 2: Data/code profiling and concept extraction
Week 3: Business glossary and logical model
Week 4: Metrics, signals, DQ, policy rules
Week 5: Semantic view implementation
Week 6: AI enablement and certification pack
```

---

## One-line Product Concept

**Semantic_Foundry is an AI-assisted accelerator that turns existing data, code, metrics, and analytical logic into governed, certified, AI-ready semantic assets for a specific enterprise business use case.**
