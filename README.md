# Semantic_Foundry

## Overview

Semantic_Foundry is a Python accelerator that turns a business use case, source code, and sample data into a governed semantic package.

The current implementation focuses on the `business_banking_fraud_detection` example and produces:

- semantic catalogues
- signal and metric catalogues
- DQ and policy validation outputs
- generated semantic SQL
- certification artefacts
- a Streamlit review cockpit for approval and publish workflow

## Architecture Summary

The repository is organized around a deterministic build pipeline:

1. load use case input
2. scan source files and mine Python logic
3. generate semantic, signal, metric, policy, and AI artefacts
4. run deterministic validation gates
5. publish a reviewable semantic package
6. support review and publish updates through the cockpit

See [design/architecture.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/architecture.md:1) for the full system view.

## Repository Structure

```text
semantic_foundry/
├── semantic_foundry/         # Python package code
├── examples/                 # Fraud fixture and use case
├── tests/                    # Unit and integration/SIT coverage
├── design/                   # Architecture, design, and review docs
├── outputs/                  # Generated semantic packages
├── main.py                   # CLI entry point
└── review_cockpit.py         # Streamlit review cockpit entry point
```

## Setup

Create or activate a Python 3.14 virtual environment, then install runtime dependencies as needed.

For the review cockpit, install Streamlit in the active environment:

```bash
python -m pip install setuptools wheel
python -m pip install streamlit
```

## Run

Build the example semantic package:

```bash
python main.py build \
  --source examples/business_banking_fraud/source \
  --use-case examples/business_banking_fraud/use_case.yaml \
  --target generic_sql
```

Inspect discovery output:

```bash
python main.py discover \
  --source examples/business_banking_fraud/source \
  --use-case examples/business_banking_fraud/use_case.yaml
```

Check certification state:

```bash
python main.py certify --package outputs/business_banking_fraud_detection
```

Launch the review cockpit:

```bash
python -m streamlit run review_cockpit.py
```

## Test / SIT

Primary automated test command:

```bash
python -m unittest discover -s tests
```

Practical SIT / smoke flow:

```bash
python main.py build \
  --source examples/business_banking_fraud/source \
  --use-case examples/business_banking_fraud/use_case.yaml \
  --target generic_sql

python main.py certify --package outputs/business_banking_fraud_detection
```

## Configuration

Key project inputs:

- use case YAML: `examples/business_banking_fraud/use_case.yaml`
- sample source data and Python logic: `examples/business_banking_fraud/source/`
- packaging config: `pyproject.toml`

No secret values should be committed into the repository.

## Documentation

- Architecture: [design/architecture.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/architecture.md:1)
- Semantic package design: [design/semantic_foundry_semantic_package_detailed_design.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/semantic_foundry_semantic_package_detailed_design.md:1)
- Pending review issues: [design/issues-pending-review.md](/Users/emilygao/LocalDocuments/Projects/semantic_foundry/design/issues-pending-review.md:1)

## Current Status

The build and validation pipeline is operational and the review cockpit is present, but the default fraud package is still intentionally `not_certifiable` because business approvals and synthetic-label caveats remain open for review.
