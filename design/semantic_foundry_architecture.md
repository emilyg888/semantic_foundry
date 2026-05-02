# Trusted Semantic Foundation Framework

A reusable consulting accelerator for building an **Enterprise Semantic Layer** that helps enterprise clients make their data **AI-ready**.

This framework is intended for clients whose data is already loaded into a data warehouse, lakehouse, or data lake environment, but where:

- Logical data models may be incomplete or inconsistent
- Data quality may be poor
- Governance maturity may be low
- Business definitions may vary across teams
- AI initiatives need trusted, governed, explainable data foundations

---

## 1. Core Idea

The semantic layer is not just a BI convenience layer.

For enterprise AI, it becomes the **trusted interpretation layer** between messy enterprise data and AI/analytics consumers.

```text
Raw / Integrated Data
        ↓
Data Quality + Lineage + Governance Controls
        ↓
Certified Business Concepts
        ↓
Enterprise Semantic Layer
        ↓
BI, Analytics, ML Features, RAG, AI Copilots, Agents
```

The framework helps clients answer:

> When an AI system answers a question using enterprise data, what certified business meaning, metric definition, access rule, data quality status, and lineage is it relying on?

That is the real purpose.

---

## 2. Reference Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                    Enterprise AI Consumers                    │
│                                                              │
│  BI Dashboards │ Analyst SQL │ ML Features │ RAG │ Copilots │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌──────────────────────────────────────────────────────────────┐
│                  Enterprise Semantic Layer                    │
│                                                              │
│  Business Entities  │ Metrics │ Dimensions │ Relationships   │
│  Glossary Terms     │ Rules   │ Policies   │ Certified Views │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌──────────────────────────────────────────────────────────────┐
│              Governance + AI Readiness Control Layer          │
│                                                              │
│  Data Quality │ Lineage │ Ownership │ Classification │ RBAC  │
│  Certification │ Usage Policy │ Auditability │ Evaluation     │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌──────────────────────────────────────────────────────────────┐
│                Existing Data Platform Foundation              │
│                                                              │
│  Warehouse │ Lakehouse │ Lake │ Marts │ APIs │ Data Products │
└──────────────────────────────────────────────────────────────┘
```

The key principle:

> The AI layer should not reason directly over raw enterprise tables. It should reason over **certified business concepts and governed semantic assets**.

---

## 3. Framework Layers

---

### Layer 1: Domain Discovery Layer

Purpose: understand what the business actually means.

Typical artefacts:

| Artefact | Purpose |
|---|---|
| Domain map | Major business domains, subdomains, data products |
| Business capability map | Links data to business outcomes |
| Critical use cases | AI, analytics, regulatory, operational priorities |
| Stakeholder map | Business owner, data owner, steward, risk owner |
| Concept inventory | Customer, product, policy, claim, transaction, account, employee, asset, etc. |

Example:

```text
Insurance Domain
├── Customer
├── Policy
├── Premium
├── Claim
├── Provider
├── Payment
├── Risk Event
└── Recovery / Outcome
```

This phase prevents the semantic layer from becoming a technical table-renaming exercise.

---

### Layer 2: Business Glossary Layer

Purpose: define enterprise meaning before defining metrics.

Each business term should have:

| Field | Example |
|---|---|
| Business term | Active Customer |
| Definition | A customer with at least one active product relationship |
| Domain | Customer |
| Owner | Head of Customer Analytics |
| Calculation logic | Derived from product status and relationship dates |
| Synonyms | Current customer, live customer |
| Exclusions | Prospects, former customers |
| Certification status | Draft / Reviewed / Certified |
| Sensitive classification | Internal / Confidential / Restricted |

For AI readiness, glossary terms should be machine-usable, not just human-readable.

Each term should link to:

```text
Business Term
   ↓
Data Element
   ↓
Transformation Logic
   ↓
Certified Semantic View
   ↓
Policy / Access Rule
   ↓
Lineage
```

---

### Layer 3: Logical Business Entity Layer

Purpose: create a coherent business model even if the client does not already have one.

This does not need to be a full enterprise data model. It can be a pragmatic **semantic entity model**.

```text
Customer ── owns ── Account ── has ── Transaction
   │                       │
   │                       └── linked to ── Product
   │
   └── raises ── Case / Claim / Request
```

Each entity should include:

| Component | Description |
|---|---|
| Entity definition | What the entity means |
| Natural keys | Business identifiers |
| System keys | Source/platform identifiers |
| Golden record rule | How duplicates are resolved |
| Relationship rules | Valid relationships to other entities |
| Temporal rules | Effective dates, active/inactive logic |
| Data quality rules | Completeness, uniqueness, validity |
| Sensitivity | PII, financial, health, restricted, etc. |

This is where the framework helps immature clients build a minimum viable logical model.

---

### Layer 4: Metric and KPI Layer

Purpose: make enterprise metrics consistent, explainable, and AI-safe.

A metric definition should include:

| Field | Example |
|---|---|
| Metric name | Net Revenue |
| Business definition | Revenue after discounts, refunds, and adjustments |
| Grain | Customer-month |
| Formula | Gross revenue - refunds - discounts |
| Filters | Exclude test accounts |
| Time logic | Recognised on transaction settlement date |
| Owner | Finance |
| Approved use | Executive reporting, forecasting |
| Restricted use | Not approved for regulatory reporting until certified |
| Certification status | Certified |

Metric design pattern:

```text
Metric = Measure + Grain + Filter + Time Logic + Policy + Owner
```

This is critical for AI because without metric certification, AI copilots will confidently answer using inconsistent definitions.

---

### Layer 5: Semantic View Layer

Purpose: expose governed, reusable, business-aligned data structures.

This may be implemented as:

| Platform | Possible Implementation |
|---|---|
| Snowflake | Secure views, dynamic tables, Cortex Search, semantic views |
| Databricks | Unity Catalog, Delta tables, views, metric views |
| dbt | dbt semantic layer, metrics, exposures |
| Power BI | Shared semantic models |
| Looker | LookML explores and governed metrics |
| AtScale / Cube | Dedicated semantic layer |
| Custom | YAML-driven semantic model + generated SQL views |

The accelerator should avoid being tool-specific.

Recommended abstraction:

```text
Semantic Asset
├── Entity View
├── Metric View
├── Dimension View
├── Relationship View
├── Policy Rule
├── Quality Rule
├── Lineage Mapping
└── Certification Status
```

Example assets:

```text
certified_customer
certified_account
certified_transaction
certified_customer_value_metrics
certified_claim_outcome_metrics
```

---

### Layer 6: Governance Control Layer

Purpose: ensure the semantic layer is trusted.

Minimum controls:

| Control | Why It Matters |
|---|---|
| Ownership | Every semantic asset has a business and technical owner |
| Certification | Users know what is approved vs experimental |
| Data quality scoring | AI can avoid low-trust data |
| Lineage | Answers can be traced back |
| Access policy | Sensitive data is protected |
| Change control | Metric definitions do not drift silently |
| Audit logging | AI/data usage can be reviewed |
| Issue management | Data problems have remediation workflows |

Certification model:

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

This gives consultants a repeatable maturity path.

---

### Layer 7: AI Consumption Layer

Purpose: make the semantic layer usable by AI systems.

AI systems need more than SQL tables. They need structured context.

For each semantic asset, provide:

| AI-Ready Metadata | Example |
|---|---|
| Business description | Represents a certified active customer view |
| Allowed questions | Customer segmentation, retention, churn analysis |
| Disallowed questions | Individual credit decisions |
| Join rules | Customer joins to account via customer_id |
| Metric definitions | Revenue, churn, lifetime value |
| Quality status | Certified, 98% completeness |
| Sensitivity | Contains restricted PII |
| Prompt-safe summary | Text description for retrieval |
| SQL-safe contract | Approved query patterns |

AI consumption pattern:

```text
User Question
    ↓
Intent Classification
    ↓
Semantic Asset Retrieval
    ↓
Policy Check
    ↓
Certified SQL / Retrieval Plan
    ↓
Data Query
    ↓
Result Validation
    ↓
LLM Explanation
```

Key principle:

> The LLM should explain and reason over governed outputs. It should not invent joins, definitions, or metric logic.

---

## 4. Reusable Delivery Methodology

---

### Phase 0: Engagement Setup

Goal: define scope and success criteria.

Key questions:

| Question | Why It Matters |
|---|---|
| What business domain is in scope? | Avoid enterprise-wide paralysis |
| What are the top AI/analytics use cases? | Prioritise semantic assets |
| What data platforms exist? | Understand implementation options |
| What governance artefacts already exist? | Reuse before rebuilding |
| Who owns the definitions? | Avoid technical-only design |

Deliverables:

```text
Engagement charter
Scope domain map
Use case backlog
Stakeholder map
Semantic layer target state
```

---

### Phase 1: Current-State Assessment

Assess across five dimensions:

```text
Data Model Maturity
Data Quality Maturity
Governance Maturity
Metadata / Lineage Maturity
AI Readiness Maturity
```

Example scoring:

| Area | Low Maturity | High Maturity |
|---|---|---|
| Logical model | Table-driven, inconsistent | Domain entities defined |
| Glossary | Ad hoc terms | Owned, governed definitions |
| Metrics | Report-specific | Enterprise-certified |
| Data quality | Reactive fixes | Monitored controls |
| Lineage | Tribal knowledge | Automated lineage |
| AI readiness | Raw tables exposed | Certified semantic contracts |

Deliverables:

```text
Current-state assessment
Data/metadata inventory
Pain point heatmap
AI readiness maturity score
Priority domain recommendation
```

---

### Phase 2: Semantic Domain Blueprint

Goal: design the business semantic model for one priority domain.

Deliverables:

```text
Domain concept model
Business glossary
Core entities
Metric catalogue
Relationship map
Policy classification
Critical data elements
```

Example blueprint:

```text
Customer Domain
├── Entity: Customer
├── Entity: Account
├── Entity: Product Holding
├── Entity: Interaction
├── Metric: Active Customers
├── Metric: Customer Lifetime Value
├── Metric: Churn Rate
├── Metric: Product Penetration
└── Policy: PII access restrictions
```

This becomes the reusable pattern for the next domain.

---

### Phase 3: Data-to-Semantic Mapping

Goal: connect messy physical data to business meaning.

Mapping template:

| Business Concept | Physical Source | Transformation | Rule | Owner | Status |
|---|---|---|---|---|---|
| Active Customer | CRM.CUST, CORE.ACCOUNT | Join + status filter | Active if open product exists | Customer Data Owner | Candidate |
| Net Revenue | FIN.TXN | Aggregate less refunds | Exclude reversals | Finance Owner | Certified |

Deliverables:

```text
Source-to-semantic mapping
Transformation rules
Join rules
DQ rules
Lineage map
Exception register
```

This is usually where data quality issues become visible.

---

### Phase 4: Build Certified Semantic Assets

Goal: implement reusable governed assets.

Typical assets:

```text
certified_customer_view
certified_product_view
certified_transaction_view
certified_customer_metrics
certified_revenue_metrics
certified_risk_signals
```

Each asset should be packaged with metadata:

```yaml
semantic_asset: certified_customer
domain: customer
owner: customer_data_owner
certification_status: certified
sensitivity: restricted
approved_use_cases:
  - customer analytics
  - retention modelling
  - service personalisation
disallowed_use_cases:
  - automated credit decisioning
quality_score: 0.96
lineage:
  - crm.customer
  - core.account
```

The framework should include reusable YAML/JSON templates like this.

---

### Phase 5: Governance and Certification

Goal: move from technically built to enterprise trusted.

Certification checklist:

| Check | Required? |
|---|---|
| Business definition approved | Yes |
| Data owner assigned | Yes |
| Technical owner assigned | Yes |
| DQ rules implemented | Yes |
| Lineage documented | Yes |
| Access policy applied | Yes |
| Metric logic reviewed | Yes |
| AI usage policy defined | Yes |
| Test queries passed | Yes |
| Change process agreed | Yes |

Useful certification gate:

```text
Can this semantic asset be safely used by:
1. A dashboard?
2. A business analyst?
3. A machine learning feature pipeline?
4. An AI copilot?
5. An autonomous or semi-autonomous agent?
```

If the answer is no for AI, document why.

---

### Phase 6: AI Enablement

Goal: expose semantic assets to AI safely.

Reusable AI patterns:

| Pattern | Description |
|---|---|
| Semantic RAG | Retrieve business definitions, policies, metric logic |
| Governed Text-to-SQL | Generate SQL only against certified views |
| AI Analyst Copilot | Answer business questions with approved definitions |
| Data Quality Copilot | Explain failed DQ checks and lineage impact |
| Metric Explainer | Explain KPI movements using certified metrics |
| Signal Discovery | Identify candidate patterns from governed features |

Recommended architecture:

```text
Question
  ↓
Semantic Retrieval
  ↓
Policy Enforcement
  ↓
Certified Query Generation
  ↓
Execution Against Governed Views
  ↓
Result Validation
  ↓
LLM Explanation
  ↓
Audit Log
```

This is the bridge from semantic layer to enterprise AI.

---

## 5. Accelerator Assets the Consulting Agency Should Build

The agency should package this as a repeatable consulting kit.

### A. Assessment Assets

```text
AI readiness questionnaire
Semantic maturity model
Data governance maturity checklist
Metadata maturity checklist
Use case prioritisation matrix
Domain complexity scoring model
```

### B. Design Assets

```text
Domain model template
Business glossary template
Metric catalogue template
Semantic entity template
Data-to-semantic mapping template
DQ rule catalogue
Policy classification template
Lineage template
```

### C. Build Assets

```text
Reusable semantic YAML schema
SQL view generation patterns
dbt model templates
Snowflake semantic view patterns
Databricks Unity Catalog patterns
Power BI semantic model standards
LookML / Cube / AtScale mapping patterns
```

### D. Governance Assets

```text
Certification workflow
RACI model
Change control process
Semantic asset lifecycle
AI usage approval checklist
Data product ownership model
DQ issue triage workflow
```

### E. AI Enablement Assets

```text
Prompt templates for semantic retrieval
Text-to-SQL guardrails
Certified-only retrieval rules
Policy enforcement patterns
AI answer audit schema
Evaluation test set template
Refusal patterns for unsafe questions
```

---

## 6. Maturity Model

A simple maturity model makes this easier to sell and deliver.

| Level | Description | Typical Client State |
|---|---|---|
| Level 1: Fragmented | Data exists, definitions inconsistent | Reports disagree, AI unsafe |
| Level 2: Documented | Some glossary and metrics exist | Useful but not enforceable |
| Level 3: Governed | Owners, DQ, lineage, access controls exist | BI-ready |
| Level 4: Certified Semantic | Reusable certified entities and metrics | Analytics/ML-ready |
| Level 5: AI-Ready Semantic | AI systems consume governed semantic contracts | Copilot/agent-ready |

The target for most first engagements should be:

> Move one priority domain from Level 1/2 to Level 4, with a clear path to Level 5.

Do not try to boil the ocean.

---

## 7. Suggested Engagement Model

### 6–8 Week Accelerator

```text
Week 1: Discovery + maturity assessment
Week 2: Use case prioritisation + domain selection
Week 3: Business glossary + entity model
Week 4: Metric catalogue + source mapping
Week 5: Build certified semantic assets
Week 6: Governance certification + DQ controls
Week 7: AI enablement pattern
Week 8: Roadmap + operating model
```

### Output

```text
1 priority domain semantic blueprint
5–10 certified business entities/metrics
Governance certification workflow
AI-ready semantic metadata pack
Reference implementation pattern
Scale-out roadmap
```

This gives the client a tangible pilot and gives the consulting agency a repeatable delivery motion.

---

## 8. Key Design Principles

### Principle 1: Start with business concepts, not tables

Bad pattern:

```text
Expose warehouse tables to AI
```

Better pattern:

```text
Expose certified business concepts to AI
```

---

### Principle 2: Separate definition from implementation

A metric should exist as a business definition before it exists as SQL.

```text
Business Definition
   ↓
Metric Contract
   ↓
SQL / dbt / Semantic Model Implementation
   ↓
Certified Consumption
```

---

### Principle 3: Make governance executable

Governance cannot stay in PDFs and spreadsheets.

It needs to become:

```text
Rules
Policies
Metadata
Quality checks
Access controls
Certification gates
```

---

### Principle 4: Treat AI as a Consumer of Governed Data Products

AI is not special. It is another consumer, but a higher-risk one.

So the semantic layer needs to provide:

```text
Meaning
Context
Boundaries
Lineage
Quality
Permission
```

---

### Principle 5: Certified-Only for Enterprise AI

A strong default rule:

> AI copilots and agents can only answer from certified semantic assets unless explicitly operating in an exploratory mode.

That gives the client a practical safety boundary.

---

## 9. Minimum Viable Semantic Layer

For a first client engagement, do not attempt the full enterprise model.

Build a minimum viable semantic layer for one high-value domain.

Minimum viable scope:

```text
One business domain
3–5 core entities
5–10 certified metrics
Critical data elements
Data quality checks
Ownership model
Lineage mapping
Access policy
AI-ready metadata
One AI/analytics use case demonstration
```

Example:

```text
Domain: Customer
Entities:
- Customer
- Account
- Product Holding
- Interaction
- Transaction

Metrics:
- Active customers
- Customer churn rate
- Average product holding
- Customer lifetime value
- Monthly transaction value

AI use case:
- Customer analytics copilot using certified semantic views only
```

---

## 10. Consulting Agency Proposition

The agency can position the accelerator like this:

> We help enterprises move from fragmented warehouse data to an AI-ready semantic layer by creating certified business concepts, governed metrics, executable data quality controls, and AI-safe semantic contracts.

Sharper version:

> We do not start by building the chatbot.  
> We build the trusted semantic foundation that lets AI answer safely.

The reusable framework should combine:

```text
Methodology
Templates
Reference architecture
Governance model
Implementation patterns
AI consumption patterns
Maturity assessment
Reusable accelerators
```

That is what makes it an engagement accelerator rather than a one-off consulting exercise.

---

## 11. Recommended Framework Name

Recommended name:

## Trusted Semantic Foundation Framework

Why this works:

- It speaks to both business and technology audiences
- It avoids being tool-specific
- It positions the semantic layer as the foundation for enterprise AI
- It aligns with governance, certification, business meaning, and AI readiness

Alternative names:

1. AI-Ready Semantic Layer Accelerator
2. Enterprise Semantic Readiness Framework
3. Semantic-to-AI Accelerator
4. Governed Semantic Layer Blueprint
5. Trusted Business Meaning Layer
6. Certified Semantic Data Product Framework

---

## 12. Summary

The **Trusted Semantic Foundation Framework** provides a reusable way for consulting teams to help clients move from fragmented, low-governance data estates toward AI-ready enterprise data foundations.

It combines:

- Business glossary
- Domain model
- Entity model
- Metric catalogue
- Certified semantic views
- Data quality controls
- Lineage
- Access policy
- AI-ready metadata
- Governance certification
- AI consumption patterns

The most important shift is this:

> Enterprise AI should not consume raw data directly. It should consume certified business meaning through governed semantic contracts.
