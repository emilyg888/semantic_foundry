# Architecture

## 1. Purpose

Semantic_Foundry is a reusable consulting accelerator for building a governed semantic package from a business use case, source code, and sample data.

At a framework level, it is intended to help enterprises make data AI-ready by introducing:

- certified business meaning
- governed semantic assets
- deterministic validation
- review and certification workflow
- safe AI consumption boundaries

The current repository is centered on the `business_banking_fraud_detection` example and supports:

- semantic package generation
- deterministic validation
- certification gating
- reviewer approval workflow
- local review and publish through a Streamlit cockpit

## 2. Conceptual Framework

The semantic layer is not just a BI convenience layer. In this project it acts as the trusted interpretation layer between raw enterprise data and downstream AI or analytics consumers.

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

The core principle is:

> AI systems should reason over certified business concepts and governed semantic assets, not directly over raw enterprise tables.

## 3. Current System Shape

This is a Python project with a CLI-first build pipeline and a Streamlit review UI.

The repository has two main operating modes:

- `main.py` / `semantic_foundry.cli`: build, discover, and certify semantic packages
- `review_cockpit.py`: load an existing package for review, issue capture, approval, and local publish

Generated semantic packages are written to `outputs/<use_case_id>/`.

## 4. Reference Architecture

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

## 5. Framework Layers

The project is designed around these architectural layers:

1. Domain discovery layer
Context gathering around business concepts, use cases, stakeholders, and candidate source assets.

2. Business glossary layer
Definitions, synonyms, ownership, sensitivity, and certification state for business terms.

3. Logical business entity layer
Pragmatic semantic entities such as customer, account, transaction, fraud alert, merchant, and model run.

4. Metric and KPI layer
Deterministic metric contracts with grain, formula, interpretation, and caveats.

5. Semantic view layer
Generated SQL and semantic assets that expose governed business-aligned structures.

6. Governance control layer
DQ rules, policy rules, ownership, certification gates, auditability, and issue tracking.

7. AI consumption layer
AI context cards, allowed and disallowed usage, refusal rules, safe joins, and sensitive field handling.

## 6. Component Map

| Component | Path | Responsibility | Key dependencies |
|---|---|---|---|
| CLI entry | `main.py`, `semantic_foundry/cli.py` | Exposes `discover`, `build`, and `certify` commands | `semantic_foundry.runtime` |
| Runtime orchestration | `semantic_foundry/runtime.py` | Coordinates loading, mining, generation, validation, and publish | intake, scanners, generators, builders, validators |
| Intake layer | `semantic_foundry/intake/` | Loads and validates use-case input | `simple_yaml`, `config` |
| Source scanners | `semantic_foundry/scanners/` | Builds source inventory, mines Python AST logic, classifies semantics | `ast`, fixture source paths |
| Generators | `semantic_foundry/generators/` | Creates glossary, entities, relationships, signals, predictions, metrics, policies, AI cards | `reference_data.py`, use case, logic |
| Builders | `semantic_foundry/builders/` | Builds manifests, package-level catalogues, SQL, reports, package index | generated artefacts, certification gate |
| Validators | `semantic_foundry/validators/` | Enforces source schema, DQ, policy, SQL, schema, and certification checks | generated artefacts and package files |
| Package publisher | `semantic_foundry/package/publisher.py` | Writes root semantic-package files and numbered review folders | `dump_yaml`, filesystem |
| Review service | `semantic_foundry/review/service.py` | Loads package review state, updates approvals/issues, refreshes manifest/report | package files, certification validator |
| Review cockpit UI | `semantic_foundry/review/dashboard.py`, `review_cockpit.py` | Streamlit reviewer workflow | `streamlit`, review service |
| Example fixture | `examples/business_banking_fraud/` | Use case, sample CSVs, and fraud logic inputs | build/test commands |
| Tests | `tests/unit/`, `tests/integration/` | Unit and SIT coverage | `unittest`, build/CLI runtime |

## 7. Runtime Flow

```text
Use case YAML + source files + sample CSVs
    ↓
Intake loading and source inventory
    ↓
Python AST mining and semantic classification
    ↓
Semantic / signal / metric / policy / AI artefact generation
    ↓
Deterministic validation:
  source schema
  DQ
  policy
  SQL
  certification gate
    ↓
Package publish to outputs/<use_case_id>/
    ↓
Optional review cockpit updates approvals/issues and republishes delivery artefacts
```

## 8. Data Flow

Primary data movement:

- `examples/business_banking_fraud/use_case.yaml` is loaded into a `UseCase` model
- `examples/business_banking_fraud/source/` is scanned for Python and CSV inputs
- AST-mined logic and deterministic templates generate semantic YAML contracts
- semantic SQL is rendered as draft generic SQL views
- validators execute against generated artefacts and fixture CSVs
- `outputs/business_banking_fraud_detection/` stores:
  - root semantic-package files
  - numbered review catalogues
  - delivery-pack artefacts

Review cockpit flow:

- reads package artefacts from `outputs/business_banking_fraud_detection/`
- updates asset statuses, owner fields, and issue register files
- rewrites certification report and semantic manifest
- appends review approvals and publish log entries

## 9. Configuration

Repository configuration sources:

- `pyproject.toml`: package metadata and optional review dependency
- `.python-version`: local Python version hint
- `examples/business_banking_fraud/use_case.yaml`: use-case and owner configuration

Local environment expectations:

- Python 3.14
- optional `streamlit` for the cockpit
- no committed secrets or `.env` files are required for the current example

## 10. Testing and SIT

Automated tests:

- unit tests under `tests/unit/`
- integration and SIT coverage under `tests/integration/`

Current SIT commands:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python main.py build --source examples/business_banking_fraud/source --use-case examples/business_banking_fraud/use_case.yaml --target generic_sql
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python main.py certify --package outputs/business_banking_fraud_detection
```

Current observed state:

- tests pass
- build passes
- certify completes successfully
- the default fraud package still returns `not_certifiable` with `validation_status: passed`

## 11. Deployment / Execution

Local execution:

- CLI: `python main.py <command>`
- cockpit: `python -m streamlit run review_cockpit.py`

Current deployment model:

- semantic package generation is local filesystem output only
- no warehouse deployment, CI/CD release, or platform adapter deployment is implemented in this repo yet

## 12. Governance / Operational Notes

- certification is deterministic and local; it does not represent external business sign-off
- the default package intentionally remains `not_certifiable` because unresolved business approval and synthetic-label issues are preserved
- review actions are recorded in package-local YAML files
- generated outputs are ignored by Git via `.gitignore`
- sample data is local fixture data only, not production banking data

## 13. Known Gaps

See [issues-pending-review.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/issues-pending-review.md:1).
