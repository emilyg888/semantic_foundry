from __future__ import annotations

from semantic_foundry.config import UseCase


def build_package_index(use_case: UseCase) -> str:
    return f"""# Semantic_Foundry Package Index

## Use Case
{use_case.use_case_id}

## Purpose
This package contains the generated Semantic_Foundry MVP artefacts for business banking fraud detection.

## Package Guide

### `01_semantic_catalogue/`
- Consumer: business owner, data steward, semantic reviewer
- Contents: glossary, entities, relationships
- Start with: `glossary.yaml`

### `02_signal_catalogue/`
- Consumer: fraud analyst, fraud analytics reviewer
- Contents: derived fraud signal definitions
- Start with: `signals.yaml`

### `03_prediction_catalogue/`
- Consumer: fraud analyst, model reviewer
- Contents: predicted fraud outputs and fraud score contracts
- Start with: `predictions.yaml`

### `04_evaluation_metric_catalogue/`
- Consumer: fraud analytics lead, model governance reviewer
- Contents: detector evaluation metrics and operational alert metrics
- Start with: `metrics.yaml`

### `05_governance_controls/`
- Consumer: risk owner, governance lead, data steward
- Contents: data quality rules, DQ validation results, policy rules, policy validation results, issue register
- Start with: `dq_validation.yaml`

### `06_ai_consumption/`
- Consumer: AI product owner, copilot designer
- Contents: AI context cards and safe-use guidance
- Start with: `ai_context_cards.yaml`

### `07_delivery_pack/`
- Consumer: engagement lead, technical reviewer, certification reviewer
- Contents: semantic manifest, generated SQL, certification report
- Start with: `certification_report.md`

## Recommended Review Order
1. `01_semantic_catalogue/glossary.yaml`
2. `01_semantic_catalogue/entities.yaml`
3. `02_signal_catalogue/signals.yaml`
4. `03_prediction_catalogue/predictions.yaml`
5. `04_evaluation_metric_catalogue/metrics.yaml`
6. `05_governance_controls/policies.yaml`
7. `07_delivery_pack/certification_report.md`
"""
