# Semantic_Foundry Prioritized Implementation Backlog

## Purpose

This backlog converts the current design-gap analysis into a sequenced implementation plan for the Semantic_Foundry MVP and the next hardening phases.

## Priority Levels

- `P0`: Required to make the current MVP reliable and reviewable
- `P1`: Required to satisfy the deterministic governance and certification design
- `P2`: Required to align the product structure and contracts with the detailed design
- `P3`: Scale-out and platform extension work

---

## P0: Current MVP Hardening

### 1. Strengthen deterministic unit and SIT coverage

**Problem**
The MVP has runnable tests, but coverage is still centred on the happy path.

**Scope**

- Add unit tests for metric catalogue generation
- Add unit tests for prediction catalogue generation
- Add unit tests for semantic manifest content
- Add SIT checks for stale output cleanup and rebuild safety
- Add SIT checks for nested output structure and certify behaviour

**Acceptance criteria**

- Unit tests validate current semantic, signal, prediction, metric, and manifest contracts
- SIT validates `discover -> build -> certify` and rebuild cleanup behaviour
- Test suite passes cleanly from `.venv`

**Status**
Completed

### 2. Formalize output package indexing

**Problem**
The package structure is now improved, but downstream readers still rely on directory knowledge instead of a formal package index.

**Scope**

- Extend delivery pack documentation
- Add a top-level package readme or index file
- Describe each numbered folder and intended consumer

**Acceptance criteria**

- A reviewer can open the build output and understand where to find semantic, signal, prediction, governance, and delivery artefacts

**Status**
Completed

---

## P1: Deterministic Validation and Certification

### 3. Implement source schema validation

**Problem**
The design calls for deterministic validation of discovered source structure, but the current MVP only validates artefact presence.

**Scope**

- Add `validators/source_schema_validator.py`
- Validate expected source roles, file categories, and required dataset references
- Fail when required source constructs are missing

**Acceptance criteria**

- Build fails when the source fixture is structurally incomplete
- Validation findings are surfaced in the issue register

**Status**
Completed

### 4. Implement SQL validation

**Problem**
Generated SQL is not parsed or checked against known column/view expectations.

**Scope**

- Add `validators/sql_validator.py`
- Validate generated SQL files for expected view names and required columns
- Add generic parser or deterministic structural checks

**Acceptance criteria**

- Build fails when SQL omits required semantic columns or views
- Validation results are included in the delivery pack

**Status**
Completed

### 5. Implement DQ validation

**Problem**
DQ rules are generated as metadata only; they are not executed.

**Scope**

- Add `validators/dq_validator.py`
- Evaluate critical uniqueness, completeness, and referential-integrity rules on the fixture
- Distinguish blocking vs non-blocking DQ failures

**Acceptance criteria**

- Critical DQ failures block certification progression
- Results are written into a DQ validation report and issue register

**Status**
Completed

### 6. Implement policy validation

**Problem**
Policy artefacts exist, but there is no enforcement check.

**Scope**

- Add `validators/policy_validator.py`
- Validate high-risk use cases require human review rules
- Validate restricted assets carry access restrictions
- Validate AI context cards contain disallowed questions

**Acceptance criteria**

- Policy gaps fail validation deterministically
- Missing high-risk controls are surfaced as blocking issues

**Status**
Completed

### 7. Implement real certification gate workflow

**Problem**
`certify` currently checks only for file presence, not readiness.

**Scope**

- Extend `certification_validator.py`
- Encode required approval and validation conditions
- Return real pass/fail/reason outcomes for certification readiness

**Acceptance criteria**

- Certification can distinguish draft, candidate, and not-certifiable outputs
- Blocking issues directly map to missing approval or validation requirements

**Status**
Completed

---

## P2: Contract and Workflow Alignment

### 8. Upgrade the use-case contract

**Problem**
The current use-case schema is flatter than the detailed design.

**Scope**

- Add support for `name`, `domain`, `description`, structured `users`, structured `business_questions`, and `constraints`
- Preserve existing MVP fields during migration

**Acceptance criteria**

- Intake supports the full design contract
- Business questions can point to expected semantic assets

**Status**
Pending

### 9. Enrich semantic contracts

**Problem**
Entity, signal, metric, and policy outputs are still thinner than the design contracts.

**Scope**

- Add entity attributes and source columns
- Add signal explainability, approved/disallowed use, and limitations
- Add policy enforcement, severity, and blocking flags
- Add richer semantic manifest asset registration

**Acceptance criteria**

- Generated YAML aligns materially with the design contract definitions
- Asset metadata is rich enough for review and certification workflows

**Status**
Pending

### 10. Implement asset-level semantic manifest

**Problem**
Current manifest is a run log, not a semantic asset registry.

**Scope**

- Replace run-only manifest with combined package manifest
- Include package ID, version, status, assets, asset type, file, entity, and certification state

**Acceptance criteria**

- Every generated semantic asset is traceable through the manifest
- Delivery pack consumers can resolve asset-to-file mapping deterministically

**Status**
Pending

### 11. Build human review workflow foundation

**Problem**
The design includes review roles and approval lifecycle, but there is no review module.

**Scope**

- Add `review/certification_workflow.py`
- Add `review/approval_model.py`
- Add structured issue register and approval capture models

**Acceptance criteria**

- Semantic assets can be promoted through explicit review states
- Review outcomes can be recorded and persisted

**Status**
Pending

---

## P2: Broader Source Scanning and Profiling

### 12. Add data/table profiling

**Problem**
The detailed design expects dataset profiling, but current scanning is code-centric.

**Scope**

- Add `scanners/table_profiler.py`
- Infer grain, primary keys, foreign keys, candidate measures, event time, and labels

**Acceptance criteria**

- Profile results are generated for customers, accounts, and transactions
- Semantic candidates become less hardcoded

**Status**
Pending

### 13. Add non-Python miners

**Problem**
The design includes SQL, dbt, and notebook miners; the current MVP does not.

**Scope**

- Add `scanners/sql_miner.py`
- Add `scanners/dbt_miner.py`
- Add `scanners/notebook_miner.py`

**Acceptance criteria**

- Source inventory can classify and route non-Python artefacts
- Concept extraction input is not limited to Python code

**Status**
Pending

---

## P3: LLM and Platform Extensions

### 14. Add LLM-assisted concept extraction

**Problem**
Phase 3 of the design is not started.

**Scope**

- Add `llm/client.py`
- Add prompt templates
- Add structured output validation

**Acceptance criteria**

- LLM outputs are validated before use
- Hallucinated fields are rejected deterministically

**Status**
Pending

### 15. Add review cockpit

**Problem**
The design expects a review UI; the MVP is CLI-only.

**Scope**

- Add lightweight Streamlit or web review cockpit
- Support asset review, approval, issue capture, and package publish

**Acceptance criteria**

- Reviewer can approve/reject draft assets
- Certification report updates after review activity

**Status**
Completed

### 16. Add platform adapters

**Problem**
Only generic SQL exists today.

**Scope**

- Add `dbt_builder.py`
- Add `snowflake_builder.py`
- Add `databricks_builder.py`

**Acceptance criteria**

- Same semantic package can emit platform-specific outputs
- Traceability to asset IDs is preserved

**Status**
Pending

---

## Recommended Execution Order

1. Finish P0 testing and package-index hardening
2. Implement P1 deterministic validators and certification gate
3. Upgrade contracts and manifest structure
4. Add review workflow foundation
5. Add profiling and non-Python scanners
6. Add LLM workflow
7. Add cockpit and platform adapters
