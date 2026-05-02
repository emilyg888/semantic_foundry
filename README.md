# Semantic_Foundry

MVP scaffold for the Semantic_Foundry accelerator described in [design/semantic_foundry_detailed_design.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/semantic_foundry_detailed_design.md:1).

The current implementation follows the design doc's Phase 1 roadmap:

- CLI skeleton
- source inventory scanner
- Python AST logic miner
- deterministic semantic artefact generation
- semantic SQL and certification report publishing
- integration tests over a business banking fraud fixture

## Quick Start

Create or activate your virtualenv, then run:

```bash
python main.py build \
  --source examples/business_banking_fraud/source \
  --use-case examples/business_banking_fraud/use_case.yaml \
  --target generic_sql
```

The build writes the MVP package to:

```text
outputs/business_banking_fraud_detection/
```

## CLI

```bash
python main.py discover --source examples/business_banking_fraud/source --use-case examples/business_banking_fraud/use_case.yaml
python main.py build --source examples/business_banking_fraud/source --use-case examples/business_banking_fraud/use_case.yaml --target generic_sql
python main.py certify --package outputs/business_banking_fraud_detection
```

`discover` now returns a structured discovery report with:

- raw code-mining output under `discovery`
- `semantic_layer_candidates`
- `signal_layer_candidates`
- `alert_layer_candidates`
- `governance_context`

## Generated Output

The MVP build produces:

```text
01_semantic_catalogue/
  glossary.yaml
  entities.yaml
  relationships.yaml
02_signal_catalogue/
  signals.yaml
03_prediction_catalogue/
  predictions.yaml
04_evaluation_metric_catalogue/
  metrics.yaml
05_governance_controls/
  dq_rules.yaml
  policies.yaml
  issue_register.yaml
06_ai_consumption/
  ai_context_cards.yaml
07_delivery_pack/
  semantic_manifest.yaml
  semantic_views.sql
  certification_report.md
```

## Tests

```bash
python -m unittest discover -s tests
```

Current test split:

- Unit tests cover source inventory, Python AST logic mining, YAML/loading, and artefact validation.
- SIT covers the CLI-level `discover -> build -> certify` workflow against the fraud fixture.
