# Semantic_Foundry Detailed Design

## 1. Design Intent

**Semantic_Foundry** is a reusable AI engagement accelerator for consulting teams that need to create an enterprise semantic layer for a specific business use case when the client has poor or missing governance, glossary, logical data model, certified metrics, and AI consumption controls.

The accelerator is not only a documentation generator. It is a semantic engineering pipeline:

```text
Existing Data + Code + Use Case
        ↓
AI-assisted discovery and semantic proposal
        ↓
Deterministic validation and governance gates
        ↓
Human certification workflow
        ↓
Published AI-ready semantic package
```

The first reference implementation is based on the attached business banking fraud detection codebase. The archive contains:

```text
datasets/
├── generator.py
├── generator_v2.py
├── generator_v3.py
├── loader.py
├── registry.py
├── schema.py
└── validator.py

fraud/
├── detector.py
├── features.py
├── load.py
└── run_fraud.py

run_dataset.py
```

Key logic discovered from the codebase:

```text
Dataset domain:
- SME business banking

Core tables:
- customers
- accounts
- transactions

Fraud feature logic:
- abs_amount
- txn_count
- same_ts_count
- z_score
- account_zscore
- is_burst
- account_had_burst

Fraud detector logic:
- is_spike
- is_velocity
- is_anomaly
- is_account_burst
- is_temporal_burst
- predicted_fraud
- fraud_score

Evaluation logic:
- true positive
- false positive
- false negative
- true negative
- precision
- recall
- f1
```

---

## 2. Design Goals

### Business goals

1. Reduce the time required to build a first semantic layer for a high-value enterprise use case.
2. Make data AI-ready by adding business meaning, ownership, policy, data quality, lineage, and safe AI usage contracts.
3. Help consulting teams demonstrate value quickly without pretending the client already has mature governance.
4. Create a repeatable methodology that can be reused across fraud, customer churn, claims, operations, service, finance, risk, HR, and regulatory reporting domains.

### Technical goals

1. Scan data and code to infer candidate semantic assets.
2. Generate draft glossary, entity model, metric catalogue, signal catalogue, DQ rules, policy rules, semantic SQL, and AI context cards.
3. Keep AI-generated outputs behind deterministic validators.
4. Track all generated artefacts as versioned files.
5. Support human review and certification before semantic assets are promoted.
6. Start platform-neutral, then add adapters for Snowflake, Databricks, dbt, Power BI, Looker, and other semantic technologies.

---

## 3. Non-goals

The MVP should not try to:

1. Replace enterprise data governance platforms.
2. Automatically certify business definitions without human review.
3. Automatically deploy production views into a client environment without approval.
4. Build a full enterprise canonical data model.
5. Support every data platform from day one.
6. Allow LLMs to execute unrestricted SQL or inspect unrestricted sensitive data.

---

## 4. Core Design Principles

### 4.1 Use case first

The accelerator starts with a business decision or business question, not a data catalogue.

```text
Bad starting point:
What tables do we have?

Better starting point:
What business decision must AI or analytics support safely?
```

For the fraud example:

```text
Decision:
Help fraud analysts identify and explain suspicious SME banking transactions.

Semantic scope:
Customers, accounts, transactions, fraud signals, alerts, detector performance, policy caveats.
```

### 4.2 LLM proposes, deterministic code enforces

```text
LLM responsibilities:
- infer business concepts
- draft definitions
- suggest entity relationships
- interpret code logic
- propose metrics and signals
- generate review questions
- produce documentation

Deterministic responsibilities:
- schema profiling
- uniqueness checks
- referential integrity checks
- SQL linting
- YAML schema validation
- certification gate enforcement
- policy gate enforcement
- data quality result calculation
```

### 4.3 Semantic assets are contracts

A semantic view is not just SQL. It must include:

```text
Business definition
Grain
Owner
Keys
Relationships
Metric or signal logic
Data quality checks
Sensitivity classification
Approved and disallowed use
Lineage
Certification status
AI consumption contract
```

### 4.4 AI should consume certified semantic assets only

Default rule:

```text
Enterprise AI consumers should only retrieve from, query, or explain certified semantic assets unless explicitly operating in exploratory mode.
```

---

## 5. High-level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     Client Inputs                            │
│ Use case, tables, SQL, Python, dbt, notebooks, docs, reports │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Semantic_Foundry Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│ 01 Intake                                                    │
│ 02 Source Scanner                                            │
│ 03 Data Profiler                                             │
│ 04 Code & Logic Miner                                        │
│ 05 Concept Extractor                                         │
│ 06 Entity Model Generator                                    │
│ 07 Metric & Signal Generator                                 │
│ 08 DQ Rule Generator                                         │
│ 09 Policy Classifier                                         │
│ 10 Semantic View Builder                                     │
│ 11 AI Contract Builder                                       │
│ 12 Validator & Certification Gate                            │
│ 13 Delivery Pack Publisher                                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Semantic Package Output                    │
│ Glossary, entities, metrics, signals, views, DQ, policy, AI  │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Runtime Modes

Semantic_Foundry should support three runtime modes.

### 6.1 Discovery mode

Used early in an engagement.

```text
Input: source folder + use case description
Output: candidate concepts, entities, metrics, signals, issues
Certification: none
```

### 6.2 Build mode

Used to generate semantic artefacts.

```text
Input: source folder + reviewed use case + configuration
Output: full semantic package
Certification: draft/candidate only
```

### 6.3 Certification mode

Used after human review.

```text
Input: semantic package + approvals + validation results
Output: certified or rejected semantic assets
Certification: enforced
```

Example CLI:

```bash
semantic-foundry discover --source ./bb_datasets --use-case ./use_case.yaml
semantic-foundry build --source ./bb_datasets --use-case ./use_case.yaml --target generic_sql
semantic-foundry certify --package ./outputs/business_banking_fraud --approvals ./approvals.yaml
```

---

## 7. Project Structure

```text
semantic_foundry/
├── README.md
├── pyproject.toml
├── semantic_foundry/
│   ├── cli.py
│   ├── config.py
│   ├── runtime.py
│   ├── logging.py
│   │
│   ├── intake/
│   │   ├── use_case_schema.py
│   │   ├── intake_loader.py
│   │   └── scope_resolver.py
│   │
│   ├── scanners/
│   │   ├── source_inventory.py
│   │   ├── table_profiler.py
│   │   ├── python_logic_miner.py
│   │   ├── sql_miner.py
│   │   ├── dbt_miner.py
│   │   └── notebook_miner.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompts/
│   │   │   ├── concept_extraction.md
│   │   │   ├── glossary_generation.md
│   │   │   ├── entity_model_generation.md
│   │   │   ├── metric_signal_generation.md
│   │   │   ├── policy_classification.md
│   │   │   └── ai_contract_generation.md
│   │   └── structured_outputs.py
│   │
│   ├── generators/
│   │   ├── glossary_generator.py
│   │   ├── entity_model_generator.py
│   │   ├── relationship_generator.py
│   │   ├── metric_generator.py
│   │   ├── signal_generator.py
│   │   ├── dq_rule_generator.py
│   │   ├── policy_generator.py
│   │   └── ai_contract_generator.py
│   │
│   ├── builders/
│   │   ├── semantic_sql_builder.py
│   │   ├── manifest_builder.py
│   │   ├── dbt_builder.py
│   │   ├── snowflake_builder.py
│   │   └── databricks_builder.py
│   │
│   ├── validators/
│   │   ├── artefact_schema_validator.py
│   │   ├── source_schema_validator.py
│   │   ├── dq_validator.py
│   │   ├── sql_validator.py
│   │   ├── policy_validator.py
│   │   ├── lineage_validator.py
│   │   └── certification_validator.py
│   │
│   ├── review/
│   │   ├── certification_workflow.py
│   │   ├── approval_model.py
│   │   └── issue_register.py
│   │
│   ├── templates/
│   │   ├── glossary.yaml.j2
│   │   ├── entities.yaml.j2
│   │   ├── relationships.yaml.j2
│   │   ├── metrics.yaml.j2
│   │   ├── signals.yaml.j2
│   │   ├── dq_rules.yaml.j2
│   │   ├── policies.yaml.j2
│   │   ├── semantic_views.sql.j2
│   │   ├── ai_context_cards.yaml.j2
│   │   └── certification_report.md.j2
│   │
│   └── package/
│       ├── publisher.py
│       ├── versioning.py
│       └── manifest.py
│
├── examples/
│   └── business_banking_fraud/
│       ├── use_case.yaml
│       ├── source/
│       ├── expected_output/
│       └── README.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── outputs/
```

---

## 8. Core Data Contracts

### 8.1 Use case contract

File: `use_case.yaml`

```yaml
use_case:
  id: business_banking_fraud_detection
  name: Business Banking Fraud Detection
  domain: Business Banking / Fraud Risk
  description: Detect and explain suspicious SME banking transactions.
  business_objective: Reduce fraud loss and support analyst triage.
  decision_type: analyst_assisted
  automation_level: human_in_the_loop
  risk_level: high

users:
  - role: Fraud Analyst
    goals:
      - Review suspicious transactions
      - Understand alert reason
  - role: Fraud Risk Manager
    goals:
      - Monitor fraud trends
      - Review detector effectiveness
  - role: Data Scientist
    goals:
      - Evaluate feature and model performance

business_questions:
  - id: q1
    question: Which transactions are suspicious?
    expected_semantic_assets:
      - certified_fraud_alert
  - id: q2
    question: Why was a transaction flagged?
    expected_semantic_assets:
      - certified_transaction_fraud_signal
  - id: q3
    question: How well does the detector perform?
    expected_semantic_assets:
      - certified_fraud_detector_evaluation

constraints:
  data_sensitivity: restricted
  requires_human_review: true
  automated_adverse_action_allowed: false
  production_decisioning_allowed: false
```

---

### 8.2 Source inventory contract

File: `source_inventory.yaml`

```yaml
source_inventory:
  root_path: ./bb_datasets
  files:
    - path: datasets/generator_v3.py
      type: python
      role: synthetic_data_generator
      detected_concepts:
        - customer
        - account
        - transaction
        - fraud_flag
    - path: fraud/features.py
      type: python
      role: feature_engineering
      detected_concepts:
        - abs_amount
        - same_ts_count
        - z_score
        - account_zscore
    - path: fraud/detector.py
      type: python
      role: fraud_detector
      detected_concepts:
        - is_spike
        - is_velocity
        - is_anomaly
        - predicted_fraud
    - path: fraud/run_fraud.py
      type: python
      role: evaluation_runner
      detected_concepts:
        - precision
        - recall
        - f1
```

---

### 8.3 Entity model contract

File: `entities.yaml`

```yaml
entities:
  - name: Business Customer
    entity_id: business_customer
    grain: one row per business customer
    primary_key: customer_id
    source_tables:
      - customers
    business_definition: A commercial customer that holds or has held a business banking relationship.
    owner: Business Banking Data Owner
    sensitivity: confidential
    certification_status: draft
    attributes:
      - name: customer_id
        type: string
        role: primary_key
      - name: customer_name
        source_column: name
        type: string
        sensitivity: confidential
      - name: industry
        type: string
      - name: risk_rating
        type: string
        sensitivity: restricted
      - name: country
        type: string
      - name: customer_created_at
        source_column: created_at
        type: datetime

  - name: Business Account
    entity_id: business_account
    grain: one row per business account
    primary_key: account_id
    source_tables:
      - accounts
    business_definition: A business banking account owned by a business customer.
    owner: Business Banking Data Owner
    sensitivity: restricted
    certification_status: draft
    attributes:
      - name: account_id
        role: primary_key
      - name: customer_id
        role: foreign_key
      - name: account_type
      - name: balance
      - name: currency
      - name: opened_at

  - name: Transaction
    entity_id: transaction
    grain: one row per transaction event
    primary_key: txn_id
    source_tables:
      - transactions
    business_definition: A recorded credit or debit event against a business account.
    owner: Payments Data Owner
    sensitivity: restricted
    certification_status: candidate
```

---

### 8.4 Relationship contract

File: `relationships.yaml`

```yaml
relationships:
  - id: customer_owns_account
    from_entity: business_customer
    to_entity: business_account
    relationship_type: one_to_many
    join:
      from_column: customer_id
      to_column: customer_id
    mandatory: true

  - id: account_has_transaction
    from_entity: business_account
    to_entity: transaction
    relationship_type: one_to_many
    join:
      from_column: account_id
      to_column: account_id
    mandatory: true

  - id: transaction_produces_fraud_signal
    from_entity: transaction
    to_entity: fraud_signal
    relationship_type: one_to_many
    join:
      from_column: txn_id
      to_column: txn_id
    mandatory: false
```

---

### 8.5 Metric contract

File: `metrics.yaml`

```yaml
metrics:
  - metric_id: fraud_alert_count
    name: Fraud Alert Count
    definition: Count of transactions flagged as predicted fraud.
    type: count
    grain:
      - date
      - account
      - customer
      - merchant_category
    formula: count(txn_id) where predicted_fraud = true
    source_asset: certified_fraud_alert
    owner: Fraud Operations Owner
    certification_status: candidate
    approved_use:
      - fraud operations monitoring
      - analyst queue reporting

  - metric_id: detector_precision
    name: Detector Precision
    definition: Percentage of predicted fraud transactions that are confirmed fraud.
    type: ratio
    formula: true_positive / (true_positive + false_positive)
    source_asset: certified_fraud_detector_evaluation
    owner: Fraud Analytics Owner
    certification_status: candidate
    caveats:
      - Synthetic labels are not production-confirmed fraud outcomes.
```

---

### 8.6 Signal contract

File: `signals.yaml`

```yaml
signals:
  - signal_id: amount_spike_signal
    name: Amount Spike Signal
    entity: transaction
    definition: Indicates that the absolute transaction amount exceeds an approved suspicious amount threshold.
    logic:
      expression: abs_amount > spike_threshold
      default_thresholds:
        spike_threshold: 20000
    source_columns:
      - amount
      - abs_amount
    source_code:
      - fraud/detector.py::detect_fraud
    explainability: high
    approved_use:
      - fraud triage
      - alert explanation
    disallowed_use:
      - sole basis for adverse customer action
    certification_status: candidate

  - signal_id: velocity_burst_signal
    name: Velocity Burst Signal
    entity: transaction
    definition: Indicates that multiple transactions occurred for the same account at the same timestamp.
    logic:
      expression: same_ts_count >= same_ts_threshold
      default_thresholds:
        same_ts_threshold: 3
    source_columns:
      - account_id
      - timestamp
      - same_ts_count
    source_code:
      - fraud/features.py::build_features
      - fraud/detector.py::detect_fraud
    explainability: high
    certification_status: candidate

  - signal_id: account_level_burst_signal
    name: Account Level Burst Signal
    entity: business_account
    definition: Indicates that an account has previously exhibited burst transaction behaviour.
    logic:
      expression: account_had_burst = true
    source_code:
      - fraud/features.py::build_features
      - fraud/detector.py::detect_fraud_v4
    explainability: medium
    certification_status: experimental
    known_limitations:
      - Propagates the burst event to every transaction from the same account.
      - May significantly increase false positives.
      - Should be reviewed before operational use.
```

---

### 8.7 Data quality contract

File: `dq_rules.yaml`

```yaml
dq_rules:
  - rule_id: customer_id_not_null
    entity: business_customer
    asset: certified_business_customer
    rule_type: completeness
    severity: critical
    expression: customer_id IS NOT NULL
    blocking_for_certification: true

  - rule_id: customer_id_unique
    entity: business_customer
    asset: certified_business_customer
    rule_type: uniqueness
    severity: critical
    expression: customer_id IS UNIQUE
    blocking_for_certification: true

  - rule_id: account_customer_valid
    entity: business_account
    asset: certified_business_account
    rule_type: referential_integrity
    severity: critical
    expression: accounts.customer_id exists in customers.customer_id
    blocking_for_certification: true

  - rule_id: transaction_account_valid
    entity: transaction
    asset: certified_transaction
    rule_type: referential_integrity
    severity: critical
    expression: transactions.account_id exists in accounts.account_id
    blocking_for_certification: true

  - rule_id: fraud_flag_boolean
    entity: transaction
    asset: certified_transaction
    rule_type: validity
    severity: high
    expression: fraud_flag in (true, false)
    blocking_for_certification: true
```

---

### 8.8 Policy contract

File: `policies.yaml`

```yaml
policy_rules:
  - policy_id: fraud_human_review_required
    name: Fraud Human Review Required
    applies_to:
      - certified_fraud_alert
      - certified_transaction_fraud_signal
    rule: Fraud predictions must support analyst review and must not be used as fully automated adverse action.
    enforcement:
      - ai_response_guardrail
      - semantic_contract
    severity: critical
    blocking_for_certification: true

  - policy_id: restricted_transaction_access
    name: Restricted Transaction Access
    applies_to:
      - certified_transaction
      - certified_transaction_fraud_signal
      - certified_fraud_alert
    rule: Transaction-level data requires restricted access.
    enforcement:
      - rbac
      - row_column_security
    severity: critical
    blocking_for_certification: true

  - policy_id: explainability_required
    name: Alert Explainability Required
    applies_to:
      - certified_fraud_alert
    rule: Every fraud alert must expose contributing signal reasons.
    enforcement:
      - semantic_view_validation
      - ai_contract_validation
    severity: high
    blocking_for_certification: true
```

---

### 8.9 Semantic manifest contract

File: `semantic_manifest.yaml`

```yaml
semantic_package:
  package_id: business_banking_fraud_semantic_layer
  version: 0.1.0
  generated_by: Semantic_Foundry
  use_case_id: business_banking_fraud_detection
  status: candidate

assets:
  - asset_id: certified_business_customer
    type: entity_view
    file: semantic_views/certified_business_customer.sql
    entity: business_customer
    certification_status: draft

  - asset_id: certified_business_account
    type: entity_view
    file: semantic_views/certified_business_account.sql
    entity: business_account
    certification_status: draft

  - asset_id: certified_transaction
    type: entity_view
    file: semantic_views/certified_transaction.sql
    entity: transaction
    certification_status: candidate

  - asset_id: certified_transaction_fraud_signal
    type: signal_view
    file: semantic_views/certified_transaction_fraud_signal.sql
    entity: fraud_signal
    certification_status: candidate

  - asset_id: certified_fraud_alert
    type: alert_view
    file: semantic_views/certified_fraud_alert.sql
    entity: fraud_alert
    certification_status: candidate
```

---

### 8.10 AI context contract

File: `ai_context_cards.yaml`

```yaml
ai_context_cards:
  - asset: certified_fraud_alert
    business_description: Contains transactions flagged as suspicious based on candidate fraud signal rules.
    allowed_questions:
      - Which transactions were flagged as suspicious?
      - Why was this transaction flagged?
      - Which signals contributed to the alert?
      - What is the alert volume by day, account, customer, or merchant category?
    disallowed_questions:
      - Should this customer be exited automatically?
      - Should this transaction be blocked without review?
      - Is this customer definitely committing fraud?
    required_caveats:
      - Fraud alerts are indicators, not final determinations.
      - Human review is required.
      - Synthetic fraud labels are not production-confirmed fraud outcomes.
    safe_join_paths:
      - certified_fraud_alert.account_id -> certified_business_account.account_id
      - certified_business_account.customer_id -> certified_business_customer.customer_id
    sensitive_fields:
      - customer_name
      - account_id
      - txn_id
    default_response_style: explain evidence and limitations
```

---

## 9. Detailed Pipeline Flow

### Step 1: Intake loading

Inputs:

```text
use_case.yaml
source path
optional platform target
optional governance configuration
```

Outputs:

```text
normalised use case object
scope object
risk classification
initial semantic asset targets
```

Deterministic checks:

```text
use_case.id exists
business_objective exists
risk_level is valid
automation_level is valid
business_questions are present
```

---

### Step 2: Source inventory

Scans source folder and classifies files:

```text
.py → Python logic miner
.sql → SQL miner
.yml/.yaml → config miner
.ipynb → notebook miner
.csv/.parquet → table profiler
.json → metadata/schema miner
```

For the fraud archive, expected classification:

```text
datasets/generator_v3.py → data generator
datasets/schema.py → schema validation
datasets/validator.py → DQ validation
fraud/features.py → feature engineering
fraud/detector.py → rule detector and ML baseline
fraud/load.py → data join and enrichment
fraud/run_fraud.py → evaluation runner
```

---

### Step 3: Data profiling

Profiles physical datasets or inferred schemas.

Generated findings:

```text
customers:
- grain: one row per customer
- key: customer_id
- candidate dimensions: industry, risk_rating, country

accounts:
- grain: one row per account
- key: account_id
- foreign key: customer_id
- candidate measure: balance

transactions:
- grain: one row per transaction
- key: txn_id
- foreign key: account_id
- event time: timestamp
- candidate measure: amount
- label: fraud_flag
```

---

### Step 4: Logic mining

Parses Python AST and comments/docstrings where possible.

Extracted from `fraud/features.py`:

```text
abs_amount = amount.abs()
txn_count = count(txn_id) over account_id
same_ts_count = count(txn_id) over account_id, timestamp
z_score = (abs_amount - global_mean) / global_std
account_zscore = (abs_amount - account_mean) / account_std
is_burst = same_ts_count >= 3
account_had_burst = account_id in burst_accounts
```

Extracted from `fraud/detector.py`:

```text
DEFAULTS:
- spike_threshold = 20000
- same_ts_threshold = 3
- zscore_threshold = 3.0

detect_fraud:
- is_spike = abs_amount > spike_threshold
- is_velocity = same_ts_count >= same_ts_threshold
- is_anomaly = abs(z_score) > zscore_threshold
- predicted_fraud = is_spike OR is_velocity OR is_anomaly

detect_fraud_v3:
- fraud_score = 0.4 * is_spike + 0.4 * is_velocity + 0.2 * is_anomaly
- predicted_fraud = fraud_score > 0.5

detect_fraud_v4:
- includes account_had_burst as is_account_burst

detect_fraud_v5:
- includes same-account-same-day temporal burst signal

detect_fraud_ml:
- logistic regression trained with abs_amount, same_ts_count, z_score, account_zscore, merchant_category_enc, risk_rating_enc
```

---

### Step 5: Concept extraction

LLM takes structured scanner output and proposes business concepts.

Examples:

| Technical artefact | Business concept |
|---|---|
| abs_amount | Transaction Absolute Amount |
| same_ts_count | Same Timestamp Transaction Count |
| z_score | Global Amount Anomaly Score |
| account_zscore | Account-Normalised Amount Anomaly Score |
| is_spike | Amount Spike Signal |
| is_velocity | Velocity Burst Signal |
| is_anomaly | Statistical Amount Anomaly Signal |
| predicted_fraud | Predicted Fraud Indicator |
| fraud_score | Fraud Risk Score |
| precision | Detector Precision |
| recall | Detector Recall |
| f1 | Detector F1 Score |

---

### Step 6: Entity, metric, and signal generation

Generates semantic models from extracted concepts.

Output groups:

```text
Entities:
- Business Customer
- Business Account
- Transaction
- Fraud Signal
- Fraud Alert
- Fraud Evaluation

Metrics:
- Fraud Alert Count
- Confirmed Fraud Rate
- Detector Precision
- Detector Recall
- Detector F1 Score
- Fraud Loss Exposure

Signals:
- Amount Spike Signal
- Velocity Burst Signal
- Statistical Amount Anomaly Signal
- Account-Level Burst Signal
- Temporal Burst Signal
```

---

### Step 7: Governance generation

Creates governance metadata:

```text
ownership suggestions
sensitivity classification
known limitations
approved/disallowed uses
certification status
required approvals
blocking issues
```

Fraud-specific governance decisions:

```text
- Transaction-level data is restricted.
- Fraud predictions require human review.
- Synthetic labels are not production-confirmed outcomes.
- Thresholds require Fraud Risk Owner approval.
- Account-level burst signal should remain experimental until false positive impact is reviewed.
- AI copilot must not state that a customer is definitely committing fraud.
```

---

### Step 8: Semantic SQL generation

MVP SQL targets generic ANSI-ish SQL. Platform-specific adapters can be added later.

#### `certified_business_customer.sql`

```sql
CREATE OR REPLACE VIEW certified_business_customer AS
SELECT
    customer_id,
    name AS customer_name,
    industry,
    risk_rating,
    country,
    created_at AS customer_created_at
FROM customers;
```

#### `certified_business_account.sql`

```sql
CREATE OR REPLACE VIEW certified_business_account AS
SELECT
    account_id,
    customer_id,
    account_type,
    balance,
    currency,
    opened_at
FROM accounts;
```

#### `certified_transaction.sql`

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
    fraud_flag
FROM transactions;
```

#### `certified_transaction_fraud_signal.sql`

```sql
CREATE OR REPLACE VIEW certified_transaction_fraud_signal AS
WITH base AS (
    SELECT
        t.*,
        ABS(t.amount) AS abs_amount,
        COUNT(*) OVER (PARTITION BY t.account_id) AS txn_count,
        COUNT(*) OVER (PARTITION BY t.account_id, t.timestamp) AS same_ts_count
    FROM transactions t
), scored AS (
    SELECT
        base.*,
        (abs_amount - AVG(abs_amount) OVER ())
            / NULLIF(STDDEV(abs_amount) OVER (), 0) AS z_score,
        (abs_amount - AVG(abs_amount) OVER (PARTITION BY account_id))
            / NULLIF(STDDEV(abs_amount) OVER (PARTITION BY account_id), 0) AS account_zscore
    FROM base
)
SELECT
    txn_id,
    account_id,
    amount,
    abs_amount,
    txn_type,
    merchant_category,
    timestamp,
    fraud_flag,
    txn_count,
    same_ts_count,
    z_score,
    account_zscore,
    CASE WHEN abs_amount > 20000 THEN TRUE ELSE FALSE END AS is_amount_spike,
    CASE WHEN same_ts_count >= 3 THEN TRUE ELSE FALSE END AS is_velocity_burst,
    CASE WHEN ABS(z_score) > 3.0 THEN TRUE ELSE FALSE END AS is_statistical_anomaly,
    CASE
        WHEN abs_amount > 20000
          OR same_ts_count >= 3
          OR ABS(z_score) > 3.0
        THEN TRUE ELSE FALSE
    END AS predicted_fraud
FROM scored;
```

#### `certified_fraud_alert.sql`

```sql
CREATE OR REPLACE VIEW certified_fraud_alert AS
SELECT
    txn_id,
    account_id,
    predicted_fraud,
    fraud_flag,
    is_amount_spike,
    is_velocity_burst,
    is_statistical_anomaly,
    CASE
        WHEN is_velocity_burst THEN 'Velocity burst'
        WHEN is_amount_spike THEN 'Amount spike'
        WHEN is_statistical_anomaly THEN 'Statistical anomaly'
        ELSE 'No alert'
    END AS primary_alert_reason
FROM certified_transaction_fraud_signal
WHERE predicted_fraud = TRUE;
```

---

### Step 9: Validation

Validation runs before any certification.

Validation categories:

```text
Artefact schema validation:
- YAML files conform to required schema.
- Required fields are populated.

Semantic validation:
- Every entity has grain and owner.
- Every metric has formula and grain.
- Every signal has logic and approved use.
- Every semantic asset has sensitivity and certification status.

DQ validation:
- Primary keys are not null.
- Primary keys are unique.
- Foreign keys resolve.
- Valid value checks pass.

SQL validation:
- SQL parses.
- Referenced columns exist.
- Referenced views exist.
- No raw sensitive table exposed directly to AI contract.

Policy validation:
- Restricted assets have access rules.
- High-risk use cases have human-review policy.
- AI context cards include disallowed questions.
```

---

### Step 10: Certification

Certification lifecycle:

```text
Draft
  ↓
Candidate
  ↓
Business Reviewed
  ↓
DQ Validated
  ↓
Policy Approved
  ↓
Certified
  ↓
Deprecated / Retired
```

Certification gate example:

```yaml
certification_gate:
  asset: certified_transaction_fraud_signal
  required:
    business_definition_approved: true
    owner_assigned: true
    dq_rules_passed: true
    sensitivity_classified: true
    policy_rules_defined: true
    ai_context_card_created: true
    lineage_documented: true
    threshold_approved: true
  blockers:
    - synthetic labels are not production-confirmed fraud outcomes
    - thresholds have not been approved by Fraud Risk Owner
  result: candidate_not_certified
```

---

## 10. Human Review Workflow

### Review roles

| Role | Responsibility |
|---|---|
| Business Owner | Approves definitions and business usage |
| Data Owner | Approves data source and ownership |
| Data Steward | Reviews glossary and DQ rules |
| Risk Owner | Approves high-risk policy constraints |
| Technical Owner | Approves implementation and lineage |
| AI Product Owner | Approves AI consumption contract |

### Review UI / report sections

```text
1. Use case summary
2. Candidate semantic assets
3. Glossary terms requiring approval
4. Entity model requiring approval
5. Metrics and signals requiring approval
6. Data quality results
7. Policy restrictions
8. Known limitations
9. AI allowed/disallowed questions
10. Certification recommendation
```

---

## 11. AI Copilot Consumption Pattern

Once semantic assets are created, an AI copilot can use them safely.

```text
User question
    ↓
Intent classification
    ↓
Retrieve AI context cards
    ↓
Check allowed/disallowed question policy
    ↓
Identify certified semantic assets
    ↓
Generate SQL only against certified semantic views
    ↓
Execute query
    ↓
Validate result shape
    ↓
Generate answer with caveats and lineage
    ↓
Audit question, assets used, answer, and policy result
```

Example safe answer pattern:

```text
This transaction was flagged because it triggered the Velocity Burst Signal.
That means multiple transactions occurred for the same account at the same timestamp.
This is an indicator for analyst review, not a final fraud determination.
```

Example refusal pattern:

```text
I cannot determine that this customer is definitely committing fraud. The available semantic asset only supports suspicious activity triage and requires human review.
```

---

## 12. MVP Implementation Plan

### Phase 1: Static semantic package generator

Goal: generate artefacts from the fraud source folder.

Build:

```text
- CLI skeleton
- source inventory scanner
- simple Python AST miner
- hardcoded fraud use case config
- YAML artefact generation
- Markdown certification report
```

Output:

```text
outputs/business_banking_fraud/
├── glossary.yaml
├── entities.yaml
├── relationships.yaml
├── metrics.yaml
├── signals.yaml
├── dq_rules.yaml
├── policies.yaml
├── semantic_manifest.yaml
├── semantic_views.sql
├── ai_context_cards.yaml
└── certification_report.md
```

Success criteria:

```text
- Can run from CLI.
- Generates consistent package.
- Artefacts pass YAML validation.
- Report identifies at least 5 concepts, 3 entities, 3 signals, and 3 DQ rules.
```

---

### Phase 2: Deterministic validators

Build:

```text
- YAML schema validator
- source schema validator
- DQ validator for Pandas/DuckDB
- SQL parser or dry-run validator
- certification gate validator
```

Success criteria:

```text
- Fails package when required owners are missing.
- Fails package when critical DQ rules fail.
- Flags experimental signals.
- Produces blocking issue register.
```

---

### Phase 3: LLM-assisted generation

Build:

```text
- LLM prompt templates
- structured output schemas
- concept extraction prompt
- glossary generation prompt
- policy classification prompt
- AI context card prompt
```

Success criteria:

```text
- LLM output is validated before being accepted.
- Invalid JSON/YAML is rejected.
- Hallucinated source columns are rejected by deterministic validator.
- Generated definitions include source references and confidence.
```

---

### Phase 4: Review cockpit

Build Streamlit or lightweight web UI:

```text
- view generated artefacts
- approve/reject glossary terms
- approve/reject signals
- edit owners and certification status
- see DQ results
- publish package
```

Success criteria:

```text
- Reviewer can promote an asset from draft to candidate.
- Reviewer can record blocking issues.
- Certification report updates after review.
```

---

### Phase 5: Platform adapters

Add generation targets:

```text
- Generic SQL
- dbt models
- Snowflake views and tags
- Databricks Unity Catalog views and tags
- Power BI semantic model draft
```

Success criteria:

```text
- Same semantic manifest can generate multiple platform outputs.
- Platform-specific output remains traceable to the same semantic asset ID.
```

---

## 13. Testing Strategy

### Unit tests

```text
- test source inventory classification
- test Python AST extraction for feature logic
- test YAML schema validation
- test DQ rule expression generation
- test policy gate validation
- test certification state transitions
```

### Integration tests

```text
- run full build on business banking fraud fixture
- validate expected artefact files are created
- validate semantic views contain expected columns
- validate issue register flags synthetic-label caveat
- validate account_level_burst_signal remains experimental
```

### Golden output tests

Maintain expected output snapshots:

```text
examples/business_banking_fraud/expected_output/
├── glossary.yaml
├── entities.yaml
├── signals.yaml
└── certification_report.md
```

Use them to detect drift in generation quality.

---

## 14. Governance and Audit Design

Every run should produce a run manifest:

```yaml
run:
  run_id: 2026-05-02T011500Z_business_banking_fraud
  semantic_foundry_version: 0.1.0
  source_hash: abc123
  use_case_hash: def456
  llm_model: optional
  generation_mode: build
  generated_assets:
    - glossary.yaml
    - entities.yaml
    - signals.yaml
    - semantic_views.sql
  validation_status: failed_policy_gate
  certification_status: candidate
```

Every generated artefact should include:

```text
source references
generation timestamp
confidence
review status
owner
certification status
```

This is essential for enterprise consulting credibility.

---

## 15. Example Certification Report Outline

```markdown
# Semantic_Foundry Certification Report

## Use Case
Business Banking Fraud Detection

## Generated Semantic Assets
- certified_business_customer
- certified_business_account
- certified_transaction
- certified_transaction_fraud_signal
- certified_fraud_alert

## Certification Summary
| Asset | Status | Reason |
|---|---|---|
| certified_business_customer | Draft | Business owner required |
| certified_transaction | Candidate | DQ rules generated, pending approval |
| certified_transaction_fraud_signal | Candidate | Thresholds require approval |
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
```

---

## 16. Consulting Delivery Playbook

### Discovery workshop

Questions:

```text
What decision is the use case supporting?
Who makes the decision?
What data is used today?
What definitions are disputed?
What reports or models already exist?
What are the known data quality problems?
What would make an AI answer unsafe?
Who can approve a business definition?
```

### Build workshop

Outputs:

```text
Draft glossary
Domain concept model
Entity relationship model
Metric and signal catalogue
DQ and policy control list
Semantic asset backlog
```

### Certification workshop

Outputs:

```text
Approved/rejected glossary terms
Approved/rejected metrics and signals
Owner assignments
Certification status
Blocking issue register
Scale-out roadmap
```

---

## 17. Extension Patterns

### Pattern A: Fraud Investigation Copilot

Uses:

```text
certified_fraud_alert
certified_transaction_fraud_signal
certified_business_account
certified_business_customer
ai_context_cards
```

Capabilities:

```text
- explain why a transaction was flagged
- summarise account behaviour
- show contributing signals
- compare alert to account baseline
- generate analyst investigation notes
```

### Pattern B: Signal Discovery Engine

Uses:

```text
certified_transaction
certified_transaction_fraud_signal
signal_catalogue
metrics_catalogue
fraud_evaluation
```

Capabilities:

```text
- propose new signals
- compare signal precision/recall impact
- promote useful signals
- deprecate weak signals
```

### Pattern C: Governance Copilot

Uses:

```text
glossary.yaml
semantic_manifest.yaml
dq_rules.yaml
policies.yaml
lineage.yaml
certification_report.md
```

Capabilities:

```text
- identify uncertified assets
- explain why an asset is blocked
- generate governance review questions
- summarise DQ failures
```

---

## 18. Roadmap

### Version 0.1

```text
- CLI
- fraud example support
- static YAML generation
- generic SQL views
- certification report
```

### Version 0.2

```text
- deterministic validators
- run manifest
- issue register
- better Python AST mining
```

### Version 0.3

```text
- LLM structured generation
- prompt templates
- human review report
- AI context card generation
```

### Version 0.4

```text
- Streamlit review cockpit
- approval workflow
- certification state machine
```

### Version 0.5

```text
- Snowflake adapter
- dbt adapter
- Databricks adapter
- semantic package versioning
```

---

## 19. Product Positioning

**Semantic_Foundry turns messy enterprise data and hidden analytical logic into governed, certified, AI-ready business meaning.**

For consulting agencies:

```text
Without Semantic_Foundry:
- each semantic layer engagement starts from scratch
- business definitions are manually discovered
- code logic remains hidden in notebooks and scripts
- AI readiness is treated as an afterthought

With Semantic_Foundry:
- discovery is accelerated
- semantic assets are generated consistently
- governance is embedded from the start
- AI consumption contracts are produced as first-class deliverables
```

---

## 20. Immediate Build Recommendation

Start with the business banking fraud fixture because it has the right ingredients:

```text
- entities: customers, accounts, transactions
- business objective: suspicious transaction detection
- feature engineering logic
- rule-based detector logic
- ML baseline logic
- validation logic
- evaluation metrics
- clear AI safety constraints
```

The first implementation should generate a semantic package from this fixture. Once that works, generalise the pipeline to accept new use cases.
